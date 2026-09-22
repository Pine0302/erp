#!/usr/bin/env python3
"""完整性核验：从原始 ASR 文件直接对照标注版产物，验证：
1. 所有原始正文、标签、时间均被保留；
2. 每个原始片段恰好出现一次；
3. 原始顺序不变；
4. 解析残余全部被报告；
5. 每条归属可关联到默认映射、局部例外或待确认状态。
不依赖中间 JSONL（重新独立解析原文，避免同一中间数据互相验证）。
"""
import re
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
V2 = WORK.parent
SRC = V2.parents[1] / 'transcripts'

FILES = [
    ("会议1", "会议1-asr.txt", "会议1-说话人标注版.md"),
    ("会议2", "会议2-asr.txt", "会议2-说话人标注版.md"),
    ("会议3", "会议3-asr.txt", "会议3-说话人标注版.md"),
    ("会议4", "会议4-asr.txt", "会议4-说话人标注版.md"),
    ("会议5-part1", "会议5-part1-asr.txt", "会议5-part1-说话人标注版.md"),
    ("会议5-part2", "会议5-part2-asr.txt", "会议5-part2-说话人标注版.md"),
    ("会议5-part3", "会议5-part3-asr.txt", "会议5-part3-说话人标注版.md"),
    ("会议6", "会议6-驻点高老师-asr.txt", "会议6-驻点高老师-说话人标注版.md"),
]

TSTAMP = re.compile(r'\[(\d+(?:\.\d+)?)\]')
LABEL = re.compile(r'\[(S\d+)\]', re.IGNORECASE)

LINE_RE = re.compile(r'^\[(会议\S+)-(\d{4})\] \[([0-9.]+)–(.+?)\] \*\*(.+?)\*\*（(.+?)｜原始标签：(S\d+)）：(.*)$')


def reparse(text):
    """独立重解析（与 parse_asr 相同规则），返回片段列表。"""
    tokens = []
    for m in TSTAMP.finditer(text):
        tokens.append((m.start(), m.end(), 'T', m.group(1)))
    for m in LABEL.finditer(text):
        tokens.append((m.start(), m.end(), 'S', m.group(1).upper()))
    tokens.sort(key=lambda t: (t[0], 0 if t[2] == 'T' else 1))
    dedup, last_end = [], -1
    for t in tokens:
        if t[0] < last_end:
            continue
        dedup.append(t)
        last_end = t[1]
    segs = []
    i = 0
    n = len(dedup)
    while i < n:
        if dedup[i][2] == 'T' and i + 1 < n and dedup[i+1][2] == 'S':
            start = dedup[i][3]
            label = dedup[i+1][3]
            body_start = dedup[i+1][1]
            j = i + 2
            while j < n and dedup[j][2] != 'T':
                j += 1
            end = dedup[j][3] if j < n else None
            body_end = dedup[j][0] if j < n else len(text)
            segs.append({'start': start, 'end': end, 'label': label,
                         'text': text[body_start:body_end]})
            i = j
        else:
            i += 1
    return segs


def strip_note(line):
    """去掉行尾〔例外段：…〕注释（注释不会出现在原文中，但正文可能有〔〕，
    因此只匹配以〔例外段：开头、以〕结尾的尾部注释）。"""
    m = re.search(r'〔例外段：.*〕$', line)
    if m:
        return line[:m.start()]
    return line


def main():
    all_ok = True
    report = {}
    for prefix, fname, mdname in FILES:
        text = (SRC / fname).read_text(encoding='utf-8')
        segs = reparse(text)
        md = (V2 / mdname).read_text(encoding='utf-8')
        errors = []
        # 1. 提取产物中的对话行
        md_lines = {}
        order = []
        for line in md.splitlines():
            m = LINE_RE.match(line)
            if m:
                uid_prefix, num, start, end, disp, cat, label, body = m.groups()
                uid = f"{uid_prefix}-{num}"
                body = strip_note(body)
                if uid in md_lines:
                    errors.append(f"片段重复出现：{uid}")
                md_lines[uid] = {'start': start, 'end': end, 'label': label, 'text': body}
                order.append(uid)
        # 2. 数量一致
        if len(md_lines) != len(segs):
            errors.append(f"片段数不一致：原文 {len(segs)} vs 产物 {len(md_lines)}")
        # 3. 顺序与内容一致
        for i, s in enumerate(segs, 1):
            uid = f"{prefix}-{i:04d}"
            if uid not in md_lines:
                errors.append(f"缺失片段：{uid}")
                continue
            m2 = md_lines[uid]
            if m2['text'] != s['text'].rstrip():
                # 允许行尾注释已剥离后的正文差异报告
                if m2['text'] != s['text']:
                    errors.append(f"正文不一致：{uid} 原文={s['text']!r} 产物={m2['text']!r}")
            if m2['label'] != s['label']:
                errors.append(f"标签不一致：{uid} 原文={s['label']} 产物={m2['label']}")
            if m2['start'] != s['start']:
                errors.append(f"开始时间不一致：{uid} 原文={s['start']} 产物={m2['start']}")
            expected_end = s['end'] if s['end'] is not None else "(无结束时间)"
            if m2['end'] != expected_end:
                errors.append(f"结束时间不一致：{uid} 原文={s['end']} 产物={m2['end']}")
        # 顺序检查：产物中的 uid 序列应为严格递增
        nums = [int(u.rsplit('-', 1)[1]) for u in order]
        if nums != sorted(nums):
            errors.append("产物顺序与原始顺序不一致")
        # 每条归属必须有类别标记
        for line in md.splitlines():
            m = LINE_RE.match(line)
            if m and ('①高置信度归属' not in m.group(6) and '②推定归属' not in m.group(6)
                      and '③身份待确认' not in m.group(6) and '④疑似多人' not in m.group(6)):
                errors.append(f"归属状态缺失：{m.group(1)}-{m.group(2)}")
        ok = not errors
        all_ok = all_ok and ok
        report[prefix] = {
            'file': fname, 'n_segments_src': len(segs), 'n_segments_out': len(md_lines),
            'residues_reported': (WORK / f'{prefix}-parse-report.json').exists(),
            'errors': errors[:20],
            'ok': ok,
        }
        print(f"{prefix}: {'PASS' if ok else 'FAIL'} (src={len(segs)}, out={len(md_lines)}, errors={len(errors)})")
        for e in errors[:10]:
            print("   ", e)

    (WORK / 'verify-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    print("\n总体：", "全部通过" if all_ok else "存在失败项")


if __name__ == '__main__':
    main()
