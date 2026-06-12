---
name: chiba-writing-sop
description: 基于18个技能的完整写文流水线 SOP，覆盖信息采集→选题决策→内容生产→发布复盘四个阶段，适用于公众号、头条号等自媒体内容创作场景
skill_level: advanced
skill_source: local_project
---

# Chiba 写文 SOP 流水线

## 概述

这是一个完整的 AI 辅助内容创作流水线，整合了 18 个技能（来自 clawhub、GitHub 和本地安装），按照 4 阶段 6 分组的方式组织，实现从热点采集到最终发布的全流程自动化。

**适用场景：**
- 每日公众号/头条号文章创作
- 热点追踪与深度分析
- 多平台内容分发
- 知识管理与经验沉淀

---

## 技能总览（18 个技能，6 大分组）

### 分组 ① 信息获取

| 技能 | 来源 | 功能 |
|------|------|------|
| `tencent-news` | clawhub | 抓取 48 小时内腾讯新闻热点，获取标题、摘要、来源 |
| `smart-summarize` | clawhub | 对长新闻/长文生成结构化摘要，压缩关键信息 |
| `web-search-exa` | clawhub | 使用 Exa 搜索引擎补充全网信息，获取深度背景 |

### 分组 ② 深度研究

| 技能 | 来源 | 功能 |
|------|------|------|
| `deep-research-prime` | clawhub | 对选定选题进行深度背景调研，生成研究报告 |
| `arxiv-watcher` | clawhub | 追踪相关学术论文，获取前沿研究支撑 |
| `hv-analysis` | GitHub | 横纵分析法深度研究（横向多维度对比 + 纵向时间线演变） |
| `autoresearch` | clawhub | 自动化研究型搜索，迭代式获取所需信息 |

### 分组 ③ 内容生产（⚠️ 严格顺序执行）

| 技能 | 来源 | 功能 |
|------|------|------|
| `marketing-skills` | clawhub | 提供写作框架和爆文结构模板，生成初稿 |
| `content-ops` | clawhub | 内容质量审核，评分 ≥ 90 分才通过 |
| `adversarial-review` | 本地 | 对抗式审核：写→挑→判循环，2-3 轮，评分 ≥ 8/10 |
| `brand-voice` | clawhub | 品牌语调检查（5 项）：专业性、亲和力、权威感等 |
| `humanizer` | 手动 | 去除 AI 痕迹，使文风更自然人性化 |

**⚠️ 顺序红线：** `content-ops` → `adversarial-review` → `brand-voice` → `humanizer`

### 分组 ④ 质量把控

已在前三阶段嵌入门禁，无需额外执行。

### 分组 ⑤ 记忆与增长

| 技能 | 来源 | 功能 |
|------|------|------|
| `agent-memory` | 手动 | 长期记忆管理，沉淀创作经验 |
| `self-improving` | 手动 | 自我改进与反思，记录错误和修正 |
| `ontology` | 手动 | 本体管理，结构化知识图谱 |
| `ai-growth-engine` | clawhub | AI 增长引擎，自动化内容优化建议 |
| `neat-freak` | GitHub | 知识库洁癖同步，检查膨胀、清理残留 |

### 分组 ⑥ 排版与发布

| 技能 | 来源 | 功能 |
|------|------|------|
| `baoyu-markdown-to-html` | 手动 | Markdown → 微信公众号兼容 HTML，支持代码高亮、数学公式 |
| `content-repurposer` | clawhub | 一文多平台适配（头条、小红书、知乎等） |
| `baoyu-post-to-wechat` | 手动 | 推送文章到微信公众号 |

---

## 4 阶段流水线

```
[输入] 主题方向 / 今日热点
    ↓
┌─────────────────────────────────────────────────────┐
│ 阶段一：信息采集（~5 分钟）                           │
│  采集 → 摘要 → 搜索                                   │
│  tencent-news → smart-summarize → web-search-exa      │
│  ↓                                                    │
│  [输出] TOP3 候选选题                                 │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│ 阶段二：选题决策（~10 分钟）                           │
│  深度调研 → 横纵分析 → 自动研究                         │
│  deep-research-prime → hv-analysis → autoresearch     │
│  ↓                                                    │
│  [输出] 最终选题 + TOP3 标题方案                        │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│ 阶段三：内容生产（~15 分钟）⚠️ 严格顺序                  │
│  写作框架 → 质量审核 → 对抗审核 → 品牌语调 → 去AI化     │
│  marketing-skills → content-ops → adversarial-review │
│  → brand-voice → humanizer                           │
│  ↓                                                    │
│  [输出] 3000 字精修正文                               │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│ 阶段四：发布与复盘（~5 分钟）                          │
│  排版 → 多平台适配 → 推送 → 经验沉淀 → 知识库清理      │
│  baoyu-markdown-to-html → content-repurposer →       │
│  baoyu-post-to-wechat → agent-memory → ontology →    │
│  neat-freak                                          │
│  ↓                                                    │
│  [输出] 公众号草稿 + 头条/小红书版 + 经验沉淀 + 干净知识库 │
└─────────────────────────────────────────────────────┘
    ↓
[完成]
```

---

## 质量门禁

| 阶段 | 门禁 | 标准 | 不通过处理 |
|------|------|------|-----------|
| 阶段一 | 候选选题数 | ≥ 3 条 | 补充搜索 |
| 阶段二 | 标题综合评分 | ≥ 80 分 | 重新调研 |
| 阶段三 | content-ops 初审 | ≥ 90 分 | 立即重写 |
| 阶段三 | adversarial-review 对抗 | ≥ 8/10 分 | 2-3 轮循环 |
| 阶段三 | brand-voice | 通过 5 项检查 | 修改后继续 |
| 阶段三 | humanizer | AI 痕迹 < 10% | 重新润色 |
| 阶段四 | neat-freak | 知识库无膨胀 | 自动清理 |

---

## 一键启动指令

在项目目录执行以下命令可跑完全流程：

```bash
# 阶段一：信息采集
chiba tencent-news --hours 48
chiba smart-summarize --input news.md
chiba web-search-exa --query "热点话题"

# 阶段二：选题决策
chiba deep-research-prime --topic "选定选题"
chiba hv-analysis --input research.md
chiba autoresearch --topic "深化方向"

# 阶段三：内容生产（⚠️ 严格顺序）
chiba marketing-skills --framework "爆文结构" --output draft.md
chiba content-ops --input draft.md --score
chiba adversarial-review --input draft.md --rounds 3
chiba brand-voice --input draft.md --check 5
chiba humanizer --input draft.md --output final.md

# 阶段四：发布与复盘
chiba baoyu-markdown-to-html --input final.md --output publish.html
chiba content-repurposer --input publish.html --platforms 头条,小红书
chiba baoyu-post-to-wechat --file publish.html
chiba agent-memory --log "今日创作经验"
chiba ontology --update knowledge-graph
chiba neat-freak --sync --audit
```

---

## 常见坑与注意事项

1. **content-ops 评分不足 90 分** → 不要跳到 adversarial-review，必须重写内容再重新提交审核
2. **adversarial-review 第 1 轮就 < 8 分** → 检查是否有硬伤（事实错误、逻辑漏洞），直接重写而非修补
3. **brand-voice 和 humanizer 顺序不可颠倒** → 必须先调整语调再去 AI 痕迹
4. **neat-freak 必须在最后执行** → 确保所有前置任务完成后清理知识库
5. **每阶段耗时预估** → 严格执行时间限制，阶段一不超过 5 分钟，阶段三不超过 15 分钟
6. **技能路径问题** → clawhub 技能在 `e:\QClaw\fujingkecheng\skills\`，手动技能在 `~/.workbuddy/skills\`

---

## 安装状态

| 状态 | 技能数 | 来源 |
|------|--------|------|
| ✅ 已安装 | 11 | clawhub（tencent-news, smart-summarize, web-search-exa, deep-research-prime, arxiv-watcher, content-ops, marketing-skills, autoresearch, brand-voice, content-repurposer, ai-growth-engine） |
| ✅ 已安装 | 2 | GitHub（neat-freak, hv-analysis） |
| ✅ 已安装 | 1 | 本地（adversarial-review） |
| ✅ 已安装 | 6 | 手动/原有（humanizer, agent-memory, self-improving, ontology, baoyu-markdown-to-html, baoyu-post-to-wechat） |

**总计：18 个技能，全部安装完成。**

---

## 更新日志

- 2026-06-12：创建初始版本，整合 18 个技能到统一 skill
