---
name: chiba-writing-sop
version: 29
update_date: 2026-06-29
---

# 写文 SOP 流水线 — 29 技能协同自动写作

> 基于《我让15个AI组了个团队》文章搭建，将29个技能按功能分组并串成4阶段流水线，实现"发一条指令，AI自动完成从热点采集到公众号推送"的全流程写作自动化。
>
> ⚡ **2026-06-29 17:16 重大调整**：阶段三改为 adversarial-review → auto-content-ops → jiaozhen-factcheck → content-ops（先对抗审核再优化内容再查证事实）；content-factory 移到阶段四（与 content-repurposer 一起做多平台格式转换）；去 AI 6 步输出整合为完整改写包（4份文件）；最终交付物为 HTML 页面 + 综合多平台 MD 文件（content-factory + content-repurposer 平台重合保留）；arxiv-watcher 按选题适用性调用；baoyu-post-to-wechat 保留但需用户指定 API 时才执行

## 流水线架构

```
[输入] 主题方向/今日热点
    ↓
┌─────────────────────────────────────────┐
│  阶段一：信息采集                         │
│  tencent-news → daily-hot-news            │
│  smart-summarize → web-search-exa         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  阶段二：选题决策                         │
│  wechat-viral-topic → deep-research-prime │
│  arxiv-watcher → hv-analysis → autoresearch│
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  阶段三：内容生产                         │
│  marketing-skills → jiaozhen-factcheck    │
│  auto-content-ops → content-ops           │
│  content-factory → adversarial-review     │
│  brand-voice → wechat-title-generator     │
│  6 层去 AI 流水线 (ai-text-humanizer-zh 等)│
│  writing-polish                           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  阶段四：记忆与发布                       │
│  agent-memory → self-improving → ontology │
│  ai-growth-engine → neat-freak            │
│  baoyu-markdown-to-html → content-repurposer│
│  baoyu-post-to-wechat                     │
└─────────────────────────────────────────┘
    ↓
[输出] 公众号文章 + 多平台适配 + 记忆沉淀
```

## 29 技能总览

### ① 信息采集（4 个技能）

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| `tencent-news` | 抓取最新 48 小时腾讯新闻热点 | — |
| `daily-hot-news` | 54 平台热榜采集（微博/知乎/抖音/B站/头条等） | `clawhub install daily-hot-news` |
| `smart-summarize` | 长文快速摘要生成 | — |
| `web-search-exa` | Exa AI 全网搜索补充资讯 | — |

### ② 选题决策（5 个技能）

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| `wechat-viral-topic` | 10 万+爆款选题制造机 | `clawhub install wechat-viral-topic` |
| `deep-research-prime` | 选题背景多轮调研 | — |
| `arxiv-watcher` | ArXiv 学术论文追踪 | `clawhub install arxiv-watcher` |
| `hv-analysis` | 横纵分析法深度研究 | — |
| `autoresearch` | 自主实验循环（定义指标→单变量迭代→keep/discard） | `clawhub install autoresearch` |

### ③ 内容生产（11 个技能）

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| `marketing-skills` | 23 个营销知识库模块 | — |
| `adversarial-review` | **对抗式审核**：笔杆子→参谋→裁判循环，≥8分 | — |
| `auto-content-ops` | **薛辉自媒体流水线**：抓热文→生热梗→结合产品 | `clawhub install auto-content-ops` |
| `jiaozhen-factcheck` | **事实查证**：对文章事实/数据/常识查证 | — |
| `content-ops` | 内容质量评分与专家评审（90+分迭代） | — |
| `brand-voice` | 品牌语调 profile 管理 | `clawhub install brand-voice` |
| `wechat-title-generator` | 8标题×5维打分最优推荐 | `clawhub install wechat-title-generator` |
| `ai-text-humanizer-zh` | AI 特征检测与诊断（16+ 类模式） | 专家包 |
| `humanizer-deai` | 24 种 AI 痕迹消除规则 | 专家包 |
| `humanize-ai-text-cp3d` | AI 检测器绕过优化 | 专家包 |
| `humanize-zh` | 中文机械化→自然风格转换 | 专家包 |
| `unclecheng-reduce-ai-perception-v2` | 中文专项修复（L1-L4 四层质检） | 专家包 |
| `writing-polish` | 深度润色与语言优化 | 专家包 |

### ④ 发布与复盘（6 个技能）

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| `agent-memory` | 持久记忆系统（remember/learn/recall） | `clawhub install agent-memory` |
| `self-improving` | 自我反思+自我批评+自我学习 | — |
| `ontology` | 类型化知识图谱 | `clawhub install ontology` |
| `ai-growth-engine` | Agent 自我成长引擎（RAPVL 五步循环） | — |
| `neat-freak` | 知识库洁癖同步 | — |
| `baoyu-markdown-to-html` | Markdown→微信公众号兼容 HTML | — |
| `content-factory` | **多平台格式转换**：5个专家角色，一份素材多格式 | `clawhub install content-factory` |
| `content-repurposer` | 一文多平台适配（头条/小红书/知乎） | — |
| `baoyu-post-to-wechat` | 推送微信公众号草稿箱（需指定 API 才执行） | — |

## 使用方式

1. 安装所有 29 个技能（见上方安装命令）
2. 在 WorkBuddy 对话中发送主题方向或热点关键词
3. AI 自动按 4 阶段流水线执行：信息采集 → 选题决策 → 内容生产 → 发布与记忆
4. 全流程无需人工干预，输出公众号文章 + 多平台适配版本

## 质量门禁

- **对抗审核**：adversarial-review ≥8 分才过
- **去 AI 流水线**：6 层检测与改写全部通过
- **品牌语调**：brand-voice 一致性检查
- **标题质量**：wechat-title-generator 5 维打分

## 仓库结构

```
.
├── README.md              # 本文件（SOP 说明）
├── skills/                # 29 个技能源文件
│   ├── tencent-news/
│   ├── daily-hot-news/
│   ├── smart-summarize/
│   ├── ...
│   └── baoyu-post-to-wechat/
└── 写文SOP流水线.md       # 完整版 SOP 文档（详细说明）
```

## 更新日志

- **2026-06-29 17:16**：🆕 阶段三顺序调整为 adversarial-review → auto-content-ops → jiaozhen-factcheck → content-ops；content-factory 移到阶段四；去 AI 6 层流水线整合为完整改写包（4份文件交付）；最终交付物为 HTML 页面 + 综合多平台 MD 文件
- **2026-06-29**：用 6 个"内容去 AI 味专家包"替换 humanizer-zh
- **2026-06-27**：修复本地 SOP 重大偏差，对齐 GitHub 原版；批量替换 7 个技能
- **2026-06-16**：新增 daily-hot-news（54 平台热榜）、wechat-title-generator
- **2026-06-14**：初始版本（15 技能）
