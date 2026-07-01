#!/usr/bin/env python3
"""
飞书推送脚本 — 将精简版周报推送到飞书群机器人

使用方法:
  python3 push-feishu.py --text "推送内容" --webhook "$FEISHU_WEBHOOK_URL"
  python3 push-feishu.py --file report.md --webhook "$FEISHU_WEBHOOK_URL"  # 从文件自动提取摘要
  python3 push-feishu.py --file report.md --dry-run  # 只预览，不发送

环境变量（优先级低于 --webhook 参数）:
  FEISHU_WEBHOOK_URL: 飞书机器人 Webhook 地址
"""

import argparse
import json
import os
import sys
import re
import urllib.request
from pathlib import Path


EMOJI_RE = re.compile(r'[\U0001F000-\U0001FFFF\U00002600-\U000027BF\U0001FA00-\U0001FAFF]')


def clean_signal_text(text: str, max_len: int = 48) -> str:
    """Normalize a report bullet/table cell into one compact Feishu line."""
    text = text.strip()
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'^\s*(?:[-*•]|\d+[.)])\s+', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^\s*(?:' + EMOJI_RE.pattern + r'|\[[^\]]+\])[\s:：-]*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]


def shorten_text(text: str, max_len: int) -> str:
    if max_len <= 0 or not text:
        return ''
    if len(text) <= max_len:
        return text
    if max_len <= 3:
        return text[:max_len]
    return text[:max_len - 3] + '...'


def section_from_heading(line: str) -> str:
    """Return the logical report section for a Markdown heading."""
    if not line.startswith('## '):
        return ''
    if '电源' in line or '液冷' in line:
        return 'power'
    if 'AI大模型' in line or '模型' in line:
        return 'model'
    if 'AI基础设施' in line or 'AI方案' in line:
        return 'solution'
    if '太空算力' in line:
        return 'space'
    if '人力资源' in line or '人才' in line:
        return 'hr'
    if '核心结论' in line or '结论' in line:
        return 'conclusion'
    return ''


def table_signal_for_section(section: str, line: str) -> str:
    """Extract a concise signal from the first data row in a Markdown table."""
    if not line.strip().startswith('|'):
        return ''
    cells = [clean_signal_text(cell, 80) for cell in line.strip().strip('|').split('|')]
    cells = [cell for cell in cells if cell]
    if len(cells) < 2:
        return ''
    if any(set(cell) <= {'-'} for cell in cells):
        return ''
    if cells[0] in {'企业', '模型厂商', '方向', '信号', '竞品'}:
        return ''

    if section == 'power' and len(cells) >= 3:
        return clean_signal_text(f"{cells[0]}：{cells[2]}")
    if section == 'model':
        return clean_signal_text(f"{cells[0]}：{cells[1]}")
    if section == 'solution':
        return clean_signal_text(f"{cells[0]}：{cells[1]}")
    if section == 'space':
        return clean_signal_text(f"{cells[0]}：{cells[1]}")
    if section == 'hr':
        return clean_signal_text(f"{cells[0]}：{cells[1]}")
    return ''


def send_feishu_text(webhook_url: str, text: str) -> bool:
    """发送飞书文本消息"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get('code') == 0:
                print(f"[OK] 飞书推送成功: {result.get('msg', 'ok')}")
                return True
            else:
                print(f"[FAIL] 飞书推送失败: code={result.get('code')}, msg={result.get('msg')}")
                return False
    except Exception as e:
        print(f"[ERROR] 飞书推送异常: {e}")
        return False


def extract_summary_from_report(filepath: str, max_chars: int = 200) -> str:
    """从报告 Markdown 中提取摘要文本"""
    content = Path(filepath).read_text(encoding='utf-8')
    
    # 提取周报标题行
    lines = content.split('\n')
    date_line = ""
    power_signal = ""
    model_signal = ""
    solution_signal = ""
    space_signal = ""
    hr_signal = ""
    conclusion = ""
    
    in_section = ""
    for line in lines:
        if '周期' in line and '**' in line:
            date_line = line.strip('* ')
        elif line.startswith('## '):
            in_section = section_from_heading(line)
            continue
        elif in_section == 'conclusion' and line.strip().startswith(('1.', '2.', '3.')):
            conclusion += clean_signal_text(line, 80) + ' '
        elif in_section and line.strip().startswith(('- ', '• ', '1.', '2.')):
            signal = clean_signal_text(line)
            if in_section == 'power' and not power_signal:
                power_signal = signal
            elif in_section == 'model' and not model_signal:
                model_signal = signal
            elif in_section == 'solution' and not solution_signal:
                solution_signal = signal
            elif in_section == 'space' and not space_signal:
                space_signal = signal
            elif in_section == 'hr' and not hr_signal:
                hr_signal = signal
        elif in_section in {'power', 'model', 'solution', 'space', 'hr'}:
            signal = table_signal_for_section(in_section, line)
            if in_section == 'power' and signal and not power_signal:
                power_signal = signal
            elif in_section == 'model' and signal and not model_signal:
                model_signal = signal
            elif in_section == 'solution' and signal and not solution_signal:
                solution_signal = signal
            elif in_section == 'space' and signal and not space_signal:
                space_signal = signal
            elif in_section == 'hr' and signal and not hr_signal:
                hr_signal = signal
    
    # 组装飞书文本
    def build_text(signal_len: int = 48, conclusion_len: int = 80) -> str:
        parts = []
        if date_line:
            parts.append(date_line.replace('**', ''))
        if power_signal:
            parts.append(f"🔵 电源/液冷：{shorten_text(power_signal, signal_len)}")
        if model_signal:
            parts.append(f"🟢 AI模型：{shorten_text(model_signal, signal_len)}")
        if solution_signal:
            parts.append(f"🟡 AI方案：{shorten_text(solution_signal, signal_len)}")
        if space_signal:
            parts.append(f"🔴 太空算力：{shorten_text(space_signal, signal_len)}")
        if hr_signal:
            parts.append(f"⚪ 人才：{shorten_text(hr_signal, signal_len)}")
        if conclusion_len and conclusion:
            parts.append(f"\n📌 {shorten_text(conclusion.strip(), conclusion_len)}")
        return '\n'.join(parts)

    text = build_text()
    
    # 控制在 max_chars 以内
    if len(text) > max_chars:
        for signal_len, conclusion_len in ((28, 40), (22, 30), (18, 20), (14, 0), (10, 0)):
            text = build_text(signal_len, conclusion_len)
            if len(text) <= max_chars:
                break
        if len(text) > max_chars:
            text = text[:max_chars - 3] + '...'
    
    return text


def main():
    parser = argparse.ArgumentParser(description='飞书推送 — xFusion 行业周报')
    parser.add_argument('--text', help='直接推送文本')
    parser.add_argument('--file', help='从报告文件自动提取摘要')
    parser.add_argument('--webhook', help='飞书 Webhook URL（优先于环境变量）')
    parser.add_argument('--max-chars', type=int, default=200, help='最大字数 (默认200)')
    parser.add_argument('--dry-run', action='store_true', help='只生成并打印推送内容，不发送到飞书')
    args = parser.parse_args()

    # 获取推送文本
    if args.text:
        text = args.text
    elif args.file:
        text = extract_summary_from_report(args.file, args.max_chars)
        if not text.strip():
            print("[ERROR] 无法从报告中提取摘要，请检查文件格式或使用 --text 直接指定。")
            sys.exit(1)
    else:
        print("[ERROR] 请使用 --text 或 --file 指定推送内容。")
        sys.exit(1)
    
    print(f"推送内容 ({len(text)} 字):")
    print(text)
    print("---")

    if args.dry_run:
        print("[DRY-RUN] 飞书推送内容已生成，未发送。")
        sys.exit(0)

    # 获取 Webhook URL
    webhook_url = args.webhook or os.environ.get('FEISHU_WEBHOOK_URL', '')
    if not webhook_url:
        print("[ERROR] 未配置飞书 Webhook URL。请设置 FEISHU_WEBHOOK_URL 环境变量或使用 --webhook 参数。")
        sys.exit(1)
    
    success = send_feishu_text(webhook_url, text)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
