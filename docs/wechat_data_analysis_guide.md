# 从微信到 LakeSkill：WeChatDataAnalysis 完整流程

用 [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) 解密微信聊天记录，再导入 LakeSkill 做证据型关系分析。

## 前置条件

| 条件 | 说明 |
|---|---|
| 操作系统 | Windows |
| 微信版本 | 4.x（已登录） |
| Python | 3.10+（仅源码运行需要） |

## 第一步：获取解密密钥

WeChatDataAnalysis 需要微信数据库的解密密钥。推荐使用 [wx_key](https://github.com/ycccccccy/wx_key)：

1. 下载 wx_key 工具
2. 运行获取微信 4.x 数据库密钥
3. 复制密钥备用

> 密钥是敏感信息，不要泄露给他人，不要上传到任何公开仓库。

## 第二步：安装 WeChatDataAnalysis

### 方式 A：下载 EXE（推荐）

1. 打开 [Release 页面](https://github.com/LifeArchiveProject/WeChatDataAnalysis/releases/latest)
2. 下载 `WeChatDataAnalysis.Setup.<version>.exe`
3. 运行安装，启动 `WeChatDataAnalysis`

> Windows 可能弹出"未知发布者"提示，确认来源为本仓库后选择"仍要运行"。

### 方式 B：从源码运行

```bash
git clone https://github.com/LifeArchiveProject/WeChatDataAnalysis.git
cd WeChatDataAnalysis
uv sync
cd frontend && npm install
# 启动后端
uv run main.py
# 启动前端（另一个终端）
cd frontend && npm run dev
```

访问 http://localhost:3000。

## 第三步：解密并浏览聊天记录

1. 启动 WeChatDataAnalysis
2. 输入第一步获取的解密密钥
3. 等待解密完成
4. 在界面中浏览、搜索目标聊天记录

## 第四步：导出聊天记录

WeChatDataAnalysis 支持三种导出格式：

| 格式 | 说明 | LakeSkill 兼容性 |
|---|---|---|
| **TXT** | 纯文本聊天记录 | ✅ 直接导入（`--type txt`） |
| **JSON** | 结构化消息数据（含元数据） | ⚠️ 需要字段映射（见下方说明） |
| **HTML** | 离线浏览页面 | ❌ 不支持导入 |

**推荐导出 TXT 格式**，最简单直接。

### 导出步骤

1. 在 WeChatDataAnalysis 界面选择目标聊天
2. 点击"导出聊天记录"
3. 选择 TXT 格式
4. 保存到本地目录

## 第五步：导入 LakeSkill

### 方式 A：TXT 导入（推荐）

```bash
lake-skill ingest --file 导出的聊天记录.txt --type txt --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
```

`--self-name` 填你在聊天中的称呼（通常是"我"或你的微信昵称），`--target-name` 填对方的称呼。

### 方式 B：SQLite 直接读取

WeChatDataAnalysis 解密后的数据库是明文 SQLite。LakeSkill 的 SQLite adapter 可以自动检测 schema 并读取：

```bash
lake-skill ingest --file 解密后的数据库.db --type sqlite --out work/raw_messages.jsonl
```

> SQLite 文件通常在 WeChatDataAnalysis 的数据目录中。具体路径取决于你的安装方式。

### 方式 C：直接粘贴

如果只需要分析一小段聊天，可以直接粘贴给 agent：

```text
使用 lake-skill，帮我分析这段聊天记录。我的目标是知道下一步怎么做。

[粘贴聊天内容]
```

## 第六步：后续处理

导入后，按标准管线处理：

```bash
# 脱敏
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe

# 分段
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl

# 数据体检
lake-skill doctor --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work

# 打包上传
lake-skill bundle --source work --out upload_bundle
```

然后把 `upload_bundle` 里的文件上传给 agent，说：

```text
使用 lake-skill，读取这些本地预处理产物。请先给湖镜行动卡，再给完整报告。
```

## 隐私提醒

- WeChatDataAnalysis 解密的数据包含**个人隐私**
- 导入 LakeSkill 前先运行 `redact` 脱敏
- 不要上传原始数据库、未脱敏数据、截图或语音
- 公开展示只用 `lake-skill demo` 生成的合成数据
- 密钥不要泄露，不要提交到 git

## 常见问题

| 问题 | 解决 |
|---|---|
| wx_key 获取不到密钥 | 确认微信版本为 4.x，且已登录 |
| WeChatDataAnalysis 启动失败 | 检查端口 10392 是否被占用 |
| 导入 LakeSkill 后消息乱码 | 运行前设置 `PYTHONUTF8=1` |
| SQLite 导入找不到表 | LakeSkill 会自动检测消息表，确认数据库已解密 |
| 消息只有单方 | 检查 `--self-name` 是否匹配聊天中的称呼 |
