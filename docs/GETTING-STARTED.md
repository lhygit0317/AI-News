# 超聚变(xFusion)多维度情报系统 — 新人上手指南

> **目标读者**: 从未接触过 Hermes Agent 的新人  
> **预计时间**: 30 分钟完成搭建  
> **最终效果**: 每周自动收集五大维度行业情报，飞书+邮件双通道推送

---

## 🎯 你将获得什么

完成本指南后，你将拥有：

- ✅ 一台 24/7 运行的 AI 情报收集助手
- ✅ 每周自动回收的超聚变行业周报
- ✅ 飞书上收到 200 字精简推送 + 完整报告链接
- ✅ 邮件收到完整 HTML 格式报告
- ✅ 支持一键生成任意子领域的深度报告

---

## 📋 前提条件检查清单

在开始之前，确认以下都已就绪：

- [ ] **Hermes Agent 已安装并运行**（桌面版或 CLI）
- [ ] **GitHub 账号已认证**（在 Hermes 中可以说 `gh auth status` 并成功）
- [ ] **飞书群机器人 Webhook URL**（从飞书群设置中获取）
- [ ] **邮箱 SMTP 配置**（发件邮箱的服务器地址、端口、用户名、密码）

---

## 🚀 第一步：部署技能文件（5分钟）

### 1.1 确认技能文件已就位

在 Hermes 对话中输入：
```
skill_view("xfusion-intelligence")
```

如果返回技能内容 → 跳到第二步。

如果提示 "not found" → 说明技能文件尚未部署。请联系管理员获取 `xfusion-intelligence` 技能文件夹，放入：
```
~/.hermes/skills/xfusion-intelligence/
```

文件夹结构应为：
```
xfusion-intelligence/
├── SKILL.md
├── references/
│   ├── company-watchlist.md
│   ├── news-sources.md
│   ├── rss-sources.md
│   └── push-config.md
├── sub-skills/
│   ├── power-supply-deep/SKILL.md
│   ├── liquid-cooling-deep/SKILL.md
│   ├── ai-software-deep/SKILL.md
│   ├── space-computing-deep/SKILL.md
│   └── hr-intelligence-deep/SKILL.md
├── templates/
│   ├── weekly-report-template.md
│   ├── sub-domain-report-template.md
│   ├── feishu-push-template.md
│   └── email-template.html
├── scripts/
│   ├── push-feishu.py
│   ├── push-email.py
│   └── backup.sh
└── docs/
    ├── ARCHITECTURE.md
    ├── OPERATIONS.md
    └── GETTING-STARTED.md (本文件)
```

---

## 🔧 第二步：配置推送通道（5分钟）

### 2.1 配置飞书推送

在 Hermes 对话中设置环境变量：
```
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY_HERE"
```

> 📌 如何获取飞书 Webhook URL：
> 1. 打开飞书电脑版
> 2. 进入目标群聊 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
> 3. 复制 Webhook 地址

### 2.2 配置邮件推送

```
export SMTP_HOST="smtp.qiye.aliyun.com"      # 企业邮箱SMTP地址
export SMTP_PORT="587"
export SMTP_USER="yourname@xfusion.com"       # 你的邮箱
export SMTP_PASS="your_app_password"          # 邮箱应用密码(非登录密码)
export EMAIL_TO="fangzhiheng@xfusion.com"     # 报告接收人
```

> 📌 如何获取应用密码：
> - **阿里企业邮箱**: 设置 → 客户端授权密码 → 生成新密码
> - **Gmail**: 账号安全 → 两步验证 → 应用专用密码
> - **腾讯企业邮箱**: 设置 → 微信安全登录 → 客户端专用密码

### 2.3 测试推送是否正常

在 Hermes 对话中：
```
测试飞书推送："超聚变情报系统搭建完成！"
```

如果收到飞书消息 → ✅ 配置成功

---

## 🎮 第三步：首次手动执行（10分钟）

### 3.1 生成第一份周报

在 Hermes 对话中输入：
```
执行 xfusion-intelligence 技能，生成本周行业情报
```

Hermes 会自动：
1. 读取历史报告（如果有）
2. 并行启动 5 个代理搜索新闻
3. 合并结果生成报告
4. 推送飞书精简版
5. 发送邮件完整版

**预计耗时**: 5-10 分钟（取决于网络和搜索量）

### 3.2 查看生成的报告

```
查看最新周报
```

或直接在文件夹中打开：
```
~/.hermes/workspace/intelligence-reports/xfusion-weekly/latest-xfusion-weekly.md
```

### 3.3 验证推送

- ✅ 飞书群收到了 200 字精简推送
- ✅ 邮箱收到了完整 HTML 报告

---

## ⏰ 第四步：设置每周自动执行（5分钟）

### 4.1 创建定时任务

在 Hermes 对话中：
```
创建一个每周一早上9点执行的定时任务：
- 名称：超聚变行业周报
- 执行 xfusion-intelligence 技能
- 推送到飞书和邮件
```

### 4.2 验证定时任务

```
列出所有定时任务
```

应看到：
```
超聚变行业周报    每周一 09:00    xfusion-intelligence    活跃
```

---

## 📚 第五步：了解进阶功能（5分钟）

### 子领域深度报告

当你想深入了解某个方向时：

```
电源深度报告        → 长城/台达等厂商详细动态
液冷厂商动态        → CoolIT/Asetek/曙光数创等
AI大模型情报        → MiniMax/智谱/Anthropic等
AI解决方案情报      → VMware/Nutanix/华为等
太空算力深度        → LEO卫星/星载AI
人力资源情报        → 竞品招聘/薪酬趋势
```

### 查看历史报告

```bash
# 所有周报
ls ~/.hermes/workspace/intelligence-reports/xfusion-weekly/

# 所有日报
ls ~/.hermes/workspace/intelligence-reports/daily/

# 子领域报告
ls ~/.hermes/workspace/intelligence-reports/sub-domain/
```

---

## ❓ 常见问题

### Q: 执行后没有收到飞书推送？

检查环境变量：
```bash
echo $FEISHU_WEBHOOK_URL
```
如果为空，重新设置。

### Q: 邮件收不到？

可能原因：
1. SMTP 密码填写的是登录密码而非应用专用密码
2. 邮箱开启了安全登录保护，需要先关闭
3. 端口被公司防火墙拦截，尝试 465 (SSL)

### Q: 代理返回"无结果"怎么办？

正常！某些方向（如太空算力）新闻稀疏。报告会自动标注"本周无重大信号"。

### Q: 如何暂停定时任务？

在 Hermes 对话中：
```
暂停「超聚变行业周报」任务
```

### Q: 如何新增监控企业？

1. 打开 `~/.hermes/skills/xfusion-intelligence/references/company-watchlist.md`
2. 在对应表格中添加一行
3. 下次执行时自动生效

---

## 🎉 完成！

现在你拥有了：
- 一个 24/7 运行的 AI 情报系统
- 每周自动推送的行业周报
- 随时可触发的子领域深度分析
- 持续增长的情报知识库

---

*有新问题？在 Hermes 对话中直接问：*  
*"超聚变情报系统怎么XXX？"*

*文档版本: 1.0 | 创建: 2026-06-27*
