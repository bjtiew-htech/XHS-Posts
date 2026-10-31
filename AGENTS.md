# 大熙教育 · 小红书出稿仓库

- 每日出稿：使用 skill `daxi-daily-post`（`.agents/skills/daxi-daily-post/SKILL.md`）。
- 流程与权责：`config/pipeline.md`。写稿规则：`config/brand.md`、`config/editorial.md`。机器规则唯一来源：`config/rules.json`。
- 子智能体：`.agents/agents/daxi-intel-researcher`（事实核查）、`.agents/agents/daxi-supervisory-critic`（独立审核，只读）。
- 编排器不得自己核事实、不得自己写审核结论；`scripts/publish_gate.py` 不通过的帖子不得发布。
- `_archive/` 是历史遗留，不要读取或引用。

