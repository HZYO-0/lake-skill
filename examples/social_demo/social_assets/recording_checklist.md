# 录屏检查清单

> 合成示例专用。录屏前关闭私有聊天、私有路径和无关窗口。

- [ ] 生成 demo：`lake-skill demo --out examples/social_demo`
- [ ] 打开 synthetic CSV：`examples/social_demo/synthetic_chat.csv`
- [ ] 打开行动卡：`examples/social_demo/social_action_card_demo.md`
- [ ] 展示证据 ID：例如 `E-20260108-001`
- [ ] 展示置信度和反证：行动卡中的"置信度：低到中"
- [ ] 运行 doctor 三档：`lake-skill doctor --messages examples/social_demo/work/messages.redacted.jsonl --sessions examples/social_demo/work/sessions.redacted.jsonl --out examples/social_demo/work`
- [ ] 展示 bundle 结果：`examples/social_demo/upload_bundle/upload_readme.md`
- [ ] 运行 check-leaks：`lake-skill check-leaks examples/social_demo`
- [ ] 检查画面中没有真实微信 ID、真实聊天、真实路径或可识别个人信息
- [ ] 旁白和字幕匹配录屏脚本时间线
