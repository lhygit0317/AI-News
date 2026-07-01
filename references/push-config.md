# 推送配置

## 飞书推送

### 环境变量
```bash
FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_KEY"
```

### 推送格式
- **字数限制**: 200字以内（含标点）
- **格式**: 纯文本 + 链接
- **包含**: 5大方向各1-2条核心 + 本周结论 + 完整报告链接
- **预演**: `python3 scripts/push-feishu.py --file report.md --dry-run`

### 模板
```
【超聚变行业周报 {日期}】
🔵 电源/液冷：{核心事件}
🟢 AI模型：{核心事件}
🟡 AI方案：{核心事件}
🔴 太空算力：{核心事件}
⚪ 人才：{核心事件}
📌 核心结论：{一句话}
🔗 详情：{报告链接}
```

---

## 邮件推送

### 环境变量
```bash
SMTP_HOST="smtp.example.com"
SMTP_PORT="587"
SMTP_USER="xxx@xfusion.com"
SMTP_PASS="your_app_password"
EMAIL_FROM="hermes-agent@xfusion.com"
EMAIL_TO="fangzhiheng@xfusion.com"
```

### 推送格式
- **主题**: `超聚变行业周报 YYYY.MM.DD - YYYY.MM.DD`
- **正文**: HTML 格式完整报告
- **附件**: 可选 Markdown 原文

### 注意事项
- Gmail/企业邮箱需要应用专用密码
- HTML邮件需清除emoji（不支持彩色emoji）
- 飞书和邮件推送可独立开关
- 本地验证可先运行 `python3 scripts/push-email.py --report report.md --subject "测试" --dry-run`

---

## 推送开关配置

在技能执行时可通过参数控制：
- `--push-feishu` : 启用飞书推送
- `--push-email` : 启用邮件推送
- `--push-all` : 启用全部推送
- 默认: 仅生成本地报告，不推送
