---
name: xfusion-intelligence
category: research
description: 超聚变(xFusion)多维度行业情报收集 — 覆盖电源/液冷/AI软件与方案/太空算力/人力资源五大方向，支持飞书+邮件双通道推送
trigger: "超聚变周报 | xFusion情报 | 服务器行业情报 | 多维度情报收集"
---

# 超聚变(xFusion)多维度行业情报收集

## 核心设计

本技能使用**多代理并行架构**，同时启动 5 个独立 sub-agent 分不同方向采集情报，最后汇总输出结构化报告。**支持飞书（精简推送+链接）+ 邮件（完整报告）双通道推送。**

### 五大监控领域

| 领域 | 代理 | 监控重点 |
|------|------|---------|
| 🔵 电源+液冷 | 代理1 | 长城/台达/曙光数创/CoolIT等 |
| 🟢 AI大模型 | 代理2 | MiniMax/智谱/Anthropic/OpenAI/Google/Qwen/Kimi |
| 🟡 AI解决方案 | 代理3 | VMware/Nutanix/深信服/华三/浪潮/华为/百度/阿里 |
| 🔴 太空算力 | 代理4 | LEO卫星/AI推理/轨道数据中心 |
| ⚪ 人力资源 | 代理5 | 竞品招聘/薪酬趋势/人才流动 |

### 周期计算规则

**周期 = 过去一周，不是当前周或未来。**
- 生成日期为 X，周期 = (X-7天) 至 X

```python
from datetime import datetime, timedelta
today = datetime.now()
period_end = today
period_start = today - timedelta(days=7)
week_start = period_start.strftime('%Y-%m-%d')
week_end = period_end.strftime('%Y-%m-%d')
```

### 公司定位

**用户公司 = 超聚变 (xFusion)**。从华为分拆的中国服务器 OEM 厂商，主要产品包括 FusionServer 系列通用服务器、AI 服务器、液冷方案。

**所有情报分析必须以「对超聚变的影响」为最终落脚点。**

---

## 报告存储位置

```
~/.hermes/workspace/intelligence-reports/
├── xfusion-weekly/
│   ├── 2026-W26-xfusion-weekly.md       # 周报
│   ├── latest-xfusion-weekly.md         # 软链接→最新
│   └── archive/                         # 12周+
├── sub-domain/
│   ├── power-supply/                    # 电源深度报告
│   ├── liquid-cooling/                  # 液冷深度报告
│   ├── ai-software/                     # AI软件深度报告
│   ├── space-computing/                 # 太空算力深度报告
│   └── hr-intelligence/                 # 人力深度报告
└── daily/
    └── 2026-06-27-xfusion-daily.md      # 日报
```

---

## 执行流程

### 步骤 0：读取历史报告摘要

在启动并行代理之前，读取最近 2-4 份历史报告，建立"跨周期关联"基线：

```bash
python3 << 'EOF'
import re
from pathlib import Path
from datetime import datetime, timedelta

today = datetime.now()
period_end = today
period_start = today - timedelta(days=7)
week_start = period_start.strftime('%Y-%m-%d')
week_end = period_end.strftime('%Y-%m-%d')

reports_dir = Path.home() / ".hermes" / "workspace" / "intelligence-reports" / "xfusion-weekly"

# Collect weekly report files
candidates = []
for p in reports_dir.glob("2026-W*.md"):
    if "latest" in p.name:
        continue
    try:
        if p.resolve().exists():
            candidates.append(p)
    except OSError:
        continue

candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
recent = candidates[:4]

history_summaries = []
for report in recent:
    try:
        content = report.read_text()
    except Exception:
        continue
    # Extract "要闻摘要" section
    emoji_pattern = r'📋\s*本周要闻摘要'
    match_emoji = re.search(emoji_pattern, content)
    if not match_emoji:
        continue
    line_start = match_emoji.start()
    search_slice = content[:match_emoji.start()]
    last_nl = search_slice.rfind('\n')
    line_start = last_nl + 1 if last_nl != -1 else 0
    remaining = content[match_emoji.end():]
    end_match = re.search(r'\n## [🔵🟢🟡🔴⚪📋]', remaining)
    end = match_emoji.end() + end_match.start() if end_match else len(content)
    section = content[line_start:end]
    section = re.sub(r'^#+\s*', '', section, flags=re.MULTILINE)
    history_summaries.append(f"### {report.name}\n{section[:800]}")

print(f"week_start={week_start}")
print(f"week_end={week_end}")
print(f"history_count={len(history_summaries)}")
for i, s in enumerate(history_summaries):
    print(f"--- HISTORY_{i} ---")
    print(s)
EOF
```

**如果历史报告数量 < 2，跳过跨周期分析，直接执行采集。**

---

### 步骤 1：并行启动 5 个采集代理

由于 `max_concurrent_children = 3` 的限制，分**两批**调用 `delegate_task()`：

**第一批（3个并行）：**
1. 代理1：🔵 电源 + 液冷
2. 代理2：🟢 AI大模型(7家)
3. 代理3：🟡 AI基础设施方案(8家)

**第二批（2个并行）：**
4. 代理4：🔴 太空算力
5. 代理5：⚪ 人力资源

每个代理的 context 必须注入：
```
【共享上下文】
- 搜索时间窗口：{week_start} 至 {week_end}（过去7天）
- 用户公司：超聚变 (xFusion) — 中国服务器 OEM，从华为分拆，产品：FusionServer 通用/AI 服务器 + 液冷方案
- 输出语言：简体中文，结构化报告格式
- 过滤原则：只保留企业级/数据中心相关内容，消费类产品全部剔除
- **所有分析必须包含「对超聚变的影响」评估**
- 历史摘要基线：
  {history_summary_text}
```

---

### 代理 1：电源 + 液冷情报

```
goal: |
  搜索本周（{week_start} 至 {week_end}）服务器电源和液冷相关事件，专注企业级市场。

  搜索方向（并行搜索）：
  1. Great Wall server power supply xFusion
  2. Delta data center power solution liquid cooling
  3. Vertiv Emerson data center infrastructure
  4. CoolIT Asetek liquid cooling data center
  5. 曙光数创 英维克 液冷 数据中心

  输出要求：
  - 整理为部件/企业表格（企业 | 关键事件 | 来源/日期 | 对xFusion影响）
  - 每个方向给出 2-3 条信号
  - 最后输出 1 行汇总判断

  **重要：禁止向磁盘写入任何文件。直接输出结构化报告文本。**

context: |
  你是服务器行业情报分析员。用户公司 = 超聚变 (xFusion)。关注服务器电源生态和液冷散热。
  过滤标准：专注企业级数据中心，排除消费电子/新能源汽车电源。
  输出语言：简体中文。
  历史基线：
  {history_summary_text}

toolsets: ['web', 'terminal']
```

### 代理 2：AI大模型情报

```
goal: |
  搜索本周（{week_start} 至 {week_end}）AI大模型领域动态，覆盖7家核心模型厂商。

  搜索方向（并行搜索）：
  1. MiniMax AI model multimodal release
  2. Zhipu GLM ChatGLM enterprise
  3. Anthropic Claude model enterprise API
  4. OpenAI GPT enterprise pricing
  5. Google Gemini AI model
  6. Qwen Alibaba AI model open source
  7. Kimi Moonshot AI long context

  输出要求：
  - 按模型厂商分块，每家 1-2 条关键事件
  - 判断每条事件对xFusion的"影响"（机会/威胁/中性）
  - 标注信号强度：🔥🔥🔥（重要）/🔥🔥（一般）/🔥（参考）

context: |
  AI大模型影响xFusion的AI服务器需求（推理/训练）。模型越强→算力需求越大→AI服务器需求越旺。
  关注：模型能力提升（利好算力）、国产模型进展（利好xFusion国产化定位）、API降价（算力需求弹性）。
  输出语言：简体中文。
  历史基线：
  {history_summary_text}

toolsets: ['web', 'terminal']
```

### 代理 3：AI基础设施方案情报

```
goal: |
  搜索本周（{week_start} 至 {week_end}）AI基础设施方案领域动态。

  搜索方向（并行搜索）：
  1. VMware vSphere AI private cloud
  2. Nutanix AI HCI GPT-in-a-Box
  3. Sangfor深信服 AI security HCI
  4. H3C AI server networking
  5. Inspur AI server solution
  6. Huawei Ascend AI cluster
  7. Baidu PaddlePaddle AI cloud
  8. Alibaba Tongyi AI platform

  输出要求：
  - 按企业分块，每家 1-2 条关键事件
  - 判断对xFusion的"竞争影响"（机会/威胁/中性）

context: |
  这些方案商是xFusion的合作伙伴或竞品。方案趋势直接决定xFusion服务器的配套生态和差异化空间。
  输出语言：简体中文。
  历史基线：
  {history_summary_text}

toolsets: ['web', 'terminal']
```

### 代理 4：太空算力情报

```
goal: |
  搜索本周（{week_start} 至 {week_end}）太空算力相关动态。

  搜索方向（并行搜索）：
  1. AWS space edge computing satellite
  2. LEO satellite AI computing orbital
  3. radiation hardened AI chip space
  4. NASA ESA space data center
  5. 中国星网 卫星 计算

  输出要求：
  - 3-5 个核心信号判断
  - 每个信号：标签 + 简述 + 对xFusion启示
  - 如本周无重大事件，输出"本周太空算力方向无重大信号"

context: |
  太空算力是前沿方向，与超聚变服务器的未来场景（边缘算力、特种环境计算）相关。
  如太空算力方向新闻稀疏，优先关注AWS/Azure太空边缘计算等落地项目。
  输出语言：简体中文。

toolsets: ['web', 'terminal']
```

### 代理 5：人力资源情报

```
goal: |
  搜索本周（{week_start} 至 {week_end}）AI/服务器行业人力资源动态。

  搜索方向（并行搜索）：
  1. Huawei AI chip talent hiring 2026
  2. Inspur Lenovo server AI recruitment
  3. AI engineer salary China 2026
  4. xFusion 超聚变 招聘
  5. 服务器 AI 芯片 人才 流动

  输出要求：
  - 竞品招聘动态 2-3 条
  - 薪酬/人才趋势 1-2 条
  - 对xFusion人才策略的影响判断

context: |
  关注AI/服务器行业核心岗位（芯片架构、AI训练、液冷工程）的招聘动态和薪酬趋势。
  分析竞品人才策略变化对xFusion的招聘竞争和人才保留的影响。
  输出语言：简体中文。

toolsets: ['web', 'terminal']
```

---

### 步骤 2：合并结果 + 跨周期关联分析

5 个代理全部返回后：

1. **组装完整报告**：按报告模板合并 5 个代理结果
2. **跨周期关联分析**：
   - 对比本次信号与 `history_summary` 中的历史信号
   - 识别"**持续信号**"（3周以上反复出现）：标注 🔄
   - 识别"**新信号**"（本周首次出现）：标注 🆕
   - 识别"**衰减信号**"（之前重要但本周减弱）：标注 📉
3. **写入报告文件**

---

### 步骤 3：保存报告 + 生成推送版本

```python
from datetime import datetime
from pathlib import Path
import os

today = datetime.now()
week_num = today.isocalendar()[1]
year = today.year
week_start_str = (today - __import__('datetime').timedelta(days=7)).strftime('%m.%d')
week_end_str = today.strftime('%m.%d')

# 保存周报
filename = f"{year}-W{week_num:02d}-xfusion-weekly.md"
filepath = Path.home() / ".hermes" / "workspace" / "intelligence-reports" / "xfusion-weekly" / filename
filepath.write_text(full_report_markdown, encoding='utf-8')

# 更新 latest 软链接
latest_link = Path.home() / ".hermes" / "workspace" / "intelligence-reports" / "xfusion-weekly" / "latest-xfusion-weekly.md"
if latest_link.exists():
    latest_link.unlink()
os.symlink(filename, str(latest_link))

print(f"Report saved: {filepath}")
```

---

### 步骤 4：飞书推送（精简版）

生成 **200字以内** 的飞书推送文本：

```python
feishu_text = f"""【超聚变行业周报 {week_start_str}-{week_end_str}】
🔵 电源/液冷：{power_signals}
🟢 AI模型：{model_signals}
🟡 AI方案：{solution_signals}
🔴 太空算力：{space_signals}
⚪ 人才：{hr_signals}

📌 {core_conclusion}

🔗 完整报告：{report_url}
#xFusion #服务器 #AI #液冷"""
```

发送：
```bash
# 使用飞书 Webhook 推送
curl -X POST "$FEISHU_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"$feishu_text\"}}"
```

---

### 步骤 5：邮件推送（完整报告）

```bash
# 清除 emoji 后发送 HTML 邮件
python3 ~/.hermes/skills/xfusion-intelligence/scripts/push-email.py \
  --subject "超聚变行业周报 ${week_start_str} - ${week_end_str}" \
  --report "${filepath}" \
  --to "${EMAIL_TO}"
```

---

## 报告模板

```markdown
# 📊 超聚变行业周报
**周期：{week_start} 至 {week_end}**
**生成时间：{timestamp}**

---

## 📋 本周要闻摘要

### 🆕 本周新事件
### 🔄 持续性信号
### 📉 衰减/减弱信号

---

## 🔗 跨周期关联分析

---

## 🔵 一、电源与液冷

[来自代理1的汇总]

---

## 🟢 二、AI大模型动态

[来自代理2的汇总]

---

## 🟡 三、AI基础设施方案

[来自代理3的汇总]

---

## 🔴 四、太空算力

[来自代理4的汇总]

---

## ⚪ 五、人力资源

[来自代理5的汇总]

---

## 📌 本周核心结论

[3条以内，一句话总结最重要的事]

---

## 🏢 对超聚变的影响评估

### 机会 (Opportunities)
### 威胁 (Threats)
### 建议行动

---

*📁 报告文件：{filename}*
*🔗 历史报告：{previous_reports_links}*
```

---

## 子领域深度报告触发

如需某子领域的深度报告，可独立触发对应子技能：

```bash
# 加载子技能后执行
skill_view('power-supply-deep')       # 电源深度
skill_view('liquid-cooling-deep')     # 液冷深度
skill_view('ai-software-deep')        # AI软件深度
skill_view('space-computing-deep')    # 太空算力深度
skill_view('hr-intelligence-deep')    # 人力资源深度
```

每个子技能包含该领域的完整监控清单、搜索策略和深度报告模板。

---

## 定时任务配置

**当前状态：定时任务已暂停。** 内容和格式调整完成前，不创建自动周报任务，不自动推送飞书或邮件。

```python
# 暂停期间仅允许查看任务，不创建新任务
cronjob(action='list')

# 子领域深度报告也暂停定时创建，需要时手动触发对应子技能。
```

---

## 验证步骤

- [ ] 5 个代理均成功返回结果
- [ ] 汇总报告中包含全部 5 个维度
- [ ] 报告文件保存到 `xfusion-weekly/`
- [ ] `latest-xfusion-weekly.md` 正确链接
- [ ] 跨周期关联分析正确
- [ ] 飞书推送文本 ≤ 200 字
- [ ] 邮件包含完整报告

---

## Pitfalls

### 1. 子代理返回空内容
部分搜索方向（尤其是太空算力、人力资源等小众方向）可能返回空。**立即切换到直接浏览器搜索**作为后备：
```bash
browser_navigate("https://news.google.com/search?q=LEO+satellite+edge+computing+AI+2026&hl=en-US")
browser_navigate("https://www.bing.com/news/search?q=AI+chip+talent+hiring+China+2026")
```

### 2. 飞书推送字数超限
严格控制 200 字以内。每个方向只取最核心 1 条，剩余用链接引导。

### 3. 邮件 emoji 兼容
Gmail/企业邮不支持彩色 emoji，发送前用正则清除：
```python
import re
text = re.sub(r'[\U0001F000-\U0001FFFF]', '', text)
```

### 4. 太空算力方向新闻稀疏
如连续多周无重大信号，该章节可简化为 2-3 行"本周无重大动态"，不强行凑内容。

---

*技能版本: 1.0*
*基于: server-industry-weekly-intelligence v1.1*
*创建日期: 2026-06-27*
