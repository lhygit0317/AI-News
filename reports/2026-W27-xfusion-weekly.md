# 超聚变行业情报周报（正式版）

**周期：2026-06-24 至 2026-07-01**  
**生成时间：2026-07-01**  
**发送对象：飞书群、lihongyu@xfusion.com**  
**信息范围：截至 2026-07-01 的公开资讯与公开报道**

---

## 一、本期摘要

本期行业信号集中在三个方向：第一，AI 数据中心的供电和液冷方案继续向平台化、模块化、标准化推进，800VDC、直接液冷和暖液冷成为高密 AI 基础设施的重要技术路线；第二，美国对前沿模型访问控制的政策试探，与 OpenAI 自研推理芯片等事件共同说明，模型能力、监管合规和算力自主化正在同步影响 AI 服务器需求结构；第三，国产 AI 基础设施和人才竞争继续升温，华为 Ascend、H3C 全栈 AI 基础设施、DeepSeek 招聘扩张等信号对超聚变的供应链、生态定位和人才策略均有直接参考价值。

对超聚变而言，本期最重要的判断是：AI 服务器竞争正在从单机硬件能力转向“服务器整机 + 电源架构 + 液冷系统 + 芯片生态 + 交付效率”的综合竞争。短期应重点跟踪 800VDC、液冷 CDU/冷板供应链、国产 AI 芯片适配、私有化 AI 部署需求，以及 AI 基础设施人才供给。

---

## 二、电源与液冷

| 事项 | 来源/日期 | 关键内容 | 对超聚变影响 |
|------|-----------|----------|--------------|
| Ecolab 收购 CoolIT Systems | Ecolab，2026-03-20；仍处 2026 年交易推进周期 | Ecolab 宣布以约 47.5 亿美元收购 CoolIT Systems，目标是形成面向下一代 AI 数据中心的端到端流体管理和液冷平台。 | CoolIT 属于直接液冷核心供应商之一，若客户或供应链依赖其冷板/CDU 能力，需评估交易完成后供应优先级、价格策略和二供方案。 |
| Delta 展示 AI Modular Data Center | Delta COMPUTEX 2026，2026-06 | Delta 展示下一代 AI 模块化数据中心，将 800VDC 高压直流供电与先进液冷技术集成，面向高密 GPU/AI 计算环境。 | 800VDC 与液冷的集成化趋势要求服务器平台更早介入机柜级供电和热设计协同，避免仅停留在整机层面适配。 |
| NVIDIA 推出 45 摄氏度暖液冷思路 | NVIDIA Blog，2026-06-21 | NVIDIA 表示新一代 AI 服务器可使用约 45 摄氏度冷却液运行，从而降低传统冷却塔和用水压力。 | 暖液冷有利于降低数据中心水耗和运维复杂度，超聚变应评估该路线对整机热设计、运维环境和客户节能诉求的影响。 |
| Vertiv 展示 AI 数据中心全栈方案 | Vertiv COMPUTEX 2026，2026-06 | Vertiv 展示 SmartRun、OneCore、800V DC 架构以及面向 AI 的先进液冷方案。 | 上游基础设施厂商正在提供更完整的机柜级与数据中心级方案，服务器 OEM 需要强化与电力、散热、机柜厂商的联合方案能力。 |

**判断：** 电源和液冷正在从“部件选型”升级为“平台架构”。超聚变后续应把 800VDC、冷板/CDU 二供、机柜级液冷、整机功耗密度和交付周期作为统一技术议题管理。

---

## 三、AI 大模型与算力需求

| 事项 | 来源/日期 | 关键内容 | 对超聚变影响 |
|------|-----------|----------|--------------|
| 美国解除 Anthropic Fable/Mythos 模型出口控制 | The Guardian、Financial Times 等，2026-07-01 | 美国政府在安全协议后解除 Anthropic Fable 5 与 Mythos 5 的出口控制，事件显示前沿模型已进入监管与安全审查的高敏感阶段。 | 前沿模型访问可能出现“可信伙伴”“分级开放”等新机制，企业级和主权 AI 部署将更强调本地算力、合规部署和可控基础设施。 |
| OpenAI 限制 GPT-5.6 推出范围 | TechCrunch，2026-06-26 | OpenAI 表示应美国政府要求，将最新模型发布限制在少数可信合作伙伴范围内。 | 模型能力提升仍会推高算力需求，但监管限制可能推动更多企业转向私有化、国产化和多模型冗余部署。 |
| OpenAI 与 Broadcom 发布 Jalapeno 推理芯片 | OpenAI，2026-06；Tom's Hardware，2026-06 | OpenAI 与 Broadcom 发布面向 LLM 推理的定制 AI 芯片 Jalapeno，强调推理效率、内存移动、网络和大规模服务模式优化。 | 大客户自研推理芯片会改变服务器加速卡生态。超聚变需要关注通用 GPU、ASIC、国产加速卡在服务器架构中的兼容和供货格局变化。 |
| Qwen-Robot Suite 发布 | Qwen，2026-06 | Qwen 发布面向物理世界智能体的机器人基础模型套件，覆盖导航、操作和世界模型等方向。 | 具身智能将带来新的边缘推理和机器人训练需求，长期可能扩展 AI 服务器和边缘计算设备需求。 |

**判断：** AI 模型侧的主要矛盾正在从“模型是否更强”转向“模型能力、监管可用性和推理成本如何共同落地”。这对 AI 服务器需求是利好，但需求形态会更偏向合规私有化、多芯片适配和推理成本优化。

---

## 四、AI 基础设施方案与竞品动态

| 事项 | 来源/日期 | 关键内容 | 对超聚变影响 |
|------|-----------|----------|--------------|
| Nutanix 2026 Enterprise Cloud Index | Nutanix，2026；Healthcare vertical 报道 2026-06 | Nutanix 报告关注 AI 对基础设施现代化、容器、影子 AI、数据主权和基础设施准备度的影响。医疗行业报道显示 AI 应用意愿明显快于基础设施准备度。 | 企业 AI 落地仍存在基础设施缺口，有利于 AI 就绪服务器、私有云和行业解决方案打包销售。 |
| H3C NAVIGATE 2026 | H3C，2026-05 | H3C 强调“Connecting the AI Future”，提出面向 AI 时代的全栈能力、产品方案和 Token 成本效率优化。 | H3C 正把服务器、网络、AI 基础设施和生态一起包装，超聚变需要在行业方案、交付速度和生态合作上形成差异化。 |
| 华为 Ascend 与 DeepSeek V4 相关进展 | TrendForce、Tom's Hardware，2026-06 | TrendForce 报道华为 Ascend 950DT 部署节奏提前；另有报道显示华为相关团队使用 Ascend 910C 完成 DeepSeek V4-Pro 的后训练工作。 | 国产 AI 芯片生态正在加速补齐训练和推理链路。超聚变需要明确在 Ascend 等国产生态中的适配、合作或差异化路径。 |

**判断：** AI 基础设施竞争正在向“全栈交付能力”集中。服务器厂商仅提供硬件会面临方案商和芯片生态厂商的挤压，必须补强行业场景、软件栈适配、交付工具链和售前架构能力。

---

## 五、太空算力与前沿算力场景

| 事项 | 来源/日期 | 关键内容 | 对超聚变影响 |
|------|-----------|----------|--------------|
| SpaceX 轨道数据中心设想持续发酵 | Light Reading，2026-06-10；WSJ，2026-06 | 行业报道显示 SpaceX 正探索轨道数据中心与 AI 计算卫星方案，部分报道提到 SpaceX 与 Google 围绕轨道数据中心进行讨论。 | 短期仍属前沿概念，但高功率密度、可靠性、热管理和边缘推理能力值得跟踪，可作为特种环境计算和边缘计算技术储备参考。 |
| 轨道数据中心可行性仍受质疑 | ScienceDaily，2026-06 | 相关分析认为，SpaceX AI1 Compute Satellite 等设想与地面数据中心相比仍存在能力差距，技术、散热、维护和经济性仍需验证。 | 不宜短期重投入，但应保持技术跟踪，优先关注可回流到地面特种服务器的散热、供电和低功耗推理技术。 |

**判断：** 太空算力目前仍是前沿观察项。对超聚变更现实的价值是倒推高可靠边缘计算、低功耗推理和特种环境服务器技术路线。

---

## 六、人力资源与人才竞争

| 事项 | 来源/日期 | 关键内容 | 对超聚变影响 |
|------|-----------|----------|--------------|
| DeepSeek 扩大招聘 | SCMP，2026-06；FT，2026-06 | DeepSeek 计划扩大核心团队规模，招聘覆盖全栈开发、算法、AI 核心系统研发、深度学习研究、模型数据策略和工程等方向。 | AI 基础设施与模型公司对系统、算法和工程人才的竞争将进一步加剧。超聚变在 AI 服务器架构、性能优化、液冷工程和国产芯片适配岗位上需更主动储备。 |
| AI 与半导体人才持续紧缺 | 行业报道，2026-06 | HBM、AI 芯片、模型工程和基础设施岗位持续吸引资本和头部企业资源。 | 薪酬竞争和项目吸引力会成为招聘关键。建议围绕“AI 基础设施工程化”“绿色液冷”“国产化适配”建立更清晰的人才卖点。 |

**判断：** 人才竞争已经从模型算法扩散到 AI 基础设施工程。超聚变应把关键岗位储备前置，尤其是 AI 服务器系统架构、GPU/国产加速卡适配、液冷设计、数据中心供电和集群运维方向。

---

## 七、对超聚变的综合影响评估

### 机会

| 机会 | 说明 | 时间窗口 |
|------|------|----------|
| 私有化与合规 AI 部署需求上升 | 前沿模型访问控制、企业数据主权和影子 AI 风险共同推动本地 AI 基础设施建设。 | 短期至中期 |
| 高密 AI 服务器平台升级 | 800VDC、直接液冷、暖液冷和模块化数据中心方案推动服务器平台升级。 | 短期至中期 |
| 国产 AI 芯片生态适配 | Ascend 等国产生态进展为国产服务器厂商提供新的适配与方案空间。 | 中期 |
| 行业 AI 基础设施缺口 | 医疗等行业 AI 采用快于基础设施准备度，利于行业方案销售。 | 短期 |

### 风险

| 风险 | 说明 | 紧迫度 |
|------|------|--------|
| 上游液冷供应链集中 | CoolIT 被收购等事件可能改变供应优先级和价格体系。 | 高 |
| 全栈方案商挤压服务器 OEM | H3C、华为、Nutanix 等均在强化端到端方案叙事。 | 高 |
| 客户自研芯片改变服务器架构 | OpenAI/Broadcom Jalapeno 显示大客户可能绕开部分通用加速卡路径。 | 中 |
| AI 基础设施人才竞争升级 | DeepSeek 等模型公司扩招会提高关键工程岗位招聘难度。 | 中 |

### 建议行动

1. 建立 800VDC 与液冷联合技术跟踪清单，覆盖电源、冷板、CDU、机柜、维护和客户数据中心条件。
2. 对 CoolIT、Delta、Vertiv、国内液冷供应商进行二供和联合方案评估，明确短期可替代供应链。
3. 梳理 Ascend、国产加速卡、NVIDIA、AMD 以及未来 ASIC 推理卡的服务器适配路线图。
4. 形成面向医疗、政企私有化 AI、制造等行业的“AI 就绪服务器 + 液冷 + 私有云基础设施”标准方案。
5. 针对 AI 服务器架构、液冷工程、国产芯片适配和集群性能优化岗位建立专项人才池。

---

## 八、来源清单

1. Ecolab: [Ecolab to Acquire CoolIT Systems](https://investor.ecolab.com/news/news-details/2026/Ecolab-to-Acquire-CoolIT-Systems-a-Global-Leader-in-Advanced-Liquid-Cooling-for-Next-Gen-AI-Data-Centers/default.aspx)
2. Delta: [Delta @ COMPUTEX 2026](https://landing.deltaww.com/en-US/landing/Computex-2026)
3. NVIDIA: [Hotter Than a Hot Tub: The 45°C Breakthrough](https://blogs.nvidia.com/blog/liquid-cooling-ai-factories/)
4. Vertiv: [Vertiv at Computex 2026](https://www.vertiv.com/en-cn/about/news-and-events/events/vertiv-at-computex-2026/)
5. The Guardian: [US lifts export controls on Anthropic models](https://www.theguardian.com/technology/2026/jul/01/anthropic-fable-mythos-ai-models-us-export-controls-lifted)
6. TechCrunch: [OpenAI limits GPT-5.6 rollout](https://techcrunch.com/2026/06/26/openai-limits-gpt-5-6-rollout-after-government-request-says-restrictions-shouldnt-be-the-norm/)
7. OpenAI: [OpenAI and Broadcom unveil Jalapeno inference chip](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)
8. Qwen: [Qwen-Robot Suite](https://qwen.ai/blog?id=qwen-robotsuite)
9. Nutanix: [2026 Enterprise Cloud Index](https://www.nutanix.com/enterprise-cloud-index)
10. H3C: [NAVIGATE 2026 International Summit](https://www.h3c.com/en/d_202605/2844902_294554_0.htm)
11. TrendForce: [Huawei Ascend 950DT deployment](https://www.trendforce.com/news/2026/06/08/news-huawei-brings-forward-ascend-950dt-deployment-to-august-deepseek-v4-2-seen-as-potential-early-adopter/)
12. Light Reading: [SpaceX orbital AI data center plan](https://www.lightreading.com/data-centers/musk-magic-not-needed-for-spacex-s-orbital-ai-data-center-plan)
13. ScienceDaily: [SpaceX wants to build AI data centers in space](https://www.sciencedaily.com/releases/2026/06/260618041501.htm)
14. SCMP: [DeepSeek hiring spree](https://www.scmp.com/tech/big-tech/article/3358394/deepseek-hiring-spree-chinese-ai-firm-seeks-newcomers-it-pursues-agi)

---

*本报告仅基于公开信息整理，用于行业情报参考，不构成投资建议或公司正式经营决策文件。*
