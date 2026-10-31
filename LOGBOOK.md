# 大熙教育 (Daxi Education) — Project Decision & Execution Logbook

> **Purpose**: Chronological single source of truth recording architectural decisions, strategic pivots, daily post generations, and weekly performance retrospectives.

---

## Chronological Decision Log

### `[2026-10-31 14:47] Entry #01 — Core Concept: CubeLV-Style Auto-Agent Pipeline in Antigravity`
- **Context**: Explored how to replicate CubeLV's ability to auto-generate specialized agents that streamline complex workflows at high quality inside Antigravity IDE.
- **Technical Architecture Identified**:
  - **Dynamic Runtime Subagents**: Using `define_subagent` and `invoke_subagent` to spawn task-specific agents with scoped permissions.
  - **Producer–Critic Loop**: Separating the **Generator/Copywriter Agent** from an independent, read-only **Critic/Verifier Agent** that enforces hard rubrics before completion.
  - **Persistence**: Capturing proven multi-agent workflows into reusable workspace **Skills (`.agent/skills/<name>/SKILL.md`)** and recurring jobs via **`/schedule`**.

---

### `[2026-10-31 15:02 – 15:10] Entry #02 — Brand & Business Scope Definition (大熙教育)`
- **Brand**: **大熙教育 (Daxi Education)** — Official Xiaohongshu (小红书) presence.
- **Business Model**: Traditional, high-trust study-abroad consultancy covering:
  1. Profile evaluation & school selection (选校定位与梯度规划)
  2. End-to-end application submission & tracking (网申递交与跟进)
  3. Personal Statement (PS), CV, and Essay guidance & polishing (文书头脑风暴与精修)
- **Target Audience**:
  - **Students**: Overwhelmed by deadlines, GPA cutoffs, and how to write a non-generic Personal Statement.
  - **Parents**: Focused on safety, total budget, QS ranking recognition (考公/落户/名企就业), and ROI.
- **Destination Spectrum (7 Regions)**:
  - **UK (英)**, **US (美)**, **HK (港)**, **SG (新)**, **MY (马)**, **AUS (澳)**, **NZ (新/纽)**.
- **Core Content Principle**: Daily content direction must align dynamically with the **real-time admissions planning cycle** of each destination, projecting senior consultant professionalism ("专业顾问感") and converting readers into organic inquiries.

---

### `[2026-10-31 15:17] Entry #03 — Solving the "7 Destinations vs. Posting Frequency" Bottleneck`
- **Problem**: 1 post/day per country means each region only gets covered once a week; 7 posts/day on 1 account triggers Xiaohongshu spam filters and splits initial traffic pools.
- **Strategic Solution**:
  1. **Cluster the 7 Destinations into 3 Natural Applicant Tracks**:
     - **Cluster A (`英港新澳` Mainstream Combo)**: UK + HK + SG (+ AUS G8) — represents ~70% of co-application demand (`英港新联申` / `英澳联申`).
     - **Cluster B (`美本/美研` Holistic Track)**: US (+ top global co-applications) — high-ticket essay and early background planning focus.
     - **Cluster C (`澳新马` High-ROI / Flexible Track)**: AUS + NZ + MY — budget-conscious families (MY), work-visa/immigration seekers (AUS/NZ), and fast rolling-admission backups.
  2. **Multi-Region Matrix Carousels (一帖多国，分页承接)**: Use 6-slide carousels where Slide 1 hooks a universal problem (GPA band, budget tier, or PS pitfall) and Slides 2–6 break down the regions—maximizing **Swipe-Through Rate (翻页率)** and **Dwell Time (停留时长)**.
  3. **Dynamic Seasonal Weighting**: Automatically shift weekly destination quotas based on the current month's admissions deadlines.

---

### `[2026-10-31 15:24] Entry #04 — 3-Account Matrix Strategy & Tooling Assessment (Antigravity vs. n8n)`
- **3-Account Matrix Assessment**:
  - Splitting into 3 vertical accounts (Cluster A, Cluster B, Cluster C) aligns with Xiaohongshu's vertical account tagging (垂类标签) and increases initial traffic pool CTR.
  - **Anti-Shadowban Requirement ("一机一卡一号")**: Never switch 3 marketing accounts on the same phone or Wi-Fi IP. Future matrix structure: **1 Official Blue-V Enterprise Account (`大熙教育`)** + **2 Personal Consultant IP Accounts** on separate 4G/5G devices.
- **Tooling Division of Labor**:
  - **Antigravity IDE**: Optimal for multi-agent reasoning, critic loops, calendar logic, and local HTML-to-image carousel rendering.
  - **n8n**: Reserved for Phase 3 24/7 cloud scheduling, Feishu/Notion content database sync, and operator mobile notifications.

---

### `[2026-10-31 15:28] Entry #05 — Pivot to Elon Musk's First Principles (最小可执行方案 / MVP)`
- **Critical Correction**: Launching 3 accounts + 5 subagents + n8n cloud pipelines on Day 1 violates Elon Musk's **"Delete, Simplify, Automate Last"** principle.
- **First-Principles Truth**:
  - The atomic unit of value is **ONE post archetype** that reliably earns Cover Clicks (**CTR >= 8%**) and Lead Comments (`评论区留【目标地区+均分+专业】`).
  - Automating 3 accounts before proving 1 post converts only scales zero-conversion output.
- **MVP Decision**:
  - **Phase 1 (Days 1–7)**: 1 Account + 1 Post/Day + 100% Antigravity IDE + Closed-loop CSV tracking.
  - Added 4 conversion multipliers: **Pinned First Comment Hook (置顶评论截流)**, **Profile 3-Pinned-Post Architecture (主页置顶三件套)**, **Safe DM Handoff SOP (私信防封承接)**, and **Consistent 3:4 Consulting Card Visual Anchor (视觉锤)**.

---

### `[2026-10-31 15:42] Entry #06 — Workspace Initialized at /Users/bjtiew/GitHub/XHS Posts`
- **Action**: Resolved `googlecloudtools.datacloud` hook conflict and initialized full project structure (`readme.md`, `LOGBOOK.md`, `config/`, `templates/`, `tracker/`, `.agent/skills/daxi-daily-post/`).

---

### `[2026-10-31 16:17] Entry #07 — Forensic Audit of Historical Posts (261018-01 to 261021-01)`
- **Data Imported**: Logged actual XHS metrics for `261018-01`, `261019-01`, `261020-01`, and `261021-01` into `tracker/performance_log.csv`.
- **Key Positive Discovery (What Already Works!)**:
  - **Cover CTR is Elite (`11.0% – 16.6%`)** vs. XHS education average of `6%–8%`.
  - **`261021-01` Editorial Card Visual Style is a Proven Winner**: Achieved **16.6% CTR** and **99.2 seconds average view duration** (3x–7x longer than native XHS templates) and first organic follower.
- **5 Root Causes Why Impressions Capped (<1,200) and Comments = 0**:
  1. **Anti-Spam Throttle Triggered (`私信 / 私聊`)**: `261018-01` image (`后台私信“问诊”`) and `261021-01` text/slide 8 (`留言或私聊` / `私信留下`) triggered XHS commercial traffic throttling on a non-Blue-V/early account, dropping subsequent impressions to `299–751`.
  2. **Zero-Comment Trap (CES Algorithm Bottleneck)**: XHS weights 1 Comment = 4 Likes (`CES = Like×1 + Save×1 + Comment×4 + Share×4`). With `Comments = 0`, the algorithm refuses to push a post from the 500-view base pool to the 5,000-view pool, even with 16.6% CTR and 99s dwell time.
  3. **High-Friction CTA**: Asking students to paste *"100-word essay openings"* or *"currently stuck paragraph logic"* in public comments has massive psychological friction. Must switch to **3-second low-friction comment triggers** (e.g., *"评论区打【港三】或留【均分+目标专业】"*).
  4. **Content Type Bias (100% Essay Theory = High Saves, Zero Comments)**: All 4 posts were pure essay-writing lectures (which users silently bookmark `收藏` to read later). **School Selection / GPA Positioning & Multi-Country Timeline posts** are what drive comments (`评论`).
  5. **Brand Inconsistency & Slide Order**: `261021-01` had `大熙教育` on Slide 1 footer but `以立工作室` on Slide 8 footer; `261018-01` had `01.jpg` and `06.jpg` reversed; `261021-01` showed Chinese-only PS excerpts instead of real English PS sentences with Chinese critique.

---

### `[2026-10-31 16:26] Entry #08 — Blue-V Organic Mechanics & 4-Template Visual A/B Testing Library`
- **Clarification on 600 RMB Enterprise Verification (专业号/蓝V)**:
  - Having a verified Blue-V account prevents account bans and unlocks **Comment-to-DM initiation (评论区主动私信追粉)**.
  - However, putting `"后台私信 / 私聊"` inside images/body still triggers XHS's **Commercial Ad Filter** (throttling free organic traffic to ~300 views to push paid 聚光 ads) and bypasses public comments (`CES +4 pts`).
  - **Updated Rule**: Drive **low-friction public comments** on the post → boost free organic impressions → use Blue-V Comment-to-DM feature to message every commenter privately.
- **Visual A/B Testing Setup (2 Posts / Day)**:
  - Since 4 posts is too small a sample to crown a single visual template, created a **4-Template A/B Testing Library** in `templates/` (with a side-by-side preview gallery at `templates/index_preview.html`):
    - `Template_A`: Warm Editorial (`template_A_editorial_light.html`)
    - `Template_B`: Executive Navy (`template_B_executive_navy.html`)
    - `Template_C`: Upgraded iOS Notes (`template_C_apple_notes.html`)
    - `Template_D`: High-Contrast Tier Matrix (`template_D_matrix_scorecard.html`)

---

### `[2026-10-31 16:29] Entry #09 — Time-Series Roll-Up Tracking Architecture (Solving Cumulative Stat Bias)`
- **Problem Identified**: Xiaohongshu stats are cumulative roll-ups over time. Comparing a 13-day-old post (`261018-01`) directly against a 1-day-old post without `snapshot_date`, `publish_date`, and `age_days` distorts A/B testing and hides long-tail search traffic.
- **Solution Implemented in `tracker/`**:
  1. [`tracker/posts_master.csv`](file:///Users/bjtiew/GitHub/XHS%20Posts/tracker/posts_master.csv) — **1 Row per Post**: Stores permanent metadata (`publish_date`, `visual_template`, `cta_type`) + latest roll-up state.
  2. [`tracker/metrics_snapshots.csv`](file:///Users/bjtiew/GitHub/XHS%20Posts/tracker/metrics_snapshots.csv) — **Append-Only Time-Series Checkpoints**: Records `snapshot_date`, `publish_date`, `age_days`, `delta_impressions`, and `velocity_imp_per_day` at standard checkpoints (`T+24h`, `T+48h`, `T+7d`) so we can compare posts at identical ages and detect long-tail search growth.
  3. Updated [`tracker/performance_log.csv`](file:///Users/bjtiew/GitHub/XHS%20Posts/tracker/performance_log.csv) to include `snapshot_date`, `publish_date`, `age_days`, and `velocity_imp_per_day`.

---

### `[2026-10-31 16:33] Entry #10 — Generated Day 1 A/B Test Pair (261031-01 & 261031-02)`
- **Slot 1 (`posts/261031-01/`)**:
  - **Template**: `Template_D_Matrix_Scorecard` (High-Contrast Red/Black Tier Table)
  - **Pillar & Topic**: `Pillar_3_Multi_Country_Matrix` — *"均分75/80/85+，7国联申选校梯度表"* (Covers all 7 destinations UK/US/HK/SG/MY/AUS/NZ across 3 GPA bands + how to adapt PS across regions).
  - **Hypothesis**: Positioning matrix + 3-second low-friction comment CTA (`【本科院校档次 + 目前均分 + 意向地区】`) will break the `0 comment` bottleneck.
- **Slot 2 (`posts/261031-02/`)**:
  - **Template**: `Template_C_Apple_Notes` (Upgraded iOS Notes with yellow highlights & green/red English comparison boxes)
  - **Pillar & Topic**: `Pillar_2_PS_Teardown` — *"改完50篇文书：这3种自杀式写法快停下"* (Includes authentic English Before/After excerpts + high-value verb replacement sheet).
  - **Hypothesis**: Combines the high initial impression reach of iOS Notes (`261018-01`) with the 99s deep read time of concrete Before/After examples (`261021-01`).

---

### `[2026-10-31 16:48] Entry #11 — Dual-Track Persona Anchoring (高申本 vs. 本申硕) & Long-Tail SEO Strategy`
- **Problem Identified**:
  1. Mixing `高申本` (high school to undergrad) and `本申硕` (bachelor's to master's) or omitting the stage label on Slide 01 prevents readers from self-identifying in 0.5 seconds.
  2. Literary titles without search keywords miss Xiaohongshu's highest-converting traffic source: **Long-Tail Search SEO (搜索长尾流)**.
- **Strategic Upgrade Locked into `config/brand_constraints.md` & `SKILL.md`**:
  - **Daily Dual-Track Split**:
    - **Post 01 (`261031-01` — Noon)**: Strictly **`【本申硕专栏】`** (University GPA `75/80/85+`, `双非/211/985`, Master's multi-country positioning & PS).
    - **Post 02 (`261031-02` — Evening)**: Strictly **`【高申本 & 家长专栏】`** (High School `普高高考 / A-Level / IB / AP`, 7-country undergrad pathways, high-school English PS Before/After, and parent budget table).
  - **Three-Layer Long-Tail SEO Rule**: Every note title (`<=20` chars) must follow `[阶段锚点]｜[背景/分数长尾词]+[地区/动作长尾词]` and embed long-tail keywords in the first 50 chars of the body.

---

### `[2026-10-31 17:06] Entry #12 — Integrated Guizang Design System (op7418/guizang-social-card-skill)`
- **Problem Identified**: Earlier custom HTML/CSS slides looked like cramped web tables ("网页感太重").
- **Solution Implemented**:
  - Cloned and installed [`op7418/guizang-social-card-skill`](file:///Users/bjtiew/GitHub/XHS%20Posts/.agent/skills/guizang-social-card-skill/SKILL.md) into `.agent/skills/guizang-social-card-skill/`.
  - Re-built [`posts/261031-01/index.html`](file:///Users/bjtiew/GitHub/XHS%20Posts/posts/261031-01/index.html) (`【本申硕专栏】`) using Guizang's **Swiss International (`template-swiss-card.html`, theme `ikb`)**: extreme font-weight contrast (`weight 200` display headlines + `Inter` / `Noto Sans SC` / `JetBrains Mono`), stacked ledger, 6-cell matrix + hero ratio `2:3:1`, horizontal bar chart, and Lucide icons.
  - Re-built [`posts/261031-02/index.html`](file:///Users/bjtiew/GitHub/XHS%20Posts/posts/261031-02/index.html) (`【高申本 & 家长专栏】`) using Guizang's **Editorial Magazine × E-ink (`template-editorial-card.html`, theme `ink-classic`)**: real WebGL `ink-flow` contour wash + paper grain texture, `Playfair Display` + `Noto Serif SC` + `IBM Plex Mono`, tall ledger, and Before/After English PS comparison.
  - Rendered all 12 cards (`1080×1440`) via `node scripts/render.mjs` with automatic Google Font subsetting/embedding and exported both `.png` (`output/xhs-01.png`–`xhs-06.png`) and `.jpg` (`01.jpg`–`06.jpg`).

---

### `[2026-10-31 19:28] Entry #13 — Content De-Duplication & 3-Step Scientific Single-Variable A/B Testing Architecture`
- **Root Problems Resolved**:
  1. **Eliminated Topic Repetition**: Removed repetitive Slide 05 PS Before/After cards that collided with Oct 18–21 posts (`261018-01`..`261021-01`, all 100% undergrad essay posts), moving the `7:3 Full-Service Loop` to the account homepage matrix level and replacing "7-country encyclopedia" posts with **Golden Medium-Slices (`黄金中切口`)**.
  2. **Established True Single-Variable A/B Testing (`三步解耦单变量实验法`)**:
     - **Funnel Metric Decoupling**: Cover/Title → `T+48h Cover CTR`; Inner Layout → `Avg View Sec & Save Rate`; Slide 06 CTA → `Comment Rate`.
     - **Sequential Sprints**: Sprint 1 (Days 1–6) freezes Title Syntax, Inner Layout, and Comment Hook to test **ONLY `Cover_A_Illustration` (CubeLV flat-vector poster) vs. `Cover_B_Typography` (Upgraded `261021` full-Chinese consulting typography card)**; Sprint 2 tests Title Formula; Sprint 3 tests CTA Hook.
     - **Matched Pain-Point Pairs (`同赛道·对称痛点上下篇`)**: Pairs identical pain points across consecutive days within the same time slot & persona track (`Pair_M1` UK vs HK/SG/AUS 78–83 pickup; `Pair_U1` 10–25W HK/MO/MY/NZ vs 30–50W UK/AUS/US undergrad bill).
- **Updated Governance & Delivered Day 1 Pair**:
  - Updated `config/brand_constraints.md`, `.agent/skills/daxi-daily-post/SKILL.md`, `tracker/posts_master.csv`, and `tracker/performance_log.csv` (`ab_sprint`, `ab_pair_id`, `test_variable`, `variant`).
  - Re-authored, audited, and rendered **`posts/261031-01/`** (`Pair_M1` Day 1 · `Cover_A_Illustration` · `本申硕捡漏｜双非78-83申英国好录清单`) and **`posts/261031-02/`** (`Pair_U1` Day 1 · `Cover_B_Typography` · `高申本算账｜10-25万港澳马纽本科账单`).

---

### `[2026-10-31 19:44] Entry #14 — Completed Day 2 Symmetrical Counterparts (261101-01 & 261101-02) for Matched Pairs Pair_M1 & Pair_U1`
- **Deliverables Completed**:
  1. **`posts/261101-01/` (`Pair_M1` Day 2 Noon `12:30` · `【本申硕专栏】` · `Cover_B_Typography`)**:
     - Title (`20` chars): `本申硕捡漏｜双非78-83申港新澳好录单` (symmetrical mirror of `261031-01` UK 78–83 pickup).
     - Content: HK PolyU/CityU/HKBU/EdUHK/Lingnan high-acceptance cross-disciplinary tracks + CET-6 (`450–490+`) direct filing; Australian Go8 `75–80` GPA drop-down into QS Top 20–40 (`USYD/UNSW/Monash/UQ`) without IELTS; Singapore NTU/SMU/Curtin SG pragmatic tracks; Nov language time-gap `2+2+2` lineup + Zoom English interview risk control.
     - Visual QA: Fixed 1-char orphan wraps on Slides `02`–`04`, verified zero banned/throttled substrings across `text.md` and `index.html`, exported `01.jpg`–`06.jpg` (`1080×1440`).
  2. **`posts/261101-02/` (`Pair_U1` Day 2 Evening `20:00` · `【高申本 & 家长专栏】` · `Cover_A_Illustration`)**:
     - Title (`20` chars): `高申本算账｜30-50万英澳美本科总账单` (symmetrical mirror of `261031-02` 10–25W HK/MO/MY/NZ bill).
     - Cover Illustration: Custom CubeLV-style UK/AUS/US campus + Big Ben/Sydney Opera House/Statue of Liberty vector poster (`cover_bg_west.jpg`) with 3-plank wooden signpost (`澳洲八大 →` / `← 英国3年制` / `← 美国前50`).
     - Content: Australia Go8 3-year undergrad (`95–125万` total, Gaokao `450–565` direct entry or Grade 11/12 GPA `75–80` non-Gaokao International Year 1); UK 3-year undergrad + 1-year Master's (`4年读完本硕 140–165万`); US flagship public (`UIUC/Purdue/UW-Madison 180–220万`) vs private Top 50 & sophomore transfer savings (`立省60–80万`); 4-row comparison table + Jan UCAS deadline risk control.
     - Visual QA: Fixed Slide `03`/`06` headline orphan wraps and Slide `05` footer single-line fit, verified zero banned substrings, exported `01.jpg`–`06.jpg` (`1080×1440`).
- **Tracker Sync**: Logged `261101-01` and `261101-02` in `tracker/posts_master.csv` and `tracker/performance_log.csv`, closing full matched pairs `Pair_M1` and `Pair_U1`.

---

### `[2026-10-31 21:30] Entry #15 — Buyer-Side Insider Depth & 2026 Factual Precision Re-Forge Across All 4 Sprint 1 Posts`
- **Root Diagnosis from Self-Audit**:
  - Earlier v1 inner cards (`02.jpg`–`05.jpg`) read too much like flat, rosy sales-brochure listings ("报菜名 / 只报喜不报忧") and contained 4 dangerous generalizations (`UCL/Edinburgh` conflated with `国际大一 IY1`; `六级申港硕` generalized beyond `港城大 CityU`; `曼大环发/CPM` mandatory IELTS-at-submission exception omitted from UK no-IELTS advice; outdated pre-hike HK/Macau/UK GBP `9.2+` budgets & unstated `加州社区转学 TAG` boundaries).
- **Governance & SOP Upgrade**:
  - Added **Rule 5 (`Anti-Brochure Buyer-Side Depth & 2026 Factual Precision`)** to `config/brand_constraints.md` and **Check 8 (`Anti-Brochure Insider Depth & 2026 Factual Precision`)** to `.agent/skills/daxi-daily-post/SKILL.md`.
- **Re-Forged All 4 Posts (`24` Cards `1080×1440` + `text.md` + 8-Point `critic_audit.md`)**:
  1. **`posts/261031-01/`**: Injected Manchester SEED tightened List & mandatory `IELTS 6.5(6.0)` at submission vs Warwick WMG 100% coursework/no-exam/no-IELTS rule, Leeds Design/Media faculty bypass, Bristol CS Conversion C/Java coding workload + individual Calculus/Stats grade check, and `财经双非` vs `公办二本/独立学院` Tier bifurcation.
  2. **`posts/261031-02/`**: Injected counter-intuitive public `澳门大学 (15–17万/年)` saving `~16万` over private `澳门科技大学 (19–23万/年)` + UM `110–120` English veto cutoff, real post-hike HK Top 8 `26–32万/年` (`17–19.8万 HKD` + `8万` rent) vs `20–24万` Lingnan/EdUHK/HKMU boundary, Malaysia July post-Gaokao authentication `+6 months` delay to March intake & strict CGPA warning, and NZ Gaokao direct entry (`3 yrs / 68–78万`) vs Foundation (`4 yrs / 90–100万`).
  3. **`posts/261101-01/`**: Clarified ONLY `港城大 (CityU)` broadly accepts CET-6 (`450–520`) for English-taught Master's (while `浸会/教大/岭南` mainstream business/media require IELTS/TOEFL), USYD arithmetic mean vs Melbourne/UQ credit-weighted GPA (`3–5分` gap), `1–1.5年制` cost savings vs `2年制` statutory Australian PSW work-visa rule, and honest domestic Tier-1 HR/选调生 screening gap between `Curtin/JCU SG` branch campuses and Australian Go8 main campuses.
  4. **`posts/261101-02/`**: Updated UK Red Brick budgets to `2026` GBP `9.2+` (`38–46万/年`, London G5 `52–65万/年`, `3+1` 4-yr Bachelor+Master `155–180万`), separated `UCL (UPC exam+interview) / Edinburgh / Manchester` Foundation-only (`4 yrs`) from `Leeds / Exeter / Newcastle` International Year 1 (`3 yrs`) + `80%+` Gaokao Math cutoff, highlighted `UNSW (QS 19) / Monash` Diploma saving `35万` over Melbourne/Sydney Foundation, and drew the exact California Community College `TAG 达标直转协议` boundary (`UCI/UCD/UCSB` covered vs `UCB/UCLA/UCSD` excluded, requiring `GPA 3.85–4.0`).

---

## Weekly Retrospective Template (Copy at End of Each Week)

```markdown
### [YYYY-MM-DD] Weekly Review — Week #XX
- **Posts Published**: X
- **Best Performing Post**: `post_XX` (CTR: X%, Comments: X, DMs: X) — Why it worked:
- **Worst Performing Post**: `post_YY` (CTR: X%, Comments: X) — What to delete/change:
- **Constraint / Prompt Updates Applied to `config/`**:
```

