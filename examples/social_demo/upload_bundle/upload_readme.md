# LakeSkill Upload Bundle

本文件夹是上传给 LakeSkill Skill 的预处理材料。

## 可以上传

- `digest.redacted.md`
- `sessions.redacted.jsonl`
- `evidence.redacted.jsonl`
- `lakeskill_intake.yaml`
- `lakeskill_intake.md`

## 不要上传原始聊天记录

- 上传前确认材料已脱敏，并已经运行 `lake-skill check-leaks <bundle_dir>`。
- 不要上传原始 `.db`、未脱敏 `.csv/.txt/.jsonl`、截图或语音文件。
- 不要上传原始数据库、聊天截图、语音、身份证件、联系方式或定位信息。
- 不要上传未获授权的第三方隐私材料。
- 不要把本文件夹用于公开展示；公开展示请使用 `lake-skill demo` 生成的合成示例。

## 风险与未成年人提示

- 如材料涉及危机、自伤、伤害他人、被威胁、被跟踪或现实暴力风险，请停止上传，并优先联系现实支持系统、当地紧急服务或合格专业帮助。
- 如材料涉及未成年人，不要用于亲密陪伴、关系推进或依赖型互动建议。

## 建议提示词

```text
使用 lake-skill，读取这些本地预处理产物。请先给湖镜行动卡，再给完整报告。
如果证据不足，请输出低置信度草案，不要做确定性判断。
```
