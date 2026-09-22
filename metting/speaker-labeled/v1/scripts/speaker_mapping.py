"""说话人映射与标注版生成器（增强版）"""
import json
from pathlib import Path
from collections import Counter, defaultdict

def load_segments(name):
    p = Path(f'/home/pine/workspace/erp/metting/speaker-labeled/v1/parsed/{name}.segments.json')
    return json.loads(p.read_text(encoding='utf-8'))

# 各文件的标签-身份映射
MAPPINGS = {
    '会议1-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', 'S03 称为"老板"，主持介绍公司情况、双公司结算、ERP定位等'),
        'S02': ('Pine（ERP开发方；被S01称为"沈老师"）', 'high', '用户自报；S01多次称"沈老师"，不据此推定Pine真实姓名'),
        'S03': ('小叶/沈歪歪（客户方助理/新同事）', 'high', 'S01 介绍"我们公司的同事，他未来可能对这个会有一定的对接"；S01 喊"小叶"；detail 称为"沈歪歪"；用户确认小叶 = 沈歪歪'),
    },
    '会议2-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '与会议1同一津金；detail 中亦称 AusUS；自报"我们这边"，描述学校业务流程'),
        'S02': ('Pine（ERP开发方）', 'high', '用户自报；延续会议1标签对应'),
    },
    '会议3-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '与会议1-2同一津金；idx=483 S02 收尾时称"沈老师"指对方'),
        'S02': ('Pine（ERP开发方）', 'high', '用户自报；延续会议1-2对应'),
    },
    '会议4-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '现场带看工厂并介绍夏经理；与会议1-3同一津金（AusUS）'),
        'S02': ('Pine（ERP开发方）', 'high', '用户自报；延续会议1-3对应'),
    },
    '会议5-part1-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '在工厂现场带看介绍人员；idx=1 "我我去修机器去" 显示是老板；用户确认津金 = AusUS'),
        'S02': ('Pine（ERP开发方；被S01称为"沈老师"）', 'high', '用户自报；S01 idx=53 介绍"沈老师，是负责咱们ERP工程的"'),
        'S03': ('杜文颖（客户方工艺/协调）', 'high', 'S02 idx=67 喊"杜老师"；S03 idx=70 自报"是设计"；idx=144 提及"设计那人"；idx=326 提及"会计老师"'),
        # S04 标签在不同时间窗对应不同人
        # 用区间判断: idx<142 => 王师傅/可能装订组长；142<=idx<=1287 => 夏经理；>1287 => 配送员/夏经理
        'S04': None,  # 标记为需要特殊处理
        'S05': ('夏经理（客户方生产经理）', 'high', 'idx=338-341 S02喊"夏经理" S05回应；内容关于传票、台账、折算、定价'),
    },
    '会议5-part2-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '延续会议5同一津金（AusUS）；idx=210 S02 提"周金华"，S01 复述"财务周老师"；idx=222 提"等周老师回来"'),
        'S02': ('Pine（ERP开发方）', 'high', '用户自报；延续会议1-4对应'),
        'S03': ('会议5-part2-S03（身份待确认；用户表示无法确认）', 'low', '仅1段"三五和八小，不是四小"（idx=105）；用户表示无法确认该发言归属；保持未识别状态'),
        'S04': ('杜文颖（客户方工艺/协调）', 'high', 'idx=203 S01喊"杜老师啊"，S04 回应；idx=365 S04 说"财务老师刚回来"（协调人）；idx=372 S01 又喊"杜老师"'),
        'S05': ('周老师/周会计（客户方财务；周金华）', 'high', 'idx=371 开始大量发言；idx=371 "哎，你好，老师"（与Pine/老板打招呼）；idx=386+ 谈采购/发票等财务内容；用户确认财务周老师=周金华，且会议中仅此一位周老师'),
    },
    '会议5-part3-asr': {
        'S01': ('津金（客户方负责人；公司名亦称津金，AusUS 为同一人）', 'high', '延续会议5同一津金（AusUS）'),
        'S02': ('Pine（ERP开发方）', 'high', '用户自报；idx=357 多次喊"周老师"'),
        'S03': ('周老师/周会计（客户方财务；周金华）', 'high', 'idx=358 S03 回应 Pine 的"问不出来吗？"——是周老师；idx=145 简短回应；idx=378 "对"；与part2 S05 为同一人'),
        'S04': ('杜文颖（客户方工艺/协调）', 'high', 'idx=360 "我这边没什么呀，主要是传稿"；idx=366 "对，我这边也没啥"——与part2 S04 一致'),
    },
    '会议6-驻点高老师-asr': {
        'S01': ('Pine（ERP开发方）', 'high', 'idx=0 "喂喂"，idx=2 "诶，高老师"；与会议1-5同一Pine，但标签号反转（电话主呼方）'),
        'S02': ('高老师（客户方驻点；六九中学一部）', 'high', 'idx=3 回应"你好，你说"；idx=7 "我这是负责初中部"；idx=12 "六九中学三部，我是一部的"；idx=26 描述驻点日常工作'),
    },
}

# 会议5-part1 的 S04 区间细分
# S04 实际 idx 范围: 114-312
# 早期（114-127）被 S03 idx=113 喊"王姐"，是王师傅/王姐
# 后期（143-312）大量回答生产/合同/计价/油墨/配送等问题，属夏经理
PART1_S04_RANGES = [
    # (start_idx, end_idx, 显示名称, 置信度, 备注)
    (110, 130, '王师傅/王姐（客户方打包复印装订）', 'medium', 'S03 idx=113 喊"王姐"，S04 回应工艺流程（印刷完裁切打包装订）；idx=114-127 王师傅继续补充；用户未确认是否为王师傅'),
    (143, 312, '夏经理（客户方生产经理）', 'medium', 'idx=143 起回答算价、石化总厂合同、传票业务范围、油墨、散客复印费、双面/单面计件、工作量、返工、配送等大量生产/合同问题；用户未确认是否为夏经理'),
]

def get_part1_s04(idx):
    for s, e, disp, conf, note in PART1_S04_RANGES:
        if s <= idx <= e:
            return disp, conf, note
    return 'S04（边界待确认：王师傅/夏经理）', 'low', 'S04 标签在不同区间对应不同身份，需以音频/上下文细分'

def fmt_segment(seg, file_prefix, mapping):
    label = seg['label']
    idx = seg['index']
    
    if file_prefix == '会议5-part1-asr' and label == 'S04':
        display, conf, note = get_part1_s04(idx)
    elif label in mapping and mapping[label] is not None:
        display, conf, note = mapping[label]
    else:
        display = f'未识别标签（{label}；身份待确认）'
        conf = 'low'
        note = ''
    
    idx_str = f'{file_prefix}-{idx:04d}'
    start = seg['start_time']
    end = seg['end_time']
    end_str = '?' if end is None else f'{end:.2f}'
    time_str = f'{start:.2f}–{end_str}'
    
    confidence_map = {'high': '高置信度', 'medium': '中置信度（推定）', 'low': '低置信度/待确认'}
    conf_label = confidence_map.get(conf, conf)
    
    text = seg['text']
    
    lines = []
    lines.append(f'### [{idx_str}] [{time_str}]')
    lines.append(f'**{display}**（原始标签：`{label}`；本段归属：{conf_label}）')
    if note:
        lines.append(f'> 标注依据/备注：{note}')
    lines.append('')
    lines.append(text)
    lines.append('')
    return '\n'.join(lines)


def write_labeled_file(name, output_path):
    segs = load_segments(name)
    mapping = MAPPINGS[name]
    
    lines = []
    lines.append(f'# 会议：{name}')
    lines.append('')
    
    # 统计信息
    label_counts = Counter(s['label'] for s in segs)
    lines.append('## 说话人映射（本文件）')
    lines.append('')
    lines.append('| 原始标签 | 规范身份 | 置信度 | 备注 |')
    lines.append('| --- | --- | --- | --- |')
    for label in sorted(label_counts.keys()):
        if file_is_part1 := (name == '会议5-part1-asr' and label == 'S04'):
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
    
    # 完整对话
    lines.append('## 完整对话（按原始顺序）')
    lines.append('')
    lines.append('> 本节完整保留原始正文、原始标签与时间，未对内容进行润色或业务补写。')
    lines.append('')
    
    for seg in segs:
        lines.append(fmt_segment(seg, name, mapping))
    
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return len(segs)


if __name__ == '__main__':
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
    for name, out_name in files:
        out_path = OUT_DIR / out_name
        n = write_labeled_file(name, out_path)
        print(f'Generated {out_name}: {n} segments')
