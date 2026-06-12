# Chiba Writing SOP — 18 技能写文流水线

> 一套完整的 AI 辅助自媒体内容创作 SOP，覆盖 **信息采集 → 选题决策 → 内容生产 → 发布复盘** 四个阶段，共整合 **18 个技能**。

## 🎯 项目定位

本项目将一篇微信公众号文章中提到的 15 个 AI 技能扩展为 **18 个技能**，按照原文的分组思路和流水线架构封装为标准化作业流程（SOP），可直接运行一键式内容创作全流程。

**适用人群：**
- 公众号/头条号/知乎等自媒体创作者
- 内容运营团队
- AI 自动化工作流爱好者

## 📊 快速概览

```
[输入] 主题方向 / 今日热点
    ↓
阶段一：信息采集（~5 分钟）→ TOP3 候选选题
    ↓
阶段二：选题决策（~10 分钟）→ 最终选题 + TOP3 标题
    ↓
阶段三：内容生产（~15 分钟，⚠️ 严格顺序）→ 3000 字精修正文
    ↓
阶段四：发布与复盘（~5 分钟）→ 全平台分发 + 经验沉淀
    ↓
[输出] 公众号草稿 + 头条/小红书版 + 知识库干净
```

## 🧩 技能总览（18 个技能，6 大分组）

### 分组 ①：信息获取（3 个技能）

| 技能 | 功能 |
|------|------|
| `tencent-news` | 抓取 48 小时内腾讯新闻热点 |
| `smart-summarize` | 长文摘要压缩，提取关键信息 |
| `web-search-exa` | Exa 搜索引擎全网补充 |

### 分组 ②：深度研究（4 个技能）

| 技能 | 功能 |
|------|------|
| `deep-research-prime` | 选题深度背景调研 |
| `arxiv-watcher` | 学术论文追踪 |
| `hv-analysis` | 横纵分析法深度研究 |
| `autoresearch` | 自动化迭代型研究搜索 |

### 分组 ③：内容生产（5 个技能，⚠️ 严格顺序）

| 技能 | 功能 |
|------|------|
| `marketing-skills` | 写作框架 + 爆文结构模板 |
| `content-ops` | 质量审核（≥ 90 分通过） |
| `adversarial-review` | 对抗式审核：写→挑→判，2-3 轮循环 |
| `brand-voice` | 品牌语调 5 项检查 |
| `humanizer` | 去除 AI 痕迹 |

> ⚠️ **顺序红线：** `content-ops` → `adversarial-review` → `brand-voice` → `humanizer`

### 分组 ④：质量把控

已嵌入前三阶段的质��门禁，无需额外步骤。

### 分组 ⑤：记忆与增长（5 个技能）

| 技能 | 功能 |
|------|------|
| `agent-memory` | 长期记忆管理 |
| `self-improving` | 自我改进与反思 |
| `ontology` | 知识图谱管理 |
| `ai-growth-engine` | 自动化内容优化建议 |
| `neat-freak` | 知识库清理与防膨胀 |

### 分组 ⑥：排版与发布（3 个技能）

| 技能 | 功能 |
|------|------|
| `baoyu-markdown-to-html` | Markdown → 公众号兼容 HTML |
| `content-repurposer` | 一文多平台适配 |
| `baoyu-post-to-wechat` | 推送至微信公众号 |

## 🔒 质量门禁

| 阶段 | 门禁 | 标准 |
|------|------|------|
| 一 | 候选选题数 | ≥ 3 条 |
| 二 | 标题综合评分 | ≥ 80 分 |
| 三 | content-ops 初审 | ≥ 90 分 |
| 三 | adversarial-review | ≥ 8/10 分，2-3 轮循环 |
| 三 | brand-voice | 通过 5 项检查 |
| 三 | humanizer | AI 痕迹 < 10% |
| 四 | neat-freak | 知识库无膨胀 |

## 🚀 使用方法

1. 克隆本仓库：
   ```bash
   git clone https://github.com/checkfrank/chiba-writing-sop.git
   ```

2. 确保 18 个技能已正确安装（参见 [SKILL.md](./SKILL.md) 的安装部分）

3. 按 [SKILL.md](./SKILL.md) 中的一键启动指令跑全流程

## 📁 仓库结构

```
├── SKILL.md          # 完整技能定义与执行手册
├── README.md         # 本文件
└── LICENSE
```

## 📚 参考来源

- 原始灵感：[《我让15个AI组了个团队》](https://mp.weixin.qq.com/s/dErprPNud8_4Ixr0lECHKQ) — 硅基智见
- 技能来源：Clawhub、GitHub、本地安装

## ⚠️ 常见坑

1. **content-ops 不及格** → 严禁跳过，必须重写后重新提交
2. **adversarial-review 首轮低分** → 通常是硬伤，直接重写
3. **顺序不可颠倒** → brand-voice 必须在 humanizer 之前
4. **neat-freak 放最后** → 所有任务完成后才清理知识库

## 📄 许可证

MIT License
