# 大熙教育 · 小红书内容引擎

每天两篇：12:30 本申硕专栏（`-01`），20:00 高申本 & 家长专栏（`-02`）。

## 目录
```text
AGENTS.md                      给 agent 的入口说明
.agents/
  skills/daxi-daily-post/      编排器 skill（每日出稿从这里开始）
  agents/daxi-intel-researcher 事实核查员（只读 + 联网）
  agents/daxi-supervisory-critic 独立审核员（只读 + 联网 + 看图，有否决权）
config/
  pipeline.md                  流程：3 方分权 + 2 道机器闸门
  brand.md                     品牌、人设、双赛道、SEO
  editorial.md                 窄切口、页数、四层深度骨架、钩子边界
  rules.json                   机器硬规则唯一来源（违禁词 / 标题 / 页数 / 尺寸）
  admissions_calendar.json     申请季节点
knowledge/facts_2026.md        招生事实库（带核验日期与来源，90 天过期）
experiments/sprint_01.md       当期 A/B 实验与预注册判定规则
templates/                     brief / fact sheet / 送审消息 / 审核转录 模板
tools/render.mjs               自有渲染器（Playwright）
scripts/
  render_deck.py               index.html → 01..NN.jpg + .render_manifest.json
  preflight_gate.py            机器闸门 #1
  publish_gate.py              机器闸门 #2（读取 critic 原始对话核对哈希）
  log_metrics.py               发布后数据录入 + A/B 判定
posts/YYMMDD-XX/               每帖：01_brief / 02_fact_sheet / text.md / index.html / NN.jpg / 04_preflight_report.json / critic_audit.md
tracker/                       posts_master / metrics_snapshots / performance_log
_archive/                      历史遗留（不再使用）
```

## 常用命令
```bash
npm install                                        # 首次：安装 Playwright
python3 scripts/render_deck.py posts/261031-01
python3 scripts/preflight_gate.py posts/261031-01
python3 scripts/publish_gate.py posts/261031-01
python3 scripts/log_metrics.py add 261031-01 --impressions 820 --views 131 --saves 5
python3 scripts/log_metrics.py evaluate Sprint1_Cover_Test
```

Python 依赖：`beautifulsoup4`、`Pillow`。
