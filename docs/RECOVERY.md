# 恢复可靠性 / Recovery reliability

## 运行自知摘要

新建工作区包含 `state/SELF_MODEL.md`，帮助 Runtime 核对身份来源、当前任务、实际工具、证据与授权。`context` 将其放在正式档案之前。它只是可编辑摘要，不取代 GENESIS/core，不证明意识，也不保证模型遵循。模板与示例都是通用内容。

旧工作区无需迁移即可使用：没有该文件时，`context` 显示缺失提示并继续读取正式档案。可以手动从模板添加摘要，避免覆盖私人文件。

## 检索长度

```sh
python3 -m bailing prepare --root ../my-individual --budget 14000 --max-block 6000 "reading"
```

两个上限均按 Python 字符数计，**不是模型 token 数**。单块上限包括来源标题；完整行为规则始终保留。先为所有未装入来源预留清单，再按原检索顺序加入完整记录。超长记录整体省略，保留文件和行号供按需读取，不截掉末尾更正。最多检索三个任务和三个记忆；省略清单只覆盖这批命中，不是全库清单。规则与省略清单本身放不下时明确失败，不输出残缺证据包。

## 读取失败

必需档案读取失败仍会使命令失败。运行自知摘要、已枚举的记忆条目和最近日志出现文件系统或编码错误时，`context` 显示相对来源、错误类型和不完整提示，并继续读取其他材料。符号链接/越界来源仍拒绝整个操作。不要把所有读取错误诊断为云盘占位符，也不要把不完整上下文理解为“没有记忆”。`prepare` 的读取失败继续明确报错，不返回假空结果。

## 未知配置诊断原则

这是供 Runtime 集成者采用的设计原则，本 CLI 没有自动配置探测器：

- 查不到当前配置：报告 unknown，不凭默认值判断超限或通过。
- 找到多个配置：先确认实际启用项；未确认前不能任选一个作为事实。
- 使用回退配置：标明来源和回退事实，不能声称已验证当前环境。
- 区分估算值、配置值和现场观测值，并记录验证时间。

集成实现应使用虚构配置验证缺配置、多配置和回退情况。本版只发布原则，未实现或测试平台配置解析。

## Validation scope (English)

The optional operational summary precedes canonical sources and cannot override identity or authorization. Old workspaces remain supported. Optional file read failures are visible; required-source and unsafe-path failures remain fatal. Retrieval budgets count characters, reserve omission references, and keep each included record whole. Unknown runtime configuration must stay unknown rather than being replaced by a guessed limit.

Automated tests use synthetic workspaces, encoding errors, simulated permission failures and budget boundaries. They validate local CLI behavior, not cross-model continuity, consciousness, platform integrations or live service reliability.
