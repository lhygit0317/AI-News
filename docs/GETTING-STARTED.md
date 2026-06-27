# 超聚变多维度情报系统 — 从零搭建完全指南

> **目标读者：零基础人员**
> **预计耗时：1-2 小时完成全部搭建**
> **最终效果：每周三/周五 9:00 自动收集六大方向行业情报，飞书推送 + 邮件群发 30 人**

---

## 目录

1. [这个系统是什么](#1-这个系统是什么)
2. [准备两样东西](#2-准备两样东西)
3. [第一步：租一台云服务器](#3-第一步租一台云服务器)
4. [第二步：申请大模型 API Key](#4-第二步申请大模型-api-key)
5. [第三步：安装 Hermes Agent](#5-第三步安装-hermes-agent)
6. [第四步：克隆项目代码](#6-第四步克隆项目代码)
7. [第五步：配置推送通道](#7-第五步配置推送通道)
8. [第六步：部署技能文件](#8-第六步部署技能文件)
9. [第七步：首次试运行](#9-第七步首次试运行)
10. [第八步：配置定时任务](#10-第八步配置定时任务)
11. [日常维护](#11-日常维护)
12. [故障排查](#12-故障排查)

---

## 1. 这个系统是什么

一句话：**一个 7×24 小时运行的 AI 助手，每周三和周五早上 9:00 自动帮你搜新闻、写周报、发飞书、发邮件。**

```
每周三 9:00  ──→  搜上周五~本周三的新闻
每周五 9:00  ──→  搜本周三~本周五的新闻
        ↓
   5个AI同时搜索（电源/液冷/AI模型/AI方案/太空+人力）
        ↓
   自动写报告 → 飞书发精简版 → 邮件群发30人完整版
```

你不用做任何操作，系统全自动运转。

---

## 2. 准备两样东西

在开始之前，你需要准备好：

### 2.1 云服务器（约 ¥50-100/月）

| 推荐方案 | 配置 | 月费 |
|---------|------|------|
| 阿里云 ECS | 2核4G 40G云盘 | ~¥68 |
| 腾讯云轻量 | 2核4G 60G SSD | ~¥58 |
| 华为云 HECS | 2核4G 40G | ~¥70 |

> **为什么需要云服务器？** 你的个人电脑关机了系统就停了。云服务器 24 小时开着，定时任务不会断。

### 2.2 大模型 API Key

Hermes Agent 需要一个 AI 大模型来驱动。推荐：

| 推荐 | 获取方式 | 费用 |
|------|---------|------|
| **DeepSeek** | https://platform.deepseek.com → 注册 → API Keys | ¥1/百万token |
| 硅基流动 | https://siliconflow.cn → 注册 → API密钥 | 有免费额度 |
| OpenAI | https://platform.openai.com → API keys | $5起充 |

> **为什么要额外准备 API Key？** 免费的模型有调用频率限制。购买 API Key 相当于给系统配了一个专属司机，不会因为排队或限流导致跑到一半断掉。

**充值建议：** 首次充 ¥50-100 就够了，每周两次报告大概消耗 ¥2-5。

---

## 3. 第一步：租一台云服务器

以**阿里云 ECS** 为例（其他云类似）：

### 3.1 购买服务器

1. 打开 https://ecs.console.aliyun.com
2. 点击「创建实例」
3. 按以下配置选择：

| 配置项 | 选择 |
|--------|------|
| 地域 | 离你近的（如华东1杭州） |
| 镜像 | **Ubuntu 22.04** |
| 规格 | 2 vCPU + 4 GiB |
| 系统盘 | 40 GB |
| 网络 | 分配公网 IPv4 |
| 登录凭证 | **设置 root 密码**（记下来！） |

4. 确认订单，支付

### 3.2 连接服务器

服务器创建完成后，你会看到一个**公网 IP 地址**（如 `47.96.xxx.xxx`）。

**Windows 电脑：**
1. 下载 PuTTY：https://www.putty.org/
2. 在 Host Name 输入公网 IP，点 Open
3. 用户名填 `root`，密码填你设置的

**Mac 电脑：**
打开终端，输入：
```bash
ssh root@你的公网IP
# 输入密码
```

### 3.3 基础环境安装

连上服务器后，依次执行以下命令（复制粘贴，回车）：

```bash
# 更新系统
apt update && apt upgrade -y

# 安装必要工具
apt install -y curl git python3 python3-pip unzip

# 验证
python3 --version  # 应显示 Python 3.10+
git --version      # 应显示 git version 2.xx
```

---

## 4. 第二步：申请大模型 API Key

以 **DeepSeek** 为例（性价比最高）：

1. 打开 https://platform.deepseek.com
2. 注册账号（邮箱或手机号）
3. 进入「API Keys」页面
4. 点击「创建 API Key」
5. **复制并保存**这个 Key（它只显示一次！）

你会得到一个类似 `sk-xxxxxxxxxxxxxxxxxxxxxxxx` 的字符串。

> ⚠️ 这个 Key 相当于你的钱包密码，不要发给任何人。

---

## 5. 第三步：安装 Hermes Agent

回到云服务器终端，执行：

```bash
# 安装 Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 初始化配置
hermes setup
```

在 `hermes setup` 过程中会问你几个问题，按以下回答：

```
选择 provider: 输入 deepseek（或你用的平台）
输入 API Key: 粘贴你第4步保存的 Key
选择 model: 输入 deepseek-chat（DeepSeek 的推荐模型）
```

安装完成后验证：
```bash
hermes --version   # 应显示版本号
```

---

## 6. 第四步：克隆项目代码

```bash
# 进入 home 目录
cd ~

# 克隆项目
git clone https://github.com/lhygit0317/AI-News.git

# 进入项目
cd AI-News

# 查看文件
ls
```

你应该看到这些目录：
```
skill/       # 情报收集技能
templates/   # 报告模板
scripts/     # 推送脚本
references/  # 配置参考
docs/        # 文档
reports/     # 报告存档
```

---

## 7. 第五步：配置推送通道

### 7.1 配置飞书 Webhook

1. 打开飞书电脑版
2. 进入目标群聊 → 右上角 `···` → 设置 → 群机器人
3. 添加机器人 → 自定义机器人
4. 复制 Webhook 地址（类似 `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx`）

在服务器上执行（替换成你的 Webhook）：
```bash
echo 'FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/你的地址"' >> ~/.hermes/.env
```

### 7.2 配置邮件发送

使用 **163 邮箱** 作为发送邮箱：

> ⚠️ 建议新注册一个 163 邮箱专门用来发报告，不要用个人主邮箱。

1. 注册 163 邮箱：https://mail.163.com
2. 登录后 → 设置 → POP3/SMTP/IMAP
3. 开启「SMTP 服务」→ 会生成一个**授权码**
4. 复制这个授权码

在服务器上执行（替换成你的信息）：
```bash
cat >> ~/.hermes/.env << 'EOF'
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=你的邮箱@163.com
SMTP_PASS=你的授权码
EMAIL_FROM=你的邮箱@163.com
SENDER_NAME=李红雨
EOF
```

### 7.3 配置收件人列表

编辑 `~/AI-News/scripts/push-email.py`，找到收件人列表部分，替换为你想要的邮箱地址。

---

## 8. 第六步：部署技能文件

```bash
# 创建 Hermes 技能目录
mkdir -p ~/.hermes/skills/xfusion-intelligence

# 复制所有文件
cp -r ~/AI-News/skill/* ~/.hermes/skills/xfusion-intelligence/
cp -r ~/AI-News/references ~/.hermes/skills/xfusion-intelligence/
cp -r ~/AI-News/templates ~/.hermes/skills/xfusion-intelligence/
cp -r ~/AI-News/scripts ~/.hermes/skills/xfusion-intelligence/
cp -r ~/AI-News/docs ~/.hermes/skills/xfusion-intelligence/

# 创建报告存储目录
mkdir -p ~/.hermes/workspace/intelligence-reports/{xfusion-weekly,daily,sub-domain}
```

---

## 9. 第七步：首次试运行

```bash
# 进入 Hermes 交互模式
hermes chat
```

在对话中输入：
```
执行 xfusion-intelligence 技能，生成本周行业情报
```

系统会自动：
1. 计算本周时间窗口（周三=上周五~今天，周五=本周三~今天）
2. 同时启动 5 个 AI 代理搜索新闻
3. 合并结果生成报告
4. 飞书推送精简版
5. 邮件群发完整版

**预计耗时：5-8 分钟。** 在云服务器上即使关掉终端也会继续跑。

---

## 10. 第八步：配置定时任务

在 Hermes 对话中输入：
```
创建一个定时任务：
- 名称：超聚变周报
- 时间：每周三和每周五早上9点
- 执行：xfusion-intelligence 技能
- 飞书推送 + 邮件群发
```

或者直接用命令：
```bash
hermes cron create \
  --name "超聚变周报" \
  --schedule "0 9 * * 3,5" \
  --skill xfusion-intelligence \
  --prompt "生成本周行业情报报告，飞书推送+邮件群发"
```

---

## 11. 日常维护

### 11.1 查看定时任务状态
```bash
hermes cron list
```

### 11.2 查看生成的报告
```bash
ls ~/.hermes/workspace/intelligence-reports/xfusion-weekly/
```

### 11.3 手动触发一次
在 Hermes 对话中：
```
立即执行超聚变周报
```

### 11.4 更新监控企业
编辑文件：
```bash
nano ~/.hermes/skills/xfusion-intelligence/references/company-watchlist.md
```
在对应表格中添加或删除企业，下次执行自动生效。

### 11.5 更换收件人
编辑脚本：
```bash
nano ~/.hermes/skills/xfusion-intelligence/scripts/push-email.py
```

### 11.6 API Key 续费
当 API 余额不足时，报告生成会失败。登录 API 平台充值即可，无需重启服务。

---

## 12. 故障排查

### 12.1 报告没发出来？

```bash
# 检查定时任务是否正常
hermes cron list

# 查看日志
tail -100 ~/.hermes/logs/hermes.log
```

### 12.2 飞书没收到？

```bash
# 检查 Webhook 是否配置
cat ~/.hermes/.env | grep FEISHU

# 手动测试
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-feishu.py \
  --webhook "你的webhook地址" \
  --text "测试消息"
```

### 12.3 邮件没收到？

检查：
- 163 邮箱 SMTP 是否开启
- 授权码是否正确（不是登录密码！是 SMTP 专用授权码）
- 收件人邮箱地址是否拼写正确

```bash
# 手动测试邮件
python3 -c "
import smtplib
from email.mime.text import MIMEText
msg = MIMEText('测试', 'plain', 'utf-8')
msg['From'] = '你的邮箱@163.com'
msg['To'] = '收件人@xfusion.com'
msg['Subject'] = '测试'
with smtplib.SMTP_SSL('smtp.163.com', 465) as s:
    s.login('你的邮箱@163.com', '授权码')
    s.sendmail('你的邮箱@163.com', ['收件人@xfusion.com'], msg.as_string())
print('OK')
"
```

### 12.4 服务器跑着跑着断了？

**这就是为什么用云服务器而不是个人电脑。** 确保：
- 云服务器选择「包年包月」而非「按量付费」（按量付费可能欠费停机）
- 服务器安全组开放出站端口（默认都是开放的）
- API Key 余额充足（每周约消耗 ¥1-2）

### 12.5 API Key 余额查询

DeepSeek：https://platform.deepseek.com → 用量统计
硅基流动：https://siliconflow.cn → 控制台 → 用量

---

## 附录 A：系统架构速览

```
云服务器 (7×24h)
└── Hermes Agent
    ├── 每周三/周五 9:00 触发
    ├── 5个AI代理并行搜索
    │   ├── 🔵 电源
    │   ├── 💧 液冷
    │   ├── 🟢 AI大模型 (7家)
    │   ├── 🟡 AI方案 (8家)
    │   ├── 🔴 太空算力
    │   └── ⚪ 人力资源
    ├── 自动生成报告
    ├── → 飞书 Webhook (精简版)
    └── → SMTP邮件 (30人完整版)
```

## 附录 B：关键文件位置

| 文件 | 路径 | 作用 |
|------|------|------|
| 主技能 | `~/.hermes/skills/xfusion-intelligence/SKILL.md` | 定义采集流程 |
| 企业清单 | `references/company-watchlist.md` | 监控企业 |
| 飞书模板 | `templates/feishu-push-template.md` | 推送格式 |
| 邮件模板 | `templates/email-template.html` | 邮件格式 |
| 飞书脚本 | `scripts/push-feishu.py` | 发送飞书 |
| 邮件脚本 | `scripts/push-email.py` | 发送邮件 |
| 环境配置 | `~/.hermes/.env` | Key/密码 |
| 报告存档 | `~/.hermes/workspace/intelligence-reports/` | 历史报告 |

## 附录 C：费用预估

| 项目 | 月费 |
|------|------|
| 云服务器 (2核4G) | ¥50-70 |
| DeepSeek API | ¥30-50 |
| 163 邮箱 | 免费 |
| **合计** | **¥80-120/月** |

---

*文档版本：1.0 | 编写于 2026-06-27*
*如有问题，在 Hermes 对话中直接问即可。*
