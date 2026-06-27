#!/usr/bin/env python3
"""
飞书推送脚本 — 将精简版周报推送到飞书群机器人

使用方法:
  python3 push-feishu.py --text "推送内容" --webhook "$FEISHU_WEBHOOK_URL"
  python3 push-feishu.py --file report.md --webhook "$FEISHU_WEBHOOK_URL"  # 从文件自动提取摘要

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
        elif '🔵' in line and '电源' in line:
            in_section = 'power'
        elif '🟢' in line and ('AI' in line or '模型' in line):
            in_section = 'model'
        elif '🟡' in line:
            in_section = 'solution'
        elif '🔴' in line:
            in_section = 'space'
        elif '⚪' in line:
            in_section = 'hr'
        elif '📌' in line and '结论' in line:
            in_section = 'conclusion'
            continue
        elif in_section == 'conclusion' and line.strip().startswith(('1.', '2.', '3.')):
            conclusion += line.strip() + ' '
        elif in_section and line.strip().startswith(('- ', '• ', '1.', '2.')):
            signal = line.strip().lstrip('- •0123456789. ')
            signal = re.sub(r'\*\*', '', signal)
            signal = signal[:40]  # truncate per signal
            if in_section == 'power':
                power_signal = signal
            elif in_section == 'model':
                model_signal = signal
            elif in_section == 'solution':
                solution_signal = signal
            elif in_section == 'space':
                space_signal = signal
            elif in_section == 'hr':
                hr_signal = signal
        elif line.startswith('## ') and in_section:
            in_section = ""
    
    # 组装飞书文本
    parts = []
    if date_line:
        parts.append(date_line.replace('**', ''))
    if power_signal:
        parts.append(f"🔵 电源/液冷：{power_signal}")
    if model_signal:
        parts.append(f"🟢 AI模型：{model_signal}")
    if solution_signal:
        parts.append(f"🟡 AI方案：{solution_signal}")
    if space_signal:
        parts.append(f"🔴 太空算力：{space_signal}")
    if hr_signal:
        parts.append(f"⚪ 人才：{hr_signal}")
    if conclusion:
        parts.append(f"\n📌 {conclusion.strip()[:80]}")
    
    text = '\n'.join(parts)
    
    # 控制在 max_chars 以内
    if len(text) > max_chars:
        # 逐行截断
        truncated = []
        current_len = 0
        for line in text.split('\n'):
            if current_len + len(line) > max_chars - 10:
                break
            truncated.append(line)
            current_len += len(line) + 1
        text = '\n'.join(truncated) + '\n...'
    
    return text


def main():
    parser = argparse.ArgumentParser(description='飞书推送 — xFusion 行业周报')
    parser.add_argument('--text', help='直接推送文本')
    parser.add_argument('--file', help='从报告文件自动提取摘要')
    parser.add_argument('--webhook', help='飞书 Webhook URL（优先于环境变量）')
    parser.add_argument('--max-chars', type=int, default=200, help='最大字数 (默认200)')
    args = parser.parse_args()
    
    # 获取 Webhook URL
    webhook_url = args.webhook or os.environ.get('FEISHU_WEBHOOK_URL', '')
    if not webhook_url:
        print("[ERROR] 未配置飞书 Webhook URL。请设置 FEISHU_WEBHOOK_URL 环境变量或使用 --webhook 参数。")
        sys.exit(1)
    
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
    
    success = send_feishu_text(webhook_url, text)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
