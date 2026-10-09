# Changelog

## 0.3.0 — Recovery reliability

- Add an optional operational self-model template and load it before canonical context.
- Reserve omission references in prepare; expose character and per-block budgets.
- Report optional context read failures while retaining fatal core/unsafe-path checks.
- Document unknown-configuration diagnostics as design guidance only.
- Add seven synthetic recovery regression tests.

## 0.2.0 — 找回历史

- 新增只读 archive-search：日期、Runtime、会话过滤，来源行号与 JSON 输出。
- 无效/不可读归档与符号链接显式报告，不静默伪装成完整搜索。
- 虚构案例展示旧安排与后续修正；新增归档格式及旧工作区升级说明。
- 补充按当前 Runtime 可用能力选择执行通道的原则。
- 不增加会话抓取、自动回写或后台任务，不包含私人归档。

## 0.1.0 — 初始探索版

- 从百灵私人实践整理的独立公开版本，全新历史。
- 身份、状态、任务、记忆、经历和身份变化协议模板。
- 初始化、检查、上下文、记录与行动前证据检索命令。
- 虚构读书会演示、中英文入口、贡献与隐私说明。
- 尚未验证真实模型的跨会话行为；无自动运行环境接入。
