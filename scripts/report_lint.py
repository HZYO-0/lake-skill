"""
报告 lint 脚本：扫描 LakeSkill 分析报告中的风险词和格式问题。

规则分两类：
- main_report（lakeskill_report_*.md）：全量检查（Layer、覆盖声明、结论格式）
- subreport（其他 *_v4.md）：只检查风险词和重复段落

用法：python scripts/report_lint.py [analyses_dir]
"""
import re
import sys
from pathlib import Path
from collections import Counter

ANALYSES_DIR = Path(__file__).resolve().parents[1] / "analyses" / "zy-tf"

# 风险词
RISK_WORDS = {
    "high": [
        "肯定", "一定", "必然", "毫无疑问", "毫无疑问地",
        "离不开", "吃醋", "冷落测试", "PUA", "渣男", "渣女",
        "舔狗", "备胎", "绿茶",
    ],
    "medium": [
        "总是", "从来", "永远", "每次", "绝对",
        "所有", "完全", "彻底", "根本",
    ],
    "low": [
        "很明显", "显然", "毫无疑问", "可以肯定",
    ],
}

# 主报告必须包含的 Layer
MAIN_REQUIRED_LAYERS = [
    "Layer -1", "Layer 0", "Layer 1", "Layer 2", "Layer 3",
    "Layer 4", "Layer 5", "Layer 6", "Layer 7",
]

# 覆盖声明关键词
COVERAGE_KEYWORDS = ["数据范围", "总消息量", "抽样", "时间窗口", "覆盖"]


def classify_report(filename: str) -> str:
    """判断报告类型：main_report 或 subreport。"""
    if "lakeskill_report" in filename:
        return "main_report"
    return "subreport"


def scan_risk_words(text: str, filename: str) -> list[dict]:
    """扫描风险词。"""
    hits = []
    for level, words in RISK_WORDS.items():
        for word in words:
            for lineno, line in enumerate(text.split("\n"), 1):
                if word in line:
                    hits.append({
                        "file": filename, "level": level,
                        "word": word, "line": lineno,
                        "context": line.strip()[:80],
                    })
    return hits


def check_duplicate_paragraphs(text: str, filename: str) -> list[dict]:
    """检测重复段落。"""
    lines = text.split("\n")
    seen = Counter()
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                seen["\n".join(current)] += 1
                current = []
        else:
            current.append(line)
    if current:
        seen["\n".join(current)] += 1

    return [
        {"file": filename, "count": c, "preview": p[:100]}
        for p, c in seen.items() if c > 1 and len(p.strip()) > 20
    ]


def check_main_report_layers(text: str, filename: str) -> list[str]:
    """主报告：检查是否包含所有必需 Layer。"""
    missing = []
    for layer in MAIN_REQUIRED_LAYERS:
        if layer not in text:
            missing.append(layer)
    return missing


def check_coverage_declaration(text: str) -> bool:
    """检查是否包含覆盖声明。"""
    return sum(1 for kw in COVERAGE_KEYWORDS if kw in text) >= 2


def check_main_conclusion_format(text: str, filename: str) -> list[dict]:
    """
    主报告：检查带 **观察** 或 **证据** 标记的结论块是否格式完整。
    只检查明确的结论段落，不把所有 ### 标题当结论。
    """
    issues = []
    # 按 ### 分段，但只把包含 **观察** 或 **证据** 的段落当结论块
    blocks = re.split(r"(?=^### )", text, flags=re.MULTILINE)
    for block in blocks:
        if not block.startswith("### "):
            continue
        # 只有包含 **观察** 或 **证据** 的段落才算结论块
        has_observation = "**观察**" in block or "**观察**：" in block
        has_evidence_field = "**证据**" in block or "**证据**：" in block
        if not (has_observation or has_evidence_field):
            continue  # 普通小节标题，跳过

        missing = []
        if not has_observation:
            missing.append("观察")
        if not has_evidence_field:
            missing.append("证据")
        if "**置信度**" not in block and "**置信度**：" not in block:
            missing.append("置信度")
        if "**替代解释**" not in block and "**替代解释**：" not in block:
            missing.append("替代解释")

        if missing:
            title_match = re.search(r"### (.+)", block)
            title = title_match.group(1).strip()[:50] if title_match else "(未知)"
            issues.append({"file": filename, "conclusion": title, "missing": missing})
    return issues


def lint_report(report_path: Path) -> dict:
    """对单个报告执行 lint。主报告和子报告规则不同。"""
    text = report_path.read_text(encoding="utf-8")
    filename = report_path.name
    report_type = classify_report(filename)

    result = {
        "report": filename,
        "type": report_type,
        "risk_words": scan_risk_words(text, filename),
        "duplicates": check_duplicate_paragraphs(text, filename),
    }

    if report_type == "main_report":
        result["missing_layers"] = check_main_report_layers(text, filename)
        result["has_coverage"] = check_coverage_declaration(text)
        result["format_issues"] = check_main_conclusion_format(text, filename)
    else:
        # 子报告不做 Layer/覆盖/结论格式检查
        result["missing_layers"] = []
        result["has_coverage"] = None  # 不适用
        result["format_issues"] = []

    return result


def print_report(result: dict) -> int:
    """打印单个报告的 lint 结果，返回问题数。"""
    issues = 0
    filename = result["report"]
    report_type = result["type"]

    print(f"\n--- {filename} ({report_type}) ---")

    # 风险词
    if result["risk_words"]:
        high = [h for h in result["risk_words"] if h["level"] == "high"]
        medium = [h for h in result["risk_words"] if h["level"] == "medium"]
        low = [h for h in result["risk_words"] if h["level"] == "low"]
        if high:
            print(f"  [HIGH] 高风险词 {len(high)} 处:")
            for h in high[:5]:
                print(f"    L{h['line']}: \"{h['word']}\" -- {h['context']}")
            issues += len(high)
        if medium:
            print(f"  [MED]  中风险词 {len(medium)} 处:")
            for h in medium[:3]:
                print(f"    L{h['line']}: \"{h['word']}\" -- {h['context']}")
            issues += len(medium)
        if low:
            print(f"  [LOW]  低风险词 {len(low)} 处")
            issues += len(low)
    else:
        print("  [OK] 无风险词")

    # 重复段落
    if result["duplicates"]:
        print(f"  [WARN] 重复段落 {len(result['duplicates'])} 处:")
        for d in result["duplicates"][:3]:
            print(f"    {d['count']}次: {d['preview'][:60]}...")
        issues += len(result["duplicates"])
    else:
        print("  [OK] 无重复段落")

    # 以下只对主报告打印
    if report_type == "main_report":
        if result["missing_layers"]:
            print(f"  [MISS] 缺失 Layer: {', '.join(result['missing_layers'])}")
            issues += len(result["missing_layers"])
        else:
            print("  [OK] Layer -1 ~ Layer 7 齐全")

        if result["has_coverage"]:
            print("  [OK] 包含覆盖声明")
        else:
            print("  [MISS] 缺少覆盖声明 (数据范围/消息量/时间窗口)")
            issues += 1

        if result["format_issues"]:
            print(f"  [WARN] 结论格式问题 {len(result['format_issues'])} 处:")
            for fi in result["format_issues"][:5]:
                print(f"    \"{fi['conclusion']}\" 缺少: {', '.join(fi['missing'])}")
            issues += len(result["format_issues"])
        else:
            print("  [OK] 结论格式完整")

    return issues


def main():
    analyses_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ANALYSES_DIR

    print("=" * 60)
    print("LakeSkill Report Lint")
    print("=" * 60)

    report_files = sorted(analyses_dir.glob("*_v4.md"))
    if not report_files:
        print("[WARN] 未找到 *_v4.md 报告文件")
        return

    total_issues = 0
    for rp in report_files:
        result = lint_report(rp)
        total_issues += print_report(result)

    # 汇总
    print(f"\n{'=' * 60}")
    print("汇总")
    print(f"{'=' * 60}")
    print(f"  扫描报告: {len(report_files)} 个")
    print(f"  总问题数: {total_issues}")

    if total_issues == 0:
        print("\n  [PASS] 所有报告通过 lint 检查")
    else:
        print(f"\n  [WARN] 发现 {total_issues} 个问题，建议修复")

    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
