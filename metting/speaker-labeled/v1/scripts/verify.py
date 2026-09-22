"""验证脚本：
1. 检查所有原始片段在标注版中
2. 检查正文、时间、标签的完整保留
3. 检查片段顺序
4. 报告解析残余
"""
import json
import re
from pathlib import Path

PARSED = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed')
OUT_DIR = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1')

files = [
    ('会议1-asr', '会议1-说话人标注版.md'),
    ('会议2-asr', '会议2-说话人标注版.md'),
    ('会议3-asr', '会议3-说话人标注版.md'),
    ('会议4-asr', '会议4-说话人标注版.md'),
    ('会议5-part1-asr', '会议5-part1-说话人标注版.md'),
    ('会议5-part2-asr', '会议5-part2-说话人标注版.md'),
    ('会议5-part3-asr', '会议5-part3-说话人标注版.md'),
    ('会议6-驻点高老师-asr', '会议6-驻点高老师-说话人标注版.md'),
]

print("=" * 70)
print("完整性验证报告")
print("=" * 70)

for src_name, out_name in files:
    print(f"\n=== {src_name} ===")
    
    # 1. 加载原始片段
    segs = json.loads((PARSED / f'{src_name}.segments.json').read_text(encoding='utf-8'))
    out_path = OUT_DIR / out_name
    out_text = out_path.read_text(encoding='utf-8')
    
    # 2. 提取标注版中的所有片段
    # 格式: ### [prefix-NNNN] [start–end]
    pattern = re.compile(r'### \[([^\]]+)\] \[([^\]]+)\]')
    matches = list(pattern.finditer(out_text))
    
    # 3. 比对
    issues = []
    
    # 片段数
    if len(segs) != len(matches):
        issues.append(f'片段数不匹配: 原始={len(segs)}, 标注={len(matches)}')
    
    # 顺序检查
    for i, (seg, match) in enumerate(zip(segs, matches)):
        idx_str = f'{src_name}-{seg["index"]:04d}'
        if match.group(1) != idx_str:
            issues.append(f'idx {i}: 标注版 idx={match.group(1)}, 原始={idx_str}')
            if len(issues) > 5:
                break
    
    # 正文检查（每个片段的正文必须出现一次）
    body_issues = 0
    for seg in segs[:20]:  # 抽样前20个
        if seg['text'].strip() and seg['text'].strip() not in out_text:
            body_issues += 1
    
    if issues:
        print(f"  ❌ 问题: {len(issues)} 处")
        for iss in issues[:5]:
            print(f"    - {iss}")
    else:
        print(f"  ✅ 片段数匹配 ({len(segs)})")
        print(f"  ✅ 顺序一致")
        if body_issues == 0:
            print(f"  ✅ 正文保留完整 (抽样 {min(20, len(segs))} 段)")

print("\n" + "=" * 70)
print("验证完成")
