"""完整正文检查：每个原始片段的正文都在标注版中出现"""
import json
from pathlib import Path

PARSED = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed')
OUT_DIR = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1')

files = [
    '会议1-asr', '会议2-asr', '会议3-asr', '会议4-asr',
    '会议5-part1-asr', '会议5-part2-asr', '会议5-part3-asr',
    '会议6-驻点高老师-asr',
]

all_ok = True

for src_name in files:
    segs = json.loads((PARSED / f'{src_name}.segments.json').read_text(encoding='utf-8'))
    out_path = OUT_DIR / f'{src_name.replace("-asr", "")}-说话人标注版.md'
    # 会议6 名称特殊
    if '会议6' in src_name:
        out_path = OUT_DIR / '会议6-驻点高老师-说话人标注版.md'
    
    out_text = out_path.read_text(encoding='utf-8')
    
    missing = []
    for seg in segs:
        text = seg['text'].strip()
        if text and text not in out_text:
            missing.append((seg['index'], text[:50]))
    
    if missing:
        print(f"❌ {src_name}: {len(missing)} 处正文缺失")
        for idx, t in missing[:5]:
            print(f"   idx={idx}: {t}")
        all_ok = False
    else:
        total_text = sum(len(s['text'].strip()) for s in segs if s['text'].strip())
        print(f"✅ {src_name}: {len(segs)} 段正文全部保留，总字符 {total_text}")

print()
print("=" * 50)
if all_ok:
    print("🎉 所有文件正文完整保留")
else:
    print("⚠️ 部分文件存在正文缺失")
