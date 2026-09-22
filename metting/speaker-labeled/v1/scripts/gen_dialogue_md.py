"""生成对话格式的说话人标注版
格式：每条发言一行；换人换行
[时间戳] 说话人（原始标签·置信度）：正文
"""
import json
from pathlib import Path
from collections import Counter

PARSED = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed')
OUT_DIR = Path('/home/pine/workspace/erp/metting/speaker-labeled/v1')

# === 复用 speaker_mapping.py 中的映射（合并引入）===
import sys
sys.path.insert(0, str(Path(__file__).parent))
from speaker_mapping import MAPPINGS, PART1_S04_RANGES, get_part1_s04

# 置信度简称
CONF_DISP = {
    'high': '高置信度',
    'medium': '推定',
    'low': '待确认',
}

# 说话人简称（用于行内显示）
# 短名映射
SHORT_NAME = {
    # 会议1-5 S01
    'S01': {
        '会议1-asr': '津金',
        '会议2-asr': '津金',
        '会议3-asr': '津金',
        '会议4-asr': '津金',
        '会议5-part1-asr': '津金',
        '会议5-part2-asr': '津金',
        '会议5-part3-asr': '津金',
    },
    'S02': {
        '会议1-asr': 'Pine',
        '会议2-asr': 'Pine',
        '会议3-asr': 'Pine',
        '会议4-asr': 'Pine',
        '会议5-part1-asr': 'Pine',
        '会议5-part2-asr': 'Pine',
        '会议5-part3-asr': 'Pine',
        '会议6-驻点高老师-asr': 'Pine',
    },
    'S03': {
        '会议1-asr': '小叶/沈歪歪',
        '会议5-part1-asr': '杜文颖',
        '会议5-part2-asr': '周老师?',
        '会议5-part3-asr': '周老师',
    },
    'S04': {
        '会议5-part1-asr': 'S04',  # 分段处理
        '会议5-part2-asr': '杜文颖',
        '会议5-part3-asr': '杜文颖',
    },
    'S05': {
        '会议5-part1-asr': '夏经理',
        '会议5-part2-asr': '周老师',
    },
}


def get_short_name(file_prefix, label, seg_idx):
    """获取用于行内显示的简短名称"""
    if file_prefix == '会议5-part1-asr' and label == 'S04':
        disp, conf, note = get_part1_s04(seg_idx)
    elif label in MAPPINGS.get(file_prefix, {}):
        disp, conf, note = MAPPINGS[file_prefix][label]
    else:
        disp = f'未识别（{label}）'
    
    # 提取主要标识，去除括号说明
    if '（' in disp:
        disp = disp.split('（')[0]
    return disp


def get_speaker_display(file_prefix, label, seg_idx, text_hint=''):
    """获取完整显示名与置信度（用于映射表）"""
    if file_prefix == '会议5-part1-asr' and label == 'S04':
        disp, conf, note = get_part1_s04(seg_idx)
    elif label in MAPPINGS.get(file_prefix, {}):
        disp, conf, note = MAPPINGS[file_prefix][label]
    else:
        disp = f'未识别（{label}）'
        conf = 'low'
    
    return disp, conf


def fmt_segment_dialogue(seg, file_prefix):
    """生成单条对话行"""
    label = seg['label']
    start = seg['start_time']
    end = seg['end_time']
    end_str = '?' if end is None else f'{end:.2f}'
    
    short = get_short_name(file_prefix, label, seg['index'])
    disp_full, conf = get_speaker_display(file_prefix, label, seg['index'])
    conf_short = CONF_DISP.get(conf, conf)
    
    text = seg['text'].strip()
    
    # 格式：[start–end] 说话人（标签·置信度）：正文
    return f'[{start:.2f}–{end_str}] **{short}**（`{label}`·{conf_short}）：{text}'


def write_dialogue_file(name, output_path):
    segs = json.loads((PARSED / f'{name}.segments.json').read_text(encoding='utf-8'))
    mapping = MAPPINGS[name]
    
    lines = []
    lines.append(f'# 会议：{name}')
    lines.append('')
    lines.append('> 本文档为**对话格式**标注版。每条发言一行；换人换行；保留原始正文、原始起止时间与原始标签。')
    lines.append('')
    
    # 说话人映射表
    lines.append('## 说话人映射（本文件）')
    lines.append('')
    label_counts = Counter(s['label'] for s in segs)
    lines.append('| 原始标签 | 规范身份 | 置信度 | 备注 |')
    lines.append('| --- | --- | --- | --- |')
    for label in sorted(label_counts.keys()):
        if name == '会议5-part1-asr' and label == 'S04':
            disp_overall = '王师傅/夏经理（分段处理，见下方）'
            conf_disp = '中（推定）/边界待确认'
            note_overall = 'S04 标签在不同区间对应不同身份：idx=110-130 为王师傅，idx=143-312 为夏经理；同一录音设备或账号导致混用'
            note_escaped = note_overall.replace('|', '\\|')
            lines.append(f'| `{label}` | {disp_overall} | {conf_disp} | {note_escaped} |')
        elif label in mapping and mapping[label] is not None:
            display, conf, note = mapping[label]
            conf_disp = {'high': '高', 'medium': '中（推定）', 'low': '低/待确认'}.get(conf, conf)
            note_escaped = note.replace('|', '\\|')
            lines.append(f'| `{label}` | {display} | {conf_disp} | {note_escaped} |')
        else:
            display = f'未识别标签（{label}）'
            conf_disp = '低/待确认'
            note_escaped = ''
            lines.append(f'| `{label}` | {display} | {conf_disp} | {note_escaped} |')
    lines.append('')
    
    # 对 part1 S04 做分段说明
    if name == '会议5-part1-asr':
        lines.append('### S04 分段细分')
        lines.append('')
        lines.append('| 片段索引区间 | 推定身份 | 置信度 | 依据 |')
        lines.append('| --- | --- | --- | --- |')
        for s, e, disp, conf, note in PART1_S04_RANGES:
            conf_disp = {'high': '高', 'medium': '中（推定）', 'low': '低/待确认'}.get(conf, conf)
            note_escaped = note.replace('|', '\\|')
            lines.append(f'| idx {s}–{e} | {disp} | {conf_disp} | {note_escaped} |')
        lines.append('')
    
    # 关键不确定点
    lines.append('## 主要不确定点')
    lines.append('')
    uncertain = []
    for label, val in mapping.items():
        if val is None:
            continue
        display, conf, note = val
        if conf in ('medium', 'low'):
            uncertain.append(f'- `{label}` → {display}（{conf}）：{note}')
    if name == '会议5-part1-asr':
        for s, e, disp, conf, note in PART1_S04_RANGES:
            if conf in ('medium', 'low'):
                uncertain.append(f'- S04 idx {s}–{e} → {disp}（{conf}）：{note}')
    if not uncertain:
        lines.append('本文件主要标签已对应到具体身份，无显著不确定点。')
    else:
        lines.extend(uncertain)
    lines.append('')
    
    # 对话正文
    lines.append('## 完整对话')
    lines.append('')
    lines.append('> 按原始顺序展示。每条发言一行；换人换行。')
    lines.append('> 格式：`[起始时间–结束时间] **说话人**（\`标签\`·置信度）：正文`')
    lines.append('')
    
    for seg in segs:
        lines.append(fmt_segment_dialogue(seg, name))
    
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return len(segs)


if __name__ == '__main__':
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
    for name, out_name in files:
        out_path = OUT_DIR / out_name
        n = write_dialogue_file(name, out_path)
        print(f'Generated {out_name}: {n} segments')
