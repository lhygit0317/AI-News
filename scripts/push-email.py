#!/usr/bin/env python3
"""
邮件推送脚本 — 将完整 Markdown 报告转为 HTML 邮件发送

使用方法:
  python3 push-email.py --report report.md --subject "超聚变行业周报 06.20-06.27" --to "xxx@xfusion.com"

环境变量:
  SMTP_HOST: SMTP 服务器地址
  SMTP_PORT: SMTP 端口 (默认 587)
  SMTP_USER: SMTP 用户名
  SMTP_PASS: SMTP 密码/应用密码
  EMAIL_FROM: 发件人地址 (默认 = SMTP_USER)
  EMAIL_TO: 默认收件人 (--to 参数优先)
"""

import argparse
import os
import re
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from pathlib import Path
from datetime import datetime


def markdown_to_html(md_text: str) -> str:
    """简单的 Markdown → HTML 转换（清除 emoji，保留基本格式）"""
    # 清除 emoji
    text = re.sub(r'[\U0001F000-\U0001FFFF\U00002600-\U000027BF\U0001FA00-\U0001FAFF]', '', md_text)
    
    lines = text.split('\n')
    html_lines = []
    in_table = False
    in_code = False
    
    for line in lines:
        # 代码块
        if line.strip().startswith('```'):
            in_code = not in_code
            if in_code:
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
            continue
        
        if in_code:
            html_lines.append(line)
            continue
        
        # 表格
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                html_lines.append('<table>')
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(c.replace('-', '') == '' for c in cells):
                continue  # 跳过分隔行
            tag = 'th' if in_table and not any('<' in l for l in html_lines[-1:] if '<td>' in l) else 'td'
            # Determine if first row should be headers
            is_header = '<th>' not in '\n'.join(html_lines[-5:]) and tag == 'td' and '<table>' in '\n'.join(html_lines[-3:])
            if is_header:
                tag = 'th'
            html_lines.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
            
            # 标题
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.startswith('> '):
                html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
            elif line.strip():
                # Bold conversion
                processed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                html_lines.append(f'<p>{processed}</p>')
            else:
                html_lines.append('<br>')
    
    if in_table:
        html_lines.append('</table>')
    
    return '\n'.join(html_lines)


def load_email_template(report_body_html: str, date_range: str, filename: str) -> str:
    """加载邮件模板并填充内容"""
    template_path = Path(__file__).parent.parent / 'templates' / 'email-template.html'
    if template_path.exists():
        template = template_path.read_text(encoding='utf-8')
    else:
        template = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"></head>
<body>
<h1>超聚变行业周报</h1>
<p>{date_range}</p>
{report_body_html}
</body>
</html>"""
    
    template = template.replace('{date_range}', date_range)
    template = template.replace('{timestamp}', datetime.now().strftime('%Y-%m-%d %H:%M'))
    template = template.replace('{filename}', filename)
    template = template.replace('{report_body_html}', report_body_html)
    
    return template


def send_email(smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str,
               from_addr: str, to_addr: str, subject: str, html_body: str) -> bool:
    """发送 HTML 邮件"""
    msg = MIMEMultipart('alternative')
    sender_name = os.environ.get('SENDER_NAME', '李红雨')
    msg['Subject'] = subject
    msg['From'] = formataddr([sender_name, from_addr])
    msg['To'] = to_addr
    
    # 同时提供纯文本和 HTML
    text_body = re.sub(r'<[^>]+>', '', html_body)
    msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        with server:
            if smtp_port != 465:
                server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_addr, [to_addr], msg.as_string())
        print(f"[OK] 邮件发送成功: {to_addr}")
        return True
    except Exception as e:
        print(f"[ERROR] 邮件发送失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='邮件推送 — xFusion 行业周报')
    parser.add_argument('--report', required=True, help='Markdown 报告文件路径')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--to', help='收件人地址')
    parser.add_argument('--smtp-host', help='SMTP 服务器')
    parser.add_argument('--smtp-port', type=int, default=587, help='SMTP 端口')
    parser.add_argument('--smtp-user', help='SMTP 用户名')
    parser.add_argument('--smtp-pass', help='SMTP 密码')
    args = parser.parse_args()
    
    # 获取配置
    smtp_host = args.smtp_host or os.environ.get('SMTP_HOST', '')
    smtp_port = args.smtp_port or int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = args.smtp_user or os.environ.get('SMTP_USER', '')
    smtp_pass = args.smtp_pass or os.environ.get('SMTP_PASS', '')
    from_addr = os.environ.get('EMAIL_FROM', smtp_user)
    to_addr = args.to or os.environ.get('EMAIL_TO', '')
    
    if not smtp_host or not smtp_user or not smtp_pass:
        print("[ERROR] SMTP 配置不完整。请设置环境变量: SMTP_HOST, SMTP_USER, SMTP_PASS")
        sys.exit(1)
    
    if not to_addr:
        print("[ERROR] 未指定收件人。请使用 --to 参数或设置 EMAIL_TO 环境变量。")
        sys.exit(1)
    
    # 读取报告
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"[ERROR] 报告文件不存在: {args.report}")
        sys.exit(1)
    
    report_md = report_path.read_text(encoding='utf-8')
    
    # 提取日期范围
    date_match = re.search(r'周期：(.+?) 至 (.+?)\*', report_md)
    if date_match:
        date_range = f"{date_match.group(1)} - {date_match.group(2)}"
    else:
        date_range = args.subject
    
    # Markdown → HTML
    report_html = markdown_to_html(report_md)
    
    # 加载模板
    full_html = load_email_template(report_html, date_range, report_path.name)
    
    # 发送
    print(f"发送邮件: {args.subject}")
    print(f"  收件人: {to_addr}")
    print(f"  报告: {report_path.name}")
    
    success = send_email(smtp_host, smtp_port, smtp_user, smtp_pass,
                         from_addr, to_addr, args.subject, full_html)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
