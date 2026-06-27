# RSS 源清单（xFusion 情报专用）

> 本文档收录服务器/算力/AI行业经实战验证的RSS新闻源。
> 当通用搜索引擎失效时，直接用 curl 抓取 RSS Feed 获取新闻。

---

## 服务器/数据中心行业

| 源 | URL | 定位 | 频率 |
|----|-----|------|------|
| ServeTheHome | `https://www.servethehome.com/feed/` | 企业级服务器/工作站 | 每日 |
| ServeTheHome (加速器) | `https://www.servethehome.com/category/accelerators/feed/` | GPU/AI加速器 | 不定期 |
| ServeTheHome (存储) | `https://www.servethehome.com/category/storage/feed/` | SSD/NAND/HDD | 不定期 |
| ServeTheHome (部件) | `https://www.servethehome.com/category/server-parts/feed/` | 内存/网卡/其他 | 不定期 |
| TechPowerUp | `https://www.techpowerup.com/rss/news` | GPU/DRAM/SSD | 每日 |
| DataCenterKnowledge | `https://www.datacenterknowledge.com/feed` | 数据中心运维 | 每日 |
| DataCenterDynamics | `https://www.datacenterdynamics.com/feed/` | 基础设施 | 每日 |

## AI/科技新闻

| 源 | URL | 定位 | 频率 |
|----|-----|------|------|
| The Verge AI | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` | 消费+企业AI | 每日 |
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` | AI创业 | 每日 |
| VentureBeat AI | `https://venturebeat.com/category/ai/feed/` | AI产业 | 每日 |
| MIT Tech Review | `https://www.technologyreview.com/feed/` | 科技深度 | 每日 |

## 中国科技

| 源 | URL | 定位 | 频率 |
|----|-----|------|------|
| 机器之心 | `https://www.jiqizhixin.com/rss` | 中国AI | 每日 |
| 量子位 | `https://www.qbitai.com/feed` | 中国AI | 每日 |
| 36氪 | `https://36kr.com/feed` | 创投科技 | 每日 |

## 通用新闻

| 源 | URL | 定位 | 频率 |
|----|-----|------|------|
| BBC World | `https://feeds.bbci.co.uk/news/world/rss.xml` | 国际 | 每日 |
| BBC Business | `https://feeds.bbci.co.uk/news/business/rss.xml` | 商业 | 每日 |
| BBC Tech | `https://feeds.bbci.co.uk/news/technology/rss.xml` | 科技 | 每日 |

---

## curl 抓取命令模板

```bash
# ServeTheHome 全站
curl -sL -A "Mozilla/5.0" "https://www.servethehome.com/feed/" | grep -iE "(title|link|pubDate)" | head -150

# TechPowerUp
curl -sL -A "Mozilla/5.0" "https://www.techpowerup.com/rss/news" | grep -iE "(title|pubDate)" | head -60

# DataCenterDynamics
curl -sL -A "Mozilla/5.0" "https://www.datacenterdynamics.com/feed/" | grep -iE "(title|pubDate)" | head -60

# BBC Tech
curl -sL "https://feeds.bbci.co.uk/news/technology/rss.xml" | grep -E "<title>|<description>" | sed 's/<[^>]*>//g' | head -30
```

---

## 搜索失效时的备选策略

1. **RSS Feed 抓取** — 使用上表URL，curl直接获取
2. **Google News 浏览器** — `browser_navigate("https://news.google.com/search?q=...")` 
3. **Bing News 浏览器** — `browser_navigate("https://www.bing.com/news/search?q=...")`
4. **SCMP/Nikkei 直接导航** — 2026-06 实测可用

---

*最后更新：2026-06-27*
