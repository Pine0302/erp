#!/usr/bin/env python3
"""对比 v1 与 v2 的说话人标注版，输出差异 JSON（供生成对比文档）。

比较层：
1. 片段数；2. 正文/时间/原始标签逐段一致性；3. 说话人归属差异（按 (v1名, v2名) 聚合计数）。
v1 行格式：[start–end] **speaker**（`S0X`·置信度）：body
v2 行格式：[会议X-0001] [start–end] **speaker**（①…｜原始标签：S0X）：body〔例外段：…〕
"""
import re
import json
from pathlib import Path
from collections import Counter

ROOT = Path('/home/pine/workspace/erp/metting/speaker-labeled')

FILES = [
    ("会议1", "会议1-说话人标注版.md"),
    ("会议2", "会议2-说话人标注版.md"),
    ("会议3", "会议3-说话人标注版.md"),
    ("会议4", "会议4-说话人标注版.md"),
    ("会议5-part1", "会议5-part1-说话人标注版.md"),
    ("会议5-part2", "会议5-part2-说话人标注版.md"),
    ("会议5-part3", "会议5-part3-说话人标注版.md"),
    ("会议6", "会议6-驻点高老师-说话人标注版.md"),
]

PAT_V1 = re.compile(r'^\[([0-9.]+)–([0-9.?]+)\] \*\*(.+?)\*\*（`?(S\d+)`?·(.+?)）：(.*)$')
PAT_V2 = re.compile(r'^\[会议\S+-(\d{4})\] \[([0-9.]+)–(.+?)\] \*\*(.+?)\*\*（(.+?)｜原始标签：(S\d+)）：(.*)$')


def parse_v1(path):
    out = []
    for l in path.read_text(encoding='utf-8').splitlines():
        m = PAT_V1.match(l)
        if m:
            out.append({'start': m.group(1), 'end': m.group(2), 'spk': m.group(3),
                        'label': m.group(4), 'body': m.group(6)})
    return out


def parse_v2(path):
    out = []
    for l in path.read_text(encoding='utf-8').splitlines():
        m = PAT_V2.match(l)
        if m:
            body = m.group(7)
            mm = re.search(r'〔例外段：.*〕$', body)
            if mm:
                body = body[:mm.start()]
            out.append({'num': m.group(1), 'start': m.group(2), 'end': m.group(3),
                        'spk': m.group(4), 'label': m.group(6), 'body': body})
    return out


def main():
    result = {}
    for prefix, fname in FILES:
        v1 = parse_v1(ROOT / 'v1' / fname)
        v2 = parse_v2(ROOT / 'v2' / fname)
        entry = {'file': fname, 'n_v1': len(v1), 'n_v2': len(v2)}
        if len(v1) != len(v2):
            entry['error'] = '行数不一致，无法逐段对齐'
            result[prefix] = entry
            continue
        entry['n_body_diff'] = sum(1 for a, b in zip(v1, v2) if a['body'] != b['body'])
        entry['n_time_diff'] = sum(1 for a, b in zip(v1, v2)
                                   if (a['start'], a['end']) != (b['start'], b['end']))
        entry['n_label_diff'] = sum(1 for a, b in zip(v1, v2) if a['label'] != b['label'])
        diffs = Counter()
        diff_uids = []
        for i, (a, b) in enumerate(zip(v1, v2), 1):
            if a['spk'] != b['spk']:
                diffs[(a['spk'], b['spk'])] += 1
                diff_uids.append(i)
        entry['n_spk_diff'] = sum(diffs.values())
        entry['spk_diffs'] = [{'v1': k[0], 'v2': k[1], 'count': v} for k, v in diffs.most_common()]
        entry['diff_uids'] = diff_uids
        result[prefix] = entry
        print(f"{prefix}: v1={len(v1)} v2={len(v2)} 正文差={entry['n_body_diff']} "
              f"时间差={entry['n_time_diff']} 标签差={entry['n_label_diff']} 归属差={entry['n_spk_diff']}")
        for d in entry['spk_diffs']:
            print(f"    v1[{d['v1']}] vs v2[{d['v2']}]: {d['count']}")
    (ROOT / 'v2' / 'work' / 'v1v2-compare.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
    print("\n已写入 work/v1v2-compare.json")


if __name__ == '__main__':
    main()
