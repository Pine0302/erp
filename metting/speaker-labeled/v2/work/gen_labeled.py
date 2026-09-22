#!/usr/bin/env python3
"""生成 v2 说话人标注版（对话式格式）+ 完整性核验。

标注版格式（用户要求）：对话式，每段一行"说话人：正文"，换人即换行。
同时保留片段编号/时间/原始标签/置信度于行内注释前缀，保证可追溯。

每行格式：
[会议1-0001] [0.03–2.25] 津金（高置信度｜原始标签：S01）：正文……

例外/待确认段：
[会议5-part2-0106] [时间] 会议5-part2-S03（身份待确认｜原始标签：S03）：正文……

连续同人发言不合并（保留原始片段边界），仅按原始顺序逐段输出。
"""
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
V2 = WORK.parent
SRC = V2.parents[1] / 'transcripts'

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

OUT_NAMES = {
    "会议1": "会议1-说话人标注版.md",
    "会议2": "会议2-说话人标注版.md",
    "会议3": "会议3-说话人标注版.md",
    "会议4": "会议4-说话人标注版.md",
    "会议5-part1": "会议5-part1-说话人标注版.md",
    "会议5-part2": "会议5-part2-说话人标注版.md",
    "会议5-part3": "会议5-part3-说话人标注版.md",
    "会议6": "会议6-驻点高老师-说话人标注版.md",
}

# ---- 会议1 映射（本次主会话直接分析，高置信度） ----
M1 = {
    "S01": ("津金", "高", "S01 主持介绍公司情况、双公司结算、ERP定位；S03 称其为『老板』；detail 全程对应 AusUS"),
    "S02": ("Pine", "高", "被 S01 称『沈老师』并负责投屏、记录、系统方案（detail 归属 Pine）"),
    "S03": ("小叶（即沈歪歪，用户已确认同一人）", "高", "S01 介绍『我们公司的同事』并被称『小叶』；detail 称『沈歪歪』；用户已确认小叶=沈歪歪"),
}

def load_mapping(prefix):
    """加载该文件的标签→(显示名, 置信度类别) 映射及例外段。"""
    if prefix == "会议1":
        mapping = {lab: (name, conf, ev) for lab, (name, conf, ev) in M1.items()}
        exceptions = {}   # 会议1无例外
        return mapping, exceptions
    key = "会议5" if prefix.startswith("会议5") else prefix
    d = json.load(open(WORK / f"{key}-speaker-analysis.json", encoding='utf-8'))
    mapping = {}
    exceptions = {}
    if key == "会议5":
        part = "part" + prefix.split("part")[1]
        for m in d["label_mapping"][part]:
            conf = m["confidence"]
            name = m["speaker"]
            # 显示名简化：去掉括号内长说明（说明保留在映射文件中）
            short = name.split("（")[0].split("(")[0]
            mapping[m["label"]] = (short, conf, name)
        # 特殊标注
        for lab, (short, conf, full) in list(mapping.items()):
            if "待确认" in short:
                mapping[lab] = (f"{prefix}-{lab}（身份待确认）", "低", full)
    else:
        for m in d["label_mapping"]:
            name = m["speaker"]
            short = name.split("（")[0].split("(")[0]
            mapping[m["label"]] = (short, m["confidence"], name)
    # 例外段（uid 精确或含中文顿号列表）；只保留属于本文件的 uid
    for e in d.get("exceptions", []):
        uids_field = e.get("uid", "")
        for uid in parse_uids(uids_field, prefix, key):
            if uid.startswith(prefix + "-"):
                exceptions[uid] = e
    return mapping, exceptions

def parse_uids(uids_field, prefix, key):
    """把 exceptions 的 uid 字段解析成完整 uid 列表。

    字段可能是 "会议5-part1-0013、0021、0023"（带前缀+裸序号混排）、
    "会议5-part3-0132" 单个，或裸序号 "0021"。裸序号只有当例外条目
    以完整 uid 开头时才视为该前缀的序号。
    """
    out = []
    if not uids_field:
        return out
    # 先切分
    raw = [t.strip() for t in uids_field.replace("，", "、").replace("~", "、").split("、") if t.strip()]
    # 确定"当前前缀"：字段中出现的第一个完整 uid 的前缀
    cur_prefix = prefix
    for t in raw:
        if t.startswith("会议"):
            cur_prefix = t.rsplit("-", 1)[0] if t.rsplit("-", 1)[-1].isdigit() else t
            break
    for t in raw:
        if t.startswith("会议"):
            # 完整 uid（可能被 ~ 切开）：补全为 4 位
            head, num = t.rsplit("-", 1)
            if num.isdigit():
                out.append(f"{head}-{int(num):04d}")
            else:
                out.append(t)
        elif t.isdigit():
            out.append(f"{cur_prefix}-{int(t):04d}")
        # 其他形态忽略（无有效序号）
    return out

def conf_cat(conf):
    """置信度→片段归属类别：①高置信度 ②推定 ③待确认"""
    if conf == "高":
        return "①高置信度归属"
    if conf == "中":
        return "②推定归属"
    return "③身份待确认"

def fmt_time(s, e):
    return f"{s}–{e}" if e is not None else f"{s}–(无结束时间)"

def main():
    stats = {}
    for prefix, fname in FILES:
        segs = [json.loads(l) for l in open(WORK / f"{prefix}-segments.jsonl", encoding='utf-8')]
        mapping, exceptions = load_mapping(prefix)
        rep = json.load(open(WORK / f"{prefix}-parse-report.json", encoding='utf-8'))

        lines = []
        lines.append(f"# {prefix} 说话人标注版（v2）\n")
        lines.append(f"> 源文件：`transcripts/{fname}`；片段数 {len(segs)}；"
                     f"本版为基于文本、背景和会议总结的说话人归属初稿，供 Pine 复核。\n")
        lines.append("## 本文件人物映射\n")
        lines.append("| 原始标签 | 规范身份 | 身份置信度 | 依据摘要 |")
        lines.append("| --- | --- | --- | --- |")
        for lab in sorted(mapping):
            short, conf, full = mapping[lab]
            ev = full if "（" in full or "(" in full else short
            # 依据摘要：full 里括号内的内容即说明
            lines.append(f"| `{lab}` | {short} | {conf} | {full} |")
        lines.append("")
        if exceptions:
            lines.append("## 局部例外（偏离默认映射的片段）\n")
            for uid in sorted(exceptions):
                e = exceptions[uid]
                lines.append(f"- `{uid}`：{e.get('speaker','')}（{e.get('confidence','')}）—— {e.get('note','')}")
            lines.append("")
        lines.append("## 完整对话（按原始顺序，对话式）\n")
        lines.append("> 每段一行：`[片段编号] [起止时间] 说话人（归属置信度｜原始标签）：原文`。")
        lines.append("> 原文未做任何润色、纠错或补写；例外段说明以〔例外段：…〕形式附在行尾，不改动正文。\n")

        # 解析残余与文件末尾截断说明
        if rep.get("residues"):
            for r in rep["residues"]:
                lines.append(f"〔解析残余：源文件字符位置 {r['pos']}，内容 `{r['text']}` —— "
                             f"非完整片段（源文件末尾截断的时间戳残留），已在解析报告中保留，未生成片段〕")
            lines.append("")
        tail = segs[-1]
        if tail["end"] is None or (tail["text"] and tail["text"].rstrip().endswith("[")
                                    and tail["text"].rstrip()[-6:].split(".")[0][1:].isdigit()):
            lines.append(f"〔注：源文件在最后片段 {tail['uid']}（{tail['start']}秒起）处中断，"
                         f"其正文尾部的时间戳片段为源文件截断残留，原样保留〕\n")

        cat_count = {"①高置信度归属": 0, "②推定归属": 0, "③身份待确认": 0, "④疑似多人": 0}
        for i, s in enumerate(segs, 1):
            uid = s["uid"]
            lab = s["label"]
            if lab in mapping:
                short, conf, full = mapping[lab]
            else:
                short, conf, full = f"{prefix}-{lab}（身份待确认）", "低", "未知标签"
            note = ""
            cat = conf_cat(conf)
            if uid in exceptions:
                e = exceptions[uid]
                spk = e.get("speaker", "")
                if "待确认" in spk or "错分" in spk:
                    disp = spk
                    cat = "③身份待确认"
                elif "疑" in spk or "被介绍" in spk:
                    disp = spk
                    cat = "③身份待确认"
                else:
                    disp = spk
                    cat = "②推定归属" if e.get("confidence") in ("中", "低") else "①高置信度归属"
                note = f"〔例外段：{e.get('note','')}〕"
            else:
                disp = short
            cat_count[cat] += 1
            t = s["text"].rstrip()
            tdisp = t if t else "（空）"
            lines.append(f"[{uid}] [{fmt_time(s['start'], s['end'])}] **{disp}**（{cat}｜原始标签：{lab}）：{tdisp}{note}")

        out = V2 / OUT_NAMES[prefix]
        out.write_text("\n".join(lines) + "\n", encoding='utf-8')
        stats[prefix] = {
            "n_segments": len(segs), "cats": cat_count,
            "sum_ok": rep["check_sum_ok"], "residues": rep["n_residues"],
        }
        print(f"{prefix}: {len(segs)} 段 -> {out.name}; 分类 {cat_count}")

    json.dump(stats, open(WORK / "gen-stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 校验四类之和 == 片段总数
    for p, st in stats.items():
        assert sum(st["cats"].values()) == st["n_segments"], f"{p} 分类之和 != 片段总数"
    print("分类互斥校验通过（四类之和 == 片段总数）")

if __name__ == "__main__":
    main()
