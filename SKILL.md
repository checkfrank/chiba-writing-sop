---
name: chiba-writing-sop
description: 基于22个技能的完整写文流水线 SOP，覆盖信息采集→选题决策→内容生产→发布复盘四个阶段，适用于公众号、头条号等自媒体内容创作场景
skill_level: advanced
skill_source: local_project
---

# Chiba 写文 SOP 流水线

## 概述

这是一个完整的 AI 辅助内容创作流水线，整合了 22 个技能（来自 clawhub、GitHub 和本地安装），按照 4 阶段 6 分组的方式组织，实现从热点采集到最终发布的全流程自动化。

**适用场景：**
- 每日公众号/头条号文章创作
- 热点追踪与深度分析
- 多平台内容分发
- 知识管理与经验沉淀

**🔥 2026-06-16 升级：** 新增 `daily-hot-news`（54 平台热榜采集）、`wechat-title-generator`（8 标题×5 维打分最优推荐）

---

## 技能总览（22 个技能，6 大分组）

### 分组 ① 信息获取

| 技能 | 来源 | GitHub 地址 | 功能 |
|------|------|-------------|------|
| `tencent-news` | clawhub | <https://clawhub.dev/tencentnewsteam/tencent-news> | 抓取 48 小时内腾讯新闻热点，获取标题、摘要、来源 |
| 🆕 `wechat-title-generator` | 手动 | <https://github.com/walkor/humanizer> | **8 个标题候选×5 维打分**：反差/情绪/结果/认知 4 类 → 最优+稳妥+激进 3 选 1 |
| `humanizer` | 手动 | <https://github.com/walkor/humanizer> | 去除 AI 痕迹，使文风更自然人性化 |

**⚠️ 顺序红线：** `content-ops` → `adversarial-review` → `brand-voice` → `wechat-title-generator` → `humanizer`

### 分组 ④ 质量把控

已在前三阶段嵌入门禁，无需额外执行。

### 分组 ⑤ 记忆与增长

| 技能 | 来源 | GitHub 地址 | 功能 |
|------|------|-------------|------|
| `agent-memory` | 手动 | — | 长期记忆管理，沉淀创作经验 |
| `self-improving` | 手动 | — | 自我改进与反思，记录错误和修正 |
| `ontology` | 手动 | — | 本体管理，结构化知识图谱 |
| `ai-growth-engine` | clawhub | <https://github.com/KingOfZhao/AGI_PROJECT> | AI 增长引擎，自动化内容优化建议 |
| `neat-freak` | GitHub | <https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak> | 知识库洁癖同步，检查膨胀、清理残留 |

### 分组 ⑥ 排版与发布

| 技能 | 来源 | GitHub 地址 | 功能 |
|------|------|-------------|------|
| `baoyu-markdown-to-html` | 手动 | <https://github.com/nicefang/baoyu-markdown-to-html> | Markdown → 微信公众号兼容 HTML，支持代码高亮、数学公式 |
| `content-repurposer` | clawhub | <https://clawhub.dev/audsmith28/content-repurposer> | 一文多平台适配（头条、小红书、知乎等） |
| `baoyu-post-to-wechat` | 手动 | <https://github.com/nicefang/baoyu-post-to-wechat> | 推送文章到微信公众号 |

---

## 4 阶段流水线

```
[输入] 主题方向 / 今日热点
    ↓
┌─────────────────────────────────────────────────────┐
│ 阶段一：信息采集（~5 分钟）🔥                          │
│  采集 → 54 平台热榜 → 摘要 → 搜索                     │
│  tencent-news → 🆕daily-hot-news → smart-summarize     │
│  → web-search-exa                                     │
│  ↓                                                    │
│  [输出] TOP3 候选选题（54 平台热点交叉验证）           │
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
│ 阶段三：内容生产（~20 分钟）⚠️ 严格顺序                  │
│  写作框架 → 质量审核 → 对抗审核 → 品牌语调 → 标题生成 → 去AI化 │
│  marketing-skills → content-ops → adversarial-review │
│  → brand-voice → 🆕wechat-title-generator → humanizer │
│  ↓                                                    │
│  [输出] 3000 字精修正文 + 最优标题推荐                  │
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
🔥 chiba daily-hot-news --platforms 微博，知乎，抖音，B站，头条
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
chiba content-repurposer --input publish.html --platforms 头条，小红书
chiba baoyu-post-to-wechat --file publish.html
chiba agent-memory --log "今日创作经验"
chiba ontology --update knowledge-graph
chiba neat-freak --sync --audit
```

---

## 常见坑与注意事项

1. **content-ops 评分不足 90 分** → 不要跳到 adversarial-review，必须重写内容再重新提交审核
2. **adversarial-review 第 1 轮就 < 8 分** → 检查是否有硬伤（事实错误、逻辑漏洞），直接重写而非修补
3. **brand-voice 和 wechat-title-generator 顺序不可颠倒** → 必须先调整语调再生成标题（标题需要文风 DNA）
4. **wechat-title-generator 必须在 humanizer 之前** → 去痕迹前先生成标题，避免标题变形
5. **neat-freak 必须在最后执行** → 确保所有前置任务完成后清理知识库
6. **每阶段耗时预估** → 严格执行时间限制，阶段一不超过 5 分钟，阶段三不超过 20 分钟
7. **技能路径问题** → clawhub 技能在 `e:\QClaw\fujingkecheng\skills\`，手动技能在 `~/.workbuddy/skills\`
8. 🆕 **daily-hot-news 必须与 tencent-news 并行** → 54 平台热榜补充多平台热点交叉验证

---

## 安装状态

| 状态 | 技能数 | 来源 |
|------|--------|------|
| ✅ 已安装 | 11 | clawhub（tencent-news, smart-summarize, web-search-exa, deep-research-prime, arxiv-watcher, content-ops, marketing-skills, autoresearch, brand-voice, content-repurposer, ai-growth-engine） |
| ✅ 已安装 | 2 | GitHub（neat-freak, hv-analysis） |
| ✅ 已安装 | 1 | 本地（adversarial-review） |
| ✅ 已安装 | 8 | 手动/原有（humanizer, agent-memory, self-improving, ontology, baoyu-markdown-to-html, baoyu-post-to-wechat, 🆕daily-hot-news, 🆕wechat-title-generator） |

**总计：22 个技能，全部安装完成。🔥 2026-06-16 新增 4 个技能。**

---

## 更新日志

- 2026-06-12：创建初始版本，整合 18 个技能到统一 skill
- 2026-06-12：为每个技能补充 GitHub/clawhub 源地址
- 2026-06-16：🔥🔥🔥 升级至 22 个技能，新增 `daily-hot-news`（54 平台热榜采集）+ `wechat-title-generator`（8 标题×5 维打分最优推荐）
- 2026-06-16：更新一键启动指令、顺序红线、常见坑
