# 超聚变(xFusion)多维度情报系统 — 操作手册

> **版本**: 1.0  
> **适用对象**: 系统管理员、情报分析师  
> **前置要求**: Hermes Agent 已安装，GitHub 已认证

---

## 目录

1. [环境准备](#1-环境准备)
2. [一次性配置](#2-一次性配置)
3. [手动触发情报收集](#3-手动触发情报收集)
4. [配置定时任务](#4-配置定时任务)
5. [子领域深度报告](#5-子领域深度报告)
6. [推送配置](#6-推送配置)
7. [故障排查](#7-故障排查)
8. [新增监控方向](#8-新增监控方向)

---

## 1. 环境准备

### 1.1 检查 Hermes Agent

```bash
# 确认 Hermes 运行正常
hermes --version
```

### 1.2 检查 GitHub 认证

```bash
git config --global user.name
git config --global user.email
ssh -T git@github.com  # 应返回 "Hi xxx!"
```

### 1.3 检查技能是否已注册

```bash
# 加载技能
skill_view("xfusion-intelligence")
```

如果提示 "skill not found"，执行：

```bash
# 在 Hermes 对话中
skill_manage(action='create', name='xfusion-intelligence', content='...')
```

---

## 2. 一次性配置

### 2.1 飞书 Webhook

1. 在飞书群中添加「自定义机器人」
2. 获取 Webhook URL
3. 设置环境变量：

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY"
```

或在 `~/.hermes/.env` 中添加：
```
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY
```

### 2.2 邮件 SMTP

```bash
export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USER="xxx@xfusion.com"
export SMTP_PASS="your_app_password"
export EMAIL_TO="fangzhiheng@xfusion.com"
```

### 2.3 验证推送

```bash
# 本地预演飞书内容（不发送）
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-feishu.py \
  --text "测试消息：超聚变情报系统已就绪" \
  --dry-run

# 测试飞书真实发送
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-feishu.py \
  --text "测试消息：超聚变情报系统已就绪" \
  --webhook "$FEISHU_WEBHOOK_URL"

# 本地预演邮件内容（不发送）
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-email.py \
  --report ~/.hermes/workspace/intelligence-reports/xfusion-weekly/latest-xfusion-weekly.md \
  --subject "测试邮件" \
  --dry-run

# 测试邮件真实发送
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-email.py \
  --report ~/.hermes/workspace/intelligence-reports/xfusion-weekly/latest-xfusion-weekly.md \
  --subject "测试邮件" \
  --to "your@email.com"
```

---

## 3. 手动触发情报收集

### 3.1 在 Hermes 对话中

```
执行 xfusion-intelligence 技能，生成本周行业情报报告
```

或简化为：
```
超聚变周报
```

### 3.2 指定时间窗口

```
执行 xfusion-intelligence，周期 2026-06-20 至 2026-06-27
```

### 3.3 指定推送目标

```
执行 xfusion-intelligence，只推飞书不推邮件
```

---

## 4. 配置定时任务

### 4.1 周报定时（每周五 9:00）

在 Hermes 对话中：

```
创建一个 cron 任务：
- 名称：超聚变行业周报
- 时间：每周五早上9点
- 任务：执行 xfusion-intelligence 技能
- 推送：飞书 + 邮件
```

或直接调用：

```python
cronjob(
    action='create',
    name='超聚变行业周报',
    schedule='0 9 * * 5',
    prompt='执行 xfusion-intelligence 技能，生成本周行业情报报告。飞书推送精简版，邮件发送完整报告。',
    skills=['xfusion-intelligence']
)
```

### 4.2 子领域深度报告

```python
# 每月第1个周二：电源深度
cronjob(action='create', name='电源行业月度深度',
    schedule='0 10 1-7 * 2',
    prompt='执行 power-supply-deep 技能，生成电源行业月度深度报告',
    skills=['power-supply-deep'])

# 每月第1个周三：液冷深度
cronjob(action='create', name='液冷行业月度深度',
    schedule='0 10 1-7 * 3',
    prompt='执行 liquid-cooling-deep 技能',
    skills=['liquid-cooling-deep'])
```

### 4.3 查看已配置任务

```
列出所有 cron 任务
```

### 4.4 手动触发定时任务

```
立即执行「超聚变行业周报」任务
```

---

## 5. 子领域深度报告

### 5.1 触发方式

在 Hermes 对话中：
```
电源深度报告
液冷厂商动态
AI大模型情报
太空算力深度
人力资源情报
```

### 5.2 报告存储

```
~/.hermes/workspace/intelligence-reports/sub-domain/
├── power-supply/2026-W26-power-supply-deep.md
├── liquid-cooling/2026-W26-liquid-cooling-deep.md
├── ai-software/2026-W26-ai-software-deep.md
├── space-computing/2026-W26-space-computing-deep.md
└── hr-intelligence/2026-W26-hr-intelligence-deep.md
```

### 5.3 查看历史深度报告

```bash
ls -lt ~/.hermes/workspace/intelligence-reports/sub-domain/power-supply/
```

---

## 6. 推送配置

### 6.1 推送开关

| 场景 | 飞书 | 邮件 |
|------|------|------|
| 每周周报 | ✅ (精简版) | ✅ (完整版) |
| 月度深度 | ❌ | ✅ (完整版) |
| 紧急推送 | ✅ (即时) | ❌ |

### 6.2 自定义推送内容

```bash
# 从报告文件自动提取飞书摘要
python3 scripts/push-feishu.py --file report.md

# 预演飞书摘要，不发送
python3 scripts/push-feishu.py --file report.md --dry-run

# 直接推送自定义文本
python3 scripts/push-feishu.py --text "紧急：华为Ascend新芯片发布"

# 邮件推送
python3 scripts/push-email.py --report report.md --subject "主题" --to "xxx@xfusion.com"

# 预演邮件HTML，不发送
python3 scripts/push-email.py --report report.md --subject "主题" --dry-run
```

---

## 7. 故障排查

### 问题：子代理返回空内容

**症状**: `⚠️ No reply: the model returned empty content after retries`

**解决**: 
1. 如果是太空算力或人力资源方向 → 正常，这些方向新闻稀疏
2. 如果是电源或AI方向 → 切换到直接浏览器搜索：
   ```
   browser_navigate("https://news.google.com/search?q=...")
   ```

### 问题：飞书推送失败

**检查**:
```bash
echo $FEISHU_WEBHOOK_URL  # 确认已设置
curl -X POST "$FEISHU_WEBHOOK_URL" -H "Content-Type: application/json" -d '{"msg_type":"text","content":{"text":"测试"}}'
```

### 问题：邮件推送失败

**检查**:
- SMTP 配置是否正确
- 是否使用了应用专用密码（非登录密码）
- 端口是否正确（587 with TLS）

### 问题：报告未保存到正确路径

**检查**: 报告应在 `~/.hermes/workspace/intelligence-reports/xfusion-weekly/` 下

### 问题：Git 备份失败

```bash
# 检查备份目录
ls -la ~/.hermes-backup/
# 查看日志
cat ~/.hermes-backup/backup.log
```

---

## 8. 新增监控方向

### 步骤

1. **更新监控清单**: 编辑 `references/company-watchlist.md`
2. **创建子技能**: 复制 `sub-skills/<template>/`，修改 SKILL.md
3. **注册子技能**: `skill_manage(action='create', name='new-domain-deep', content='...')`
4. **添加代理定义**: 在 `SKILL.md` 中添加新代理
5. **更新模板**: 在 `templates/weekly-report-template.md` 中添加新章节
6. **测试**: 手动触发一次确认流程正常

---

*文档版本: 1.0 | 最后更新: 2026-06-27*
