# 找回历史：归档检索

v0.2.0 新增只读 `archive-search`。它检索你主动放入私人工作区的 Markdown 归档，不读取模型账户或自动抓取会话，也不会把命中记录升级为正式记忆。

## 立即体验（全为虚构）

```bash
python3 -m bailing archive-search "社区读书会" --root examples/fictional
python3 -m bailing archive-search "reading" --root examples/fictional --runtime hermes --since 2026-01-02 --until 2026-01-02 --session followup --json
```

第一条可找到旧安排和后续修正；第二条筛选出后续虚构会话：时长由45分钟改为30分钟。日期仍未知。检索分数只表示词项相关性，不能决定哪条事实当前有效；应读取来源和后续修正。

## 添加自己的记录

在私人工作区创建 `memory/archive/`，只放你有权保留、并决定用于检索的资料。允许子目录，例如 `2026/01/`。文件名格式：

```text
YYYY-MM-DD-runtime-session.md
2026-01-02-hermes-reading-followup.md
```

日期必须有效；runtime 使用小写字母开头，可含数字或下划线。session 是剩余完整文件名部分，不猜测内部 UUID。过滤 `--runtime` 为精确匹配，`--session` 为区分大小写的子串匹配，日期上下界均包含当天。文件日期来自名称，不是系统修改时间。

正文可按下面格式分轮；也兼容 `### 百灵 · ` 标题。没有这些标题时按整份文件检索。

```markdown
# Synthetic example

### user · 2026-01-02T09:00:00Z
The reading session should last 30 minutes.

### assistant · 2026-01-02T09:01:00Z
The date remains undecided.
```

新初始化的工作区自带归档说明；v0.1.0 的旧工作区只需自己创建目录，不用重新 init，也不覆盖已有档案。

## 结果与边界

- 默认输出最多8项，`--limit` 支持1–50。命中带相对路径、1起始行号、运行环境、日期及会话标识。
- 文本模式提供短摘录；`--json` 返回命中的完整消息块，请在交给其他人或云服务前检查内容。
- 无法读取、非UTF-8、命名无效的 Markdown 和符号链接会列为跳过项。空结果不代表历史事件不存在；也可能是关键词不匹配或源文件被跳过。
- 不跟随符号链接目录；这是单写入者本地工具，不是针对恶意并发修改的安全沙箱。
- 仍采用词项检索（BM25），没有语义向量搜索、永久索引、自动压缩或跨轮上下文扩展。需要时按行号读取前后文。
- `prepare` 仍只查正式记忆和任务；`context` 不自动装入原始归档。
- 不会清除归档中的秘密。隐私筛选由使用者在放入资料与分享输出前完成。
