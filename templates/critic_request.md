# 送审消息模板（编排器 → daxi-supervisory-critic）

```
请审核以下帖子。逐篇给出结论，每篇结论的格式必须是：

POST: <post_id>
VERDICT: APPROVED 或 VERDICT: VETO_REJECT
AUDITED_HASH: <下面给你的该帖 content_hash，原样回写>
（然后是逐条检查清单与证据）

待审帖子：
- <绝对路径>/posts/<post_id_1>   content_hash = <preflight 输出的 16 位哈希>
- <绝对路径>/posts/<post_id_2>   content_hash = <...>

规则文件：<绝对路径>/config/brand.md、config/editorial.md、config/rules.json
当期实验：<绝对路径>/experiments/sprint_<n>.md
```

复审时：只发生变化的帖子重新给出**新 content_hash**，并列出本轮修改点。
