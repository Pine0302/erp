"""验证对话格式标注版的完整性"""
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

# 对话行格式: [start–end] **说话人**（`标签`·置信度）：正文
# 使用 Unicode 转义确保字符正确
LINE_RE = re.compile(
    r'^\[(\d+\.\d+)\u2013(\?|\d+\.\d+)\] \*\*([^*]+)\*\*\uff08`(S\d+)`\u00b7(高置信度|推定|待确认)\uff09\uff1a(.*)$'
)

all_ok = True
total_segs = 0
total_lines = 0

for src_name, out_name in files_map.items():
    segs = json.loads((PARSED / f'{src_name}.segments.json').read_text(encoding='utf-8'))
    out_text = (OUT_DIR / out_name).read_text(encoding='utf-8')
    
    # 提取所有对话行
    dialogue_lines = []
    for line in out_text.split('\n'):
        m = LINE_RE.match(line)
        if m:
            dialogue_lines.append({
                'start': float(m.group(1)),
                'end': m.group(2),
                'speaker': m.group(3),
                'label': m.group(4),
                'conf': m.group(5),
                'text': m.group(6),
            })
    
    # 比对
    issues = []
    
    if len(segs) != len(dialogue_lines):
        issues.append(f'片段数不匹配: 原始={len(segs)}, 对话行={len(dialogue_lines)}')
    
    # 顺序检查
    for i, (seg, dl) in enumerate(zip(segs, dialogue_lines)):
        if abs(seg['start_time'] - dl['start']) > 0.001:
            issues.append(f'idx={seg["index"]}: 时间不一致 原始={seg["start_time"]} 对话={dl["start"]}')
        if seg['label'] != dl['label']:
            issues.append(f'idx={seg["index"]}: 标签不一致 原始={seg["label"]} 对话={dl["label"]}')
        seg_text = seg['text'].strip()
        dl_text = dl['text'].strip()
        if seg_text != dl_text:
            issues.append(f'idx={seg["index"]}: 正文不匹配')
        if issues and len(issues) > 3:
            break
    
    if issues:
        all_ok = False
        print(f"❌ {src_name}: {len(issues)} 处问题")
        for iss in issues[:3]:
            print(f"  - {iss}")
    else:
        total_segs += len(segs)
        total_lines += len(dialogue_lines)
        print(f"✅ {src_name}: {len(segs)} 段 → {len(dialogue_lines)} 行对话")

print()
print(f"总片段: {total_segs}, 总对话行: {total_lines}")
if all_ok:
    print("🎉 所有对话格式标注版完整性通过")
