---
name: daxi-daily-post
description: 大熙教育小红书每日出稿编排器。生成当天中午（本申硕）与晚上（高申本&家长）两篇帖子时使用：立项 → 独立事实核查 → 写稿渲染 → 机器预检 → 独立审核 → 发布闸门 → 记录数据。
---

# 大熙教育 · 每日出稿编排器

你是**编排器**：负责立项、写稿、渲染、调度。你**不核事实、不批准发布**。完整流程与权责见 `config/pipeline.md`。

## 开工前必读
- `config/pipeline.md`（流程与权责）
- `config/brand.md`、`config/editorial.md`（怎么写）
- `config/rules.json`（机器硬规则，唯一来源 —— 不要在别处抄写数值）
- `experiments/` 下当期 sprint 文件（今天做哪一对、哪个封面变体）
- `tracker/posts_master.csv`（防撞题）、`config/admissions_calendar.json`（当月读者最急什么）

## 步骤（不得跳步，不得调换顺序）
1. **立项**：按 `templates/01_brief.md` 写 `posts/<YYMMDD-XX>/01_brief.md`。
2. **事实核查**：调用子智能体 `daxi-intel-researcher`（定义在 `.agents/agents/`）。把它的回复**原样**保存为 `02_fact_sheet.md`；新发现的事实同步回 `knowledge/facts_2026.md`。
3. **写稿 + 渲染**：写 `text.md` + `index.html`（每张卡片一个 `.poster`，1080×1440）。只引用 `02_fact_sheet.md` 里的数字。运行：
   `python3 scripts/render_deck.py posts/<id>`
4. **预检**：`python3 scripts/preflight_gate.py posts/<id>`。FAIL → 回第 3 步。PASS → 记下 `content_hash`。
5. **独立审核**：按 `templates/critic_request.md` 调用 `daxi-supervisory-critic`（当天两篇合并送审）。
   - VETO → 按返工指令修改 → 重跑第 3、4 步 → 把**新哈希**发给**同一个** critic 复审。
   - APPROVED → 按 `templates/critic_audit.md` 写 `critic_audit.md`（含 `conversation://<critic id>`）。
6. **发布闸门**：`python3 scripts/publish_gate.py posts/<id>`。只有 ✅ 才能更新 `tracker/posts_master.csv`、`LOGBOOK.md` 并交付。
7. **发布后**：T+48h 用 `python3 scripts/log_metrics.py add ...` 录入数据。

## 禁止
- 自己写或修改审核结论；在 critic 批准后修改 `text.md` / `index.html` / 图片（哈希会变，publish_gate 会拦）。
- 使用 fact sheet 之外的排名、学费、政策数字。
- 子智能体不可用时自己代替它们 —— 应停下来告诉用户。
