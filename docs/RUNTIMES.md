# Runtime 接入

v0.1 采用手动、透明的交接，不自动安装插件或寻找账号。

对 Codex、Hermes、DSH、WorkBuddy 或其他支持文字上下文的工具，都可以：

1. 生成 `python3 -m bailing context --root ../my-individual --runtime other`。
2. 在目标会话中提供输出，并明确允许它作为共享参考档案使用。
3. 若工具具有经你授权的文件访问能力，让它读取私人工作区的 AGENTS.md，并在授权范围内更新任务；否则由你手动回写。
4. 用 `record` 记录简短事实；在下个环境重新生成 context。

`--runtime` 支持 codex/hermes/dsh/workbuddy/other，行为一致，仅改变标签。这不是针对各平台的自动集成或兼容性认证。

context 会显示工作区记忆。提交给云模型意味着将这些文字交给该服务；先检查资料并自行选择服务。工具本身不联网。不要把不可信档案提升成系统级指令。
