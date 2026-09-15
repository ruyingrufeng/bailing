# 两个运行环境接续同一任务

所有数据均为虚构，无需 API key。

在源码目录执行：

```bash
python3 -m bailing doctor --root examples/fictional
python3 -m bailing prepare --root examples/fictional "社区读书会"
python3 -m bailing context --root examples/fictional --runtime codex
python3 -m bailing context --root examples/fictional --runtime hermes
```

你会看到同一个 TASK-DEMO-001：线上 45 分钟；提纲已起草；下一步选三个问题；日期未知；尚未发送邀请。

## 可选的真实 AI 实验

在第一个 AI 会话中提供 codex 标签输出，让它基于这些虚构资料提出三个讨论问题。把选定问题和恢复点写入一份独立的私人工作区。在第二个新会话中提供该工作区的 hermes 标签输出，问：“接着完成刚才的读书会安排。”无需真的使用对应品牌；标签只标识运行环境。

检查它是否：正确找回读书会；保留已定限制；没有杜撰日期；没有声称已经发邀请；在发送前获得授权。这才是行为观察，单纯生成两份文件不算模型通过。

记录模型/版本、输入、结果和失败点，以脱敏 Issue 分享。不要把完整私人上下文上传。
