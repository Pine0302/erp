"""批量解析所有转写文件"""
import json
from parse_asr import parse_file
from pathlib import Path
from collections import Counter

SRC = Path('/home/pine/workspace/erp/metting/transcripts')
DST = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed')
DST.mkdir(parents=True, exist_ok=True)

files = sorted(SRC.glob('*.txt'))
summary = {}
for f in files:
    segs = parse_file(str(f))
    # 输出每段
    out = DST / (f.stem + '.segments.json')
    out.write_text(json.dumps(segs, ensure_ascii=False, indent=2), encoding='utf-8')
    cnt = Counter(s['label'] for s in segs)
    summary[f.name] = {'count': len(segs), 'labels': dict(cnt)}
    print(f"{f.name}: {len(segs)} segments, labels={dict(cnt)}")

print("\nSummary:")
print(json.dumps(summary, ensure_ascii=False, indent=2))
