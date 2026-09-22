"""验证：原始标签和起止时间在标注版中都被保留"""
import json
import re
from pathlib import Path

PARSED = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed')
OUT_DIR = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1')

files_map = {
    '会议1-asr': '会议1-说话人标注版.md',
    '会议2-asr': '会议2-说话人标注版.md',
    '会议3-asr': '会议3-说话人标注版.md',
    '会议4-asr': '会议4-说话人标注版.md',
    '会议5-part1-asr': '会议5-part1-说话人标注版.md',
    '会议5-part2-asr': '会议5-part2-说话人标注版.md',
    '会议5-part3-asr': '会议5-part3-说话人标注版.md',
    '会议6-驻点高老师-asr': '会议6-驻点高老师-说话人标注版.md',
}

all_ok = True

for src_name, out_name in files_map.items():
    segs = json.loads((PARSED / f'{src_name}.segments.json').read_text(encoding='utf-8'))
    out_text = (OUT_DIR / out_name).read_text(encoding='utf-8')
    
    label_missing = []
    time_missing = []
    
    for seg in segs:
        label = seg['label']
        # 检查标签在标注版中（原始标签行）
        if f'原始标签：`{label}`' not in out_text:
            label_missing.append((seg['index'], label))
        
        # 检查起止时间
        start = seg['start_time']
        end = seg['end_time']
        if end is None:
            end_str = '?'
        else:
            end_str = f'{end:.2f}'
        start_str = f'{start:.2f}'
        expected_time = f'[{start_str}–{end_str}]'
        if expected_time not in out_text:
            time_missing.append((seg['index'], expected_time))
    
    if label_missing or time_missing:
        all_ok = False
        print(f"❌ {src_name}")
        if label_missing:
            print(f"  标签缺失: {len(label_missing)} 处")
            for x in label_missing[:3]:
                print(f"    {x}")
        if time_missing:
            print(f"  时间缺失: {len(time_missing)} 处")
            for x in time_missing[:3]:
                print(f"    {x}")
    else:
        print(f"✅ {src_name}: {len(segs)} 段标签和时间均保留")

print()
if all_ok:
    print("🎉 所有原始标签和时间戳完整保留")
