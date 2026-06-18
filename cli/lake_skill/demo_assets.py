"""Synthetic demo package generation for LakeSkill promotion and onboarding."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

from .evidence.indexer import index_evidence, save_evidence_index
from .intake_io import save_intake_md, save_intake_yaml
from .jsonl_utils import write_jsonl_models
from .reports.digest import generate_digest
from .schema import IntakeCard, Message, MessageType, Modality, SenderRole, WorkMode
from .segmentation.sessionizer import segment_sessions


def synthetic_messages() -> list[Message]:
    """Return a small, fully synthetic chat for public demos."""
    start = datetime(2026, 1, 8, 21, 10)
    rows = [
        (0, SenderRole.SELF, "最近感觉你回得少了，我是不是哪里让你有压力？"),
        (6, SenderRole.TARGET, "没有，就是这几天事情比较多。"),
        (18, SenderRole.SELF, "那我不追问了，你忙完再说。"),
        (65, SenderRole.TARGET, "昨天你说的那个资料还有吗？"),
        (68, SenderRole.SELF, "有，我发你。你先用，不急着回我。"),
        (95, SenderRole.TARGET, "谢谢，最近确实有点累。"),
        (98, SenderRole.SELF, "收到。那我先正常发资料，不把情绪压给你。"),
        (145, SenderRole.TARGET, "嗯，这样会舒服一点。"),
        (165, SenderRole.SELF, "那我们还是慢慢来，不急着定义关系。"),
        (170, SenderRole.TARGET, "对，慢慢来比较好。"),
    ]
    return [
        Message(
            message_id=f"demo-{idx:03d}",
            conversation_id="demo-conversation",
            source_type="synthetic",
            timestamp=start + timedelta(minutes=minutes),
            sender_role=role,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=text,
            text_redacted=text,
        )
        for idx, (minutes, role, text) in enumerate(rows, 1)
    ]


def write_synthetic_csv(messages: list[Message], output_path: Path) -> None:
    """Write the synthetic demo chat as a simple CSV users can inspect."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sender", "content"])
        for message in messages:
            sender = "我" if message.sender_role == SenderRole.SELF else "TA"
            writer.writerow([message.timestamp.strftime("%Y-%m-%d %H:%M:%S"), sender, message.text])


def generate_social_action_card(output_path: Path) -> None:
    """Write a public-safe action-card example for README and social posts."""
    output_path.write_text(
        """# LakeSkill 湖镜行动卡 Demo

> 合成示例，仅用于 README、小红书、抖音录屏。不要用真实聊天记录做公开素材。

## 先看这个：湖镜行动卡（关系行动卡）

### 当前局势
对方没有切断互动，但情绪确认问题上保持低展开。样本显示更适合低压稳定，而不是继续追问关系定义。

证据：E-20260108-001
置信度：中。该示例包含一次压力表达、一次求助和一次关系节奏讨论，但仍是短样本。

### 当前策略
**低压稳定**

为什么是这个策略：对方在“事情比较多”之后仍主动求助，并接受“不急着回我”的降压表达；后续又明确说“慢慢来比较好”。这支持“降低压力、保持正常互动”，不支持“直接推进”或“冷落测试”。

### 本周 3 个动作
1. 对方求助时正常回应，帮完不追加情绪索取。
2. 情绪话题只说一次，不连续追问“你是不是不在乎”。
3. 如果对方继续主动开启日常话题，再轻微增加分享，不要求立刻表态。

### 不要做
- 不要把短回复直接解释成关系变差。
- 不要用冷落、试探或嫉妒诱导测试对方。
- 不要把分析结果发给对方要求其承认。

### 可直接发的话
“资料我发你。你先忙你的，不急着回，我只是想把事情说清楚，不想给你压力。”
""",
        encoding="utf-8",
    )


def generate_audit_demo_files(output_dir: Path) -> None:
    """Write a minimal auditable synthetic ledger and report."""
    ledger_record = {
        "evidence_id": "E-20260108-001",
        "date": "2026-01-08",
        "speaker": "target",
        "tier": "T1",
        "signal_type": "relationship_pacing",
        "quote": "对，慢慢来比较好。",
        "local_context": "双方讨论是否急着定义关系。",
        "later_followup": "公开 demo 样本到此结束，不作长期推断。",
        "interpretation_candidates": ["对方接受低压节奏", "短样本不足以支持长期关系判断"],
    }
    (output_dir / "relationship_signal_ledger.jsonl").write_text(
        json.dumps(ledger_record, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "lakeskill_report_demo.md").write_text(
        """# LakeSkill 关系分析报告

**分析对象**: 我 ↔ TA
**数据范围**: 2026-01-08 至 2026-01-08
**总消息量**: 10 条
**抽样说明**: 全量合成示例
**分析覆盖**: 仅覆盖一个短场景，不支持长期关系模式判断。
**结论状态**: 低置信度草案

## Layer -1: 湖镜行动卡（关系行动卡）

当前策略：低压稳定。证据：E-20260108-001。

## Layer 0

短样本只能说明当前对话更适合低压节奏。

## Layer 1

双方在关系节奏上出现“慢慢来”的明确表达。证据：E-20260108-001。

## Layer 2

对方画像暂不展开，样本不足。

## Layer 3

自我画像暂不展开，样本不足。

## Layer 4

互动模式暂不展开，样本不足。

## Layer 5

依恋信号暂不展开，样本不足。

## Layer 6

建议只使用低压表达，不连续追问关系定义。

## Layer 7

该合成示例缺少长期时间线、冲突修复和多场景覆盖。

## Reliability Audit

**关系信号台账**: PASS
**T1 覆盖**: PASS
**T4 覆盖 T1 检查**: PASS
**单因子断言检查**: PASS
**人格画像反证检查**: PASS
**结论状态**: 低置信度草案
""",
        encoding="utf-8",
    )


def generate_social_assets(output_dir: Path) -> None:
    """Write public-safe Xiaohongshu and Douyin recording assets."""
    assets_dir = output_dir / "social_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    (assets_dir / "xiaohongshu_carousel.md").write_text(
        """# 小红书长图脚本：LakeSkill 湖镜行动卡

> 合成示例。仅用于公开教程、录屏和图文排版，不包含真实聊天。

## Page 1

标题：TA 回得慢 = 不在乎？先别急着下结论。

副标题：一个开源工具，把聊天证据整理成行动卡，不替你猜 TA 的心。

## Page 2

你有没有过这种时刻？

TA 回复变慢了，你开始反复翻聊天记录，想找到一个确定答案。

但 AI 说得越肯定，你越焦虑。

## Page 3

LakeSkill 不一样。

它的第一屏不是人格分析，而是一张行动卡：

现在该稳住、修复、轻推，还是先回到自己。

## Page 4

每条建议都能追到证据 ID。

合成示例：E-20260108-001 支持"低压稳定"，不支持继续追问关系定义。

置信度、反证、替代解释——全标出来。

## Page 5

如果证据不够，它会降级，而不是把话说满。

数据体检分三档：只能局部观察 / 可出行动卡 / 可出完整报告。

## Page 6

隐私优先：本地脱敏、数据体检、打包，确认安全再上传。

公开展示只用合成数据，不用真实聊天。

## Page 7

CTA：GitHub 搜「LakeSkill 湖镜」，装好 Skill，粘一段聊天试一次。

AI 不该替你脑补关系答案。它只做一件事：把证据整理成你能用的行动卡。
""",
        encoding="utf-8",
    )

    (assets_dir / "xiaohongshu_caption.md").write_text(
        """# 小红书正文草稿

> 合成示例。公开发布前请只配 `lake-skill demo` 生成的截图。

你有没有把聊天记录丢给 AI，让它帮你判断"TA 到底怎么想"？

AI 回得很快、很肯定，但你越看越焦虑——因为它说得太像真的了。

LakeSkill 湖镜做的是更克制的事：它不替你猜 TA 的心，只把聊天证据整理成一张行动卡。

每条建议都有三个东西：

1. 证据 ID——你能在聊天记录里找到原话。
2. 置信度——它知道自己的判断有多可靠。
3. 反证和替代解释——它不只给你一个答案。

如果证据不够，它会降级：只给低风险观察，不给完整判断。

想试试？GitHub 搜「LakeSkill 湖镜」，装好后粘一段聊天就行。

公开演示只用合成数据，不用真实聊天。

标签建议：#AI工具 #聊天分析 #关系行动卡 #隐私保护 #开源项目 #LakeSkill
""",
        encoding="utf-8",
    )

    (assets_dir / "douyin_recording_script.md").write_text(
        """# 抖音录屏脚本：35 秒 LakeSkill Demo

> 合成示例。录屏只展示 `examples/social_demo`，不要展示真实聊天或本地私有路径。

## 0-3s（钩子）

画面：屏幕中央大字「TA 回得慢 = 不在乎？」，3 秒后打出红色叉号。

旁白：把聊天记录丢给 AI，最怕它说得太肯定。

字幕：AI 说得越肯定，你越焦虑。

## 3-8s（引出工具）

画面：终端运行 `lake-skill demo --out examples/social_demo`。

旁白：我做了一个不一样的工具：它不猜 TA 的心，只整理证据。

字幕：不猜心，只整理证据。

## 8-15s（展示输入）

画面：打开 `synthetic_chat.csv`，展示"我 / TA / 时间"三列。

旁白：粘一段聊天，它先回到时间线，再找证据。

字幕：聊天先回到时间线。

## 15-25s（展示核心输出）

画面：打开 `social_action_card_demo.md`，放大"当前策略""证据 ID""不要做"。

旁白：第一屏不是长报告，是行动卡：该做什么、不要做什么、证据在哪。每条都能追到原话。

字幕：行动卡 = 动作 + 边界 + 证据 ID。

## 25-35s（CTA）

画面：打开 `work/data_readiness.md` 和 `upload_bundle/upload_readme.md`。

旁白：上传前先做数据体检，再用 bundle 打包。GitHub 搜「LakeSkill 湖镜」，装好粘一段聊天试一次。

字幕：GitHub 搜 LakeSkill 湖镜。
""",
        encoding="utf-8",
    )

    (assets_dir / "recording_checklist.md").write_text(
        """# 录屏检查清单

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
""",
        encoding="utf-8",
    )


def generate_demo_package(output_dir: Path) -> None:
    """Generate a complete synthetic demo package."""
    work_dir = output_dir / "work"
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    messages = synthetic_messages()
    sessions = segment_sessions(messages, time_gap_hours=6.0)
    evidence = index_evidence(messages, sessions)

    write_synthetic_csv(messages, output_dir / "synthetic_chat.csv")
    write_jsonl_models(work_dir / "messages.redacted.jsonl", messages)
    write_jsonl_models(work_dir / "sessions.redacted.jsonl", sessions)
    generate_digest(messages, sessions, str(work_dir / "digest.redacted.md"))
    save_evidence_index(evidence, str(work_dir / "evidence.redacted.jsonl"))

    card = IntakeCard(
        relationship_type="ambiguous",
        status="short synthetic demo",
        self_name="我",
        target_name="TA",
        duration="synthetic sample",
        goal="生成行动卡演示",
        data_source="synthetic csv",
        privacy_mode="publish-safe",
        work_mode=WorkMode.PRACTICAL,
        scene_summary="合成短样本：压力表达、求助、降压回应、慢慢来。",
    )
    save_intake_yaml(card, output_dir / "lakeskill_intake.yaml")
    save_intake_md(card, output_dir / "lakeskill_intake.md")
    generate_social_action_card(output_dir / "social_action_card_demo.md")
    generate_audit_demo_files(output_dir)
    generate_social_assets(output_dir)
