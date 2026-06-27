# 新闻源清单（已验证 + 新增）

> 继承 `server-industry-weekly-intelligence` 技能中已验证的新闻源，并扩展 xFusion 特定方向。

---

## ✅ 已继承验证源（来自原技能，2026年5-6月实测）

### 通用搜索（首选）

| 源 | URL 模板 | 备注 |
|----|---------|------|
| **Google News** | `https://news.google.com/search?q=<关键词>&hl=en-US&gl=US&ceid=US%3Aen` | 优于Bing News，支持时间过滤 |
| **Bing News** | `https://www.bing.com/news/search?q=<关键词>&setlang=en-US` | 备选，bot检测宽松，支持 `dateFilter:7d` |
| **SCMP** | `https://www.scmp.com/tech/policy` | 中国AI政策、半导体、科技战 |
| **Nikkei Asia** | `https://asia.nikkei.com/` | 亚洲AI投资、半导体供应链 |
| **SIA** | `https://www.semiconductors.org/` | 美国半导体产业协会，政策博客 |

### 行业垂直源

| 源 | URL | 覆盖方向 |
|----|-----|---------|
| **ServeTheHome** | `https://www.servethehome.com/feed/` | 企业级硬件、服务器部件 |
| **TechPowerUp** | `https://www.techpowerup.com/rss/news` | GPU/DRAM/SSD |
| **DataCenterDynamics** | `https://www.datacenterdynamics.com/` | 数据中心基础设施 |

### RSS Feed（curl直接抓取）

```bash
# ServeTheHome 全站
curl -sL -A "Mozilla/5.0" "https://www.servethehome.com/feed/"

# TechPowerUp
curl -sL -A "Mozilla/5.0" "https://www.techpowerup.com/rss/news"

# BBC Tech
curl -sL "https://feeds.bbci.co.uk/news/technology/rss.xml"
```

---

## 🆕 新增方向专用源（xFusion 扩展）

### AI 大模型

| 源 | URL | 备注 |
|----|-----|------|
| **机器之心** | `https://www.jiqizhixin.com/` | 中国AI深度报道 |
| **量子位** | `https://www.qbitai.com/` | 中国AI产业动态 |
| **The Verge AI** | `https://www.theverge.com/ai-artificial-intelligence` | 消费+企业AI |
| **TechCrunch AI** | `https://techcrunch.com/category/artificial-intelligence/` | AI创业公司 |
| **The Information** | `https://www.theinformation.com/` | 科技深度报道（部分付费） |

### 液冷/电源/数据中心基础设施

| 源 | URL | 备注 |
|----|-----|------|
| **DataCenterKnowledge** | `https://www.datacenterknowledge.com/` | 数据中心运维 |
| **Uptime Institute** | `https://uptimeinstitute.com/` | 数据中心标准 |
| **CoolingPost** | `https://www.coolingpost.com/` | 制冷行业 |

### 中国科技/商业

| 源 | URL | 备注 |
|----|-----|------|
| **36氪** | `https://36kr.com/` | 创投+科技 |
| **虎嗅** | `https://www.huxiu.com/` | 科技商业 |
| **晚点LatePost** | `https://www.latepost.com/` | 深度商业报道 |

### 人力资源

| 源 | URL | 备注 |
|----|-----|------|
| **脉脉** | `https://maimai.cn/` | 中国科技圈动态 |
| **猎聘** | `https://www.liepin.com/` | 高端招聘趋势 |
| **LinkedIn News** | `https://www.linkedin.com/news/` | 全球职场动态 |

---

## ❌ 已知不可用源

| 源 | 原因 |
|----|------|
| Reuters | DataDome 设备验证拦截 |
| FT | Cloudflare 拦截 |
| DuckDuckGo API | 返回测试假数据 |
| Google 直接搜索(curl) | bot检测拦截 |
| The Register | 强bot检测 |
| Tom's Hardware | HTTP 400 拒绝 |

---

## 🔍 搜索策略优先级

### AI模型方向
1. **机器之心/量子位** → 中国AI动态
2. **Google News** → `MiniMax OR Zhipu OR Qwen model 202X`
3. **TechCrunch/The Verge** → 国际AI

### 液冷/电源方向（中文）
1. **Google News** → `液冷 数据中心 曙光数创 OR 英维克`
2. **Bing News** → `liquid cooling data center 202X`
3. **Search ServeTheHome** → `liquid cooling immersion`

### 太空算力方向（小众）
1. **Google News** → `LEO satellite edge computing AI`
2. **ArXiv** → `space-based computing AI`
3. **公告机构** → NASA/ESA 官网

### 人力资源方向
1. **脉脉/猎聘** → 竞品招聘动态
2. **LinkedIn News** → 行业人才报告
3. **Google News** → `AI chip talent hiring China`

---

## ⚠️ 安全规避规则

1. **禁止** `curl | python3/shell` → Tirith [HIGH] 拦截
2. **使用** `browser_navigate` 访问搜索页面
3. **避免** 直接访问 Reuters/FT/Google 裸搜索
4. **DuckDuckGo API** 绝对不可用于新闻搜索

---

*最后更新：2026-06-27*
