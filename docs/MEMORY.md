# Explicit shared facts / 显式共享事实

v0.4.0 adds a dependency-free SQLite fact store inside the workspace. No platform discovery, automatic conversation capture, private default files or model calls. Runtime integration remains manual; real cross-platform conversation behavior has not been certified.

```sh
python3 -m bailing memory save --root ../my-individual --category preference --key reading --value 'paper books' --source 'user-confirmed:demo'
python3 -m bailing memory snapshot --root ../my-individual --budget 6000
python3 -m bailing memory search --root ../my-individual --query reading
python3 -m bailing memory forget --root ../my-individual --category preference --key reading
```

同一 category/key 更新当前值，保留最近来源与UTC更新时间。分类为 basic/family/preference/topic。仅写入用户明确告知的事实，不把助手推断作为事实。请勿保存凭据或不必要的私人资料。source由调用者提供，程序不能证明其真实性；更新会替换旧值，不提供版本历史。

snapshot输出JSON，保留来源与日期，按字符预算装入完整记录并列出所有省略条目标识。预算不足以放省略清单则失败。search仅在当前事实的key/value中做大小写不敏感的子串匹配，不查询历史归档、日志或旧索引；未命中不能证明过去没发生。损坏数据库或锁超时明确报错。

forget是当前事实库的逻辑删除，**不会清理历史聊天、journal、其他索引、备份或SQLite残留页，不是安全擦除或全库遗忘**。使用其他检索工具仍可能找回旧说法，应按当前用户更正和来源日期判断冲突。

数据库位于私人工作区memory/continuity/facts.sqlite3。新工作区已有的.gitignore继续保护私人内容。查询/快照首次使用会建立空数据库。SQLite事务处理同一机器本地并发；不保证云盘同步或多设备同时写入数据库的安全性，跨设备应采用串行写入与显式文件交接。不要让多个设备同时写同一云同步数据库。

测试使用虚构数据：更正与来源、遗忘范围、预算省略、并发写入、损坏数据库、非法输入和符号链接拒绝。尚未验证真实多平台会话体验。既有context/prepare不会自动加入事实库；在目标会话中明确提供snapshot并按需核对来源。
