#!/usr/bin/env python3
"""严格解析 8 份 ASR 转写为片段 JSONL（v2 版本）。

格式：[开始][S01]正文[结束][下一段开始][S02]正文[结束]...
规则：
- 片段起点 = 时间戳后紧跟说话人标签 [T][S] 对；
- 该段正文 = 从标签结束到下一个时间戳之前（原文截取，不做任何清洗）；
- 该段结束时间 = 正文后第一个时间戳；
- 下一个 [T][S] 对的开始时间与上一段结束时间之间可能存在孤立时间戳（插话重叠），跳过；
- 孤立标签（无前置时间戳）单独记录；
- 残余（token 之间的非空文本）全部保留并报告。
完整性：所有片段正文+残余的字符总长 + token 字符总长 == 原文总长。
"""
import re
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent          # .../speaker-labeled/v2/work
SRC = BASE.parents[2] / 'transcripts'           # .../metting/transcripts
OUT = BASE

FILES = [
    ("会议1", "会议1-asr.txt"),
    ("会议2", "会议2-asr.txt"),
    ("会议3", "会议3-asr.txt"),
    ("会议4", "会议4-asr.txt"),
    ("会议5-part1", "会议5-part1-asr.txt"),
    ("会议5-part2", "会议5-part2-asr.txt"),
    ("会议5-part3", "会议5-part3-asr.txt"),
    ("会议6", "会议6-驻点高老师-asr.txt"),
]

TSTAMP = re.compile(r'\[(\d+(?:\.\d+)?)\]')
LABEL = re.compile(r'\[(S\d+)\]', re.IGNORECASE)


def tokenize(text):
    tokens = []
    for m in TSTAMP.finditer(text):
        tokens.append({'pos': m.start(), 'end': m.end(), 'kind': 'T', 'val': m.group(1)})
    for m in LABEL.finditer(text):
        tokens.append({'pos': m.start(), 'end': m.end(), 'kind': 'S', 'val': m.group(1).upper()})
    tokens.sort(key=lambda t: (t['pos'], 0 if t['kind'] == 'T' else 1))
    dedup, last_end = [], -1
    for t in tokens:
        if t['pos'] < last_end:
            continue
        dedup.append(t)
        last_end = t['end']
    return dedup


def parse(text):
    tokens = tokenize(text)
    n = len(tokens)
    segments = []
    idx = 0
    while idx < n:
        tok = tokens[idx]
        if tok['kind'] == 'T':
            if idx + 1 < n and tokens[idx + 1]['kind'] == 'S':
                start_t = tok['val']
                label = tokens[idx + 1]['val']
                body_start = tokens[idx + 1]['end']
                j = idx + 2
                while j < n and tokens[j]['kind'] != 'T':
                    j += 1
                end_t = tokens[j]['val'] if j < n else None
                body_end = tokens[j]['pos'] if j < n else len(text)
                body = text[body_start:body_end]
                segments.append({'start': start_t, 'end': end_t, 'label': label,
                                 'text': body, 'char_pos': body_start,
                                 'raw_span': f"{body_start}-{body_end}"})
                idx = j
                continue
            else:
                idx += 1
                continue
        else:
            label = tok['val']
            j = idx + 1
            while j < n and tokens[j]['kind'] != 'T':
                j += 1
            body_end = tokens[j]['pos'] if j < n else len(text)
            segments.append({'start': None, 'end': tokens[j]['val'] if j < n else None,
                             'label': label, 'text': text[tok['end']:body_end],
                             'char_pos': tok['end'], 'raw_span': f"{tok['end']}-{body_end}",
                             'no_start_time': True})
            idx = j if j < n else n
            continue
    # 残余 = 非 token 且非片段正文的非空文本
    covered = [(t['pos'], t['end']) for t in tokens]
    for s in segments:
        covered.append((s['char_pos'], s['char_pos'] + len(s['text'])))
    covered.sort()
    residue = []
    prev = 0
    for s, e in covered:
        if s > prev:
            g = text[prev:s]
            if g.strip():
                residue.append({'pos': prev, 'len': s - prev, 'text': g})
        prev = max(prev, e)
    if prev < len(text):
        g = text[prev:]
        if g.strip():
            residue.append({'pos': prev, 'len': len(text) - prev, 'text': g})
    return segments, residue


def main():
    for prefix, fname in FILES:
        path = SRC / fname
        text = path.read_text(encoding='utf-8')
        segs, residue = parse(text)
        out_path = OUT / f'{prefix}-segments.jsonl'
        with open(out_path, 'w', encoding='utf-8') as f:
            for k, s in enumerate(segs, 1):
                s['uid'] = f'{prefix}-{k:04d}'
                s['src'] = fname
                f.write(json.dumps(s, ensure_ascii=False) + '\n')
        seg_chars = sum(len(s['text']) for s in segs)
        res_chars = sum(len(r['text']) for r in residue)
        tok_chars = 0
        prev = 0
        for t in tokenize(text):
            if t['pos'] >= prev:
                tok_chars += t['end'] - t['pos']
                prev = t['end']
        labels = sorted(set(s['label'] for s in segs))
        rep = {
            'file': fname, 'total_chars': len(text), 'n_segments': len(segs),
            'seg_chars': seg_chars, 'residue_chars': res_chars, 'token_chars': tok_chars,
            'check_sum_ok': (seg_chars + res_chars + tok_chars) == len(text),
            'labels': labels,
            'label_counts': {l: sum(1 for s in segs if s['label'] == l) for l in labels},
            'n_no_start': sum(1 for s in segs if s.get('no_start_time')),
            'n_no_end': sum(1 for s in segs if s['end'] is None),
            'n_empty_body': sum(1 for s in segs if not s['text']),
            'n_residues': len(residue),
            'residues': residue,
        }
        (OUT / f'{prefix}-parse-report.json').write_text(
            json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f"{fname}: segs={len(segs)} labels={rep['label_counts']} "
              f"no_start={rep['n_no_start']} no_end={rep['n_no_end']} "
              f"empty={rep['n_empty_body']} residue={len(residue)} "
              f"sum_ok={rep['check_sum_ok']}")


if __name__ == '__main__':
    main()
