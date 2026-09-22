"""ASR转写文件解析器
格式: [开始时间][标签]正文[结束时间][开始时间][标签]正文...
- 时间戳格式: 秒.毫秒 或 秒 (部分文件)
- 标签格式: S01 S02 S03 ...  或  S1 S2 ... 或 SP01 SP02
"""
import re
import json
import sys
from pathlib import Path

# 匹配: [开始秒数.毫秒][标签]正文 一直到下一个 [秒数] 或 [秒数.毫秒]
# 注意: 可能是 [0.03] 或 [12] 等
TIME_RE = re.compile(r'\[(\d+(?:\.\d+)?)\]')
LABEL_RE = re.compile(r'\[(S\d+|SP\d+)\]', re.IGNORECASE)

def parse_file(path):
    """解析转写文件，返回片段列表"""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 用正则找所有 [时间][标签]正文块
    # 模式: 寻找 [time][LABEL]，然后贪婪匹配正文直到下一个 [time][LABEL]
    pattern = re.compile(r'\[(\d+(?:\.\d+)?)\]\[(S\d+|SP\d+)\]', re.IGNORECASE)
    matches = list(pattern.finditer(text))
    
    segments = []
    for i, m in enumerate(matches):
        start_time = float(m.group(1))
        label = m.group(2).upper()
        text_start = m.end()
        if i + 1 < len(matches):
            # 到下一段开头为止
            next_start = matches[i + 1].start()
            content = text[text_start:next_start]
            # 段尾可能有个 [endtime] 在标签之前
            end_match = re.search(r'\[(\d+(?:\.\d+)?)\]\[(S\d+|SP\d+)\]', content, re.IGNORECASE)
            # 找最后一个 [time] 紧接 标签前的内容（这是段尾时间）
            # 由于 [time][label] 都是这种模式，需要找 [endtime] 这种单纯的时间标记
            # 在 content 中扫描 [time] 然后跟着的不是 label
            stripped = re.sub(r'\[(\d+(?:\.\d+)?)\]\[(S\d+|SP\d+)\]', '', content, flags=re.IGNORECASE)
        else:
            content = text[text_start:]
            stripped = content
        
        # 在 content 中尝试找出结束时间
        # 格式: 正文... [endtime] 下一个 [starttime][label]
        # 也就是 content 末尾可能有 [endtime]
        m_end = re.search(r'\[(\d+(?:\.\d+)?)\](?=\[|$)', stripped)
        if m_end:
            # 这就是段尾时间
            end_time = float(m_end.group(1))
            # 正文是 m_end之前
            body = stripped[:m_end.start()]
        else:
            end_time = None
            body = stripped
        
        # 清理正文：去除前后空白
        body = body.strip()
        # 去除开头的 [time] 可能误带
        body = re.sub(r'^\[\d+(?:\.\d+)?\]', '', body).strip()
        
        segments.append({
            'index': i,
            'start_time': start_time,
            'end_time': end_time,
            'label': label,
            'text': body
        })
    
    return segments

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: parse_asr.py <file.txt>")
        sys.exit(1)
    segs = parse_file(sys.argv[1])
    print(f"Parsed {len(segs)} segments")
    for s in segs[:5]:
        print(json.dumps(s, ensure_ascii=False))
    # 统计标签
    from collections import Counter
    c = Counter(s['label'] for s in segs)
    print("Label counts:", c)
