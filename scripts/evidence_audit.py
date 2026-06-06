"""
证据审计脚本：校验 BondLens 分析报告中的证据完整性。

检查项：
1. 每条结论是否包含 evidence_id / confidence / alternative_explanation
2. 报告中引用的 evidence_id 是否存在于 evidence_index.jsonl
3. evidence_index.jsonl 中的记录是否符合 schema
4. 统计覆盖率：有证据的结论 vs 无证据的结论

用法：python scripts/evidence_audit.py [analyses_dir]
"""
import json
import re
import sys
from pathlib import Path

ANALYSES_DIR = Path(__file__).resolve().parents[1] / "analyses" / "zy-tf"

# 必须字段和合法值
REQUIRED_FIELDS = ["evidence_id", "date", "speaker", "raw_quote", "context",
                   "claim_tags", "confidence", "source_file", "analysis_version"]
VALID_CONFIDENCE = {"low", "medium", "high"}
VALID_SPEAKER = {"Tf", "Zy"}


def load_evidence_index(index_path: Path) -> dict[str, dict]:
    """加载 evidence_index.jsonl，返回 {evidence_id: record}。"""
    index = {}
    if not index_path.exists():
        return index
    with open(index_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  [ERROR] JSON 解析失败 (line {lineno}): {e}")
                continue
            eid = rec.get("evidence_id")
            if eid:
                index[eid] = rec
    return index


def validate_index_records(index: dict[str, dict]) -> list[str]:
    """校验 index 中每条记录是否符合 schema。"""
    errors = []
    for eid, rec in index.items():
        # 检查必填字段
        for field in REQUIRED_FIELDS:
            if field not in rec or rec[field] is None:
                errors.append(f"  [{eid}] 缺少必填字段: {field}")
        # 检查 confidence 合法性
        conf = rec.get("confidence")
        if conf and conf not in VALID_CONFIDENCE:
            errors.append(f"  [{eid}] confidence 值非法: {conf} (合法值: {VALID_CONFIDENCE})")
        # 检查 speaker 合法性
        speaker = rec.get("speaker")
        if speaker and speaker not in VALID_SPEAKER:
            errors.append(f"  [{eid}] speaker 值非法: {speaker} (合法值: {VALID_SPEAKER})")
        # 检查 claim_tags 非空
        tags = rec.get("claim_tags")
        if not tags or not isinstance(tags, list):
            errors.append(f"  [{eid}] claim_tags 为空或非列表")
        # 检查 alternative_explanation 必须为非空 string
        alt = rec.get("alternative_explanation")
        if alt is None:
            errors.append(f"  [{eid}] alternative_explanation 为 null（schema 要求为 string）")
        elif not isinstance(alt, str):
            errors.append(f"  [{eid}] alternative_explanation 类型错误: {type(alt).__name__}（应为 string）")
        elif alt.strip() == "":
            errors.append(f"  [{eid}] alternative_explanation 为空字符串（schema 要求为非空 string）")
        # 检查 evidence_id 格式
        if not re.match(r"^E-\d{8}-\d{3}$", eid):
            errors.append(f"  [{eid}] evidence_id 格式不合规 (应为 E-YYYYMMDD-NNN)")
    return errors


def extract_evidence_refs_from_report(report_path: Path) -> set[str]:
    """从报告文件中提取所有 E-YYYYMMDD-NNN 格式的证据引用。"""
    text = report_path.read_text(encoding="utf-8")
    return set(re.findall(r"E-\d{8}-\d{3}", text))


def extract_conclusions_from_report(report_path: Path) -> list[dict]:
    """提取报告中的结论块（带 **证据**: 行的段落）。"""
    text = report_path.read_text(encoding="utf-8")
    conclusions = []
    current = None
    for line in text.split("\n"):
        # 检测新的结论段（### 开头或 **描述**: 开头）
        if line.startswith("### ") or line.startswith("**描述**"):
            if current:
                conclusions.append(current)
            current = {"lines": [line], "has_evidence": False,
                       "has_confidence": False, "has_alt_explanation": False}
        elif current:
            current["lines"].append(line)
            if "**证据**:" in line or "**证据**：" in line:
                current["has_evidence"] = True
            if "**置信度**:" in line or "**置信度**：" in line:
                current["has_confidence"] = True
            if "**替代解释**:" in line or "**替代解释**：" in line:
                current["has_alt_explanation"] = True
    if current:
        conclusions.append(current)
    return conclusions


def audit_report(report_path: Path, index: dict[str, dict]) -> dict:
    """审计单个报告文件。"""
    report_name = report_path.name
    refs = extract_evidence_refs_from_report(report_path)
    conclusions = extract_conclusions_from_report(report_path)

    missing_in_index = refs - set(index.keys())
    unused_in_index = set(index.keys()) - refs

    # 检查结论完整性
    conclusions_without_evidence = [c for c in conclusions if not c["has_evidence"]]
    conclusions_without_confidence = [c for c in conclusions if not c["has_confidence"]]
    conclusions_without_alt = [c for c in conclusions if not c["has_alt_explanation"]]

    return {
        "report": report_name,
        "total_conclusions": len(conclusions),
        "with_evidence": len(conclusions) - len(conclusions_without_evidence),
        "with_confidence": len(conclusions) - len(conclusions_without_confidence),
        "with_alt_explanation": len(conclusions) - len(conclusions_without_alt),
        "evidence_refs": sorted(refs),
        "missing_in_index": sorted(missing_in_index),
        "unused_in_index": sorted(unused_in_index),
        "conclusions_without_evidence": len(conclusions_without_evidence),
        "conclusions_without_confidence": len(conclusions_without_confidence),
        "conclusions_without_alt_explanation": len(conclusions_without_alt),
    }


def main():
    analyses_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ANALYSES_DIR
    index_path = analyses_dir / "evidence_index.jsonl"

    print("=" * 60)
    print("BondLens 证据审计")
    print("=" * 60)

    # 1. 加载并校验 evidence_index.jsonl
    print(f"\n[1] 校验 evidence_index.jsonl: {index_path}")
    index = load_evidence_index(index_path)
    print(f"    加载 {len(index)} 条证据记录")

    schema_errors = validate_index_records(index)
    if schema_errors:
        print(f"    [WARN] 发现 {len(schema_errors)} 条 schema 违规:")
        for e in schema_errors:
            print(e)
    else:
        print("    [OK] 所有记录符合 schema")

    # 2. 审计每个 v4 报告
    print("\n[2] 审计 v4 报告文件")
    report_files = sorted(analyses_dir.glob("*_v4.md"))
    if not report_files:
        print("    [WARN] 未找到 *_v4.md 报告文件")
        return

    total_conclusions = 0
    total_with_evidence = 0
    all_missing = set()
    all_refs = set()

    for rp in report_files:
        result = audit_report(rp, index)
        total_conclusions += result["total_conclusions"]
        total_with_evidence += result["with_evidence"]
        all_missing.update(result["missing_in_index"])
        all_refs.update(result["evidence_refs"])

        print(f"\n  --- {result['report']} ---")
        print(f"    结论总数: {result['total_conclusions']}")
        print(f"    有证据:   {result['with_evidence']}/{result['total_conclusions']}")
        print(f"    有置信度: {result['with_confidence']}/{result['total_conclusions']}")
        print(f"    有替代解释: {result['with_alt_explanation']}/{result['total_conclusions']}")
        print(f"    引用证据数: {len(result['evidence_refs'])}")

        if result["missing_in_index"]:
            print("    [MISSING] 以下证据 ID 在报告中引用但不在 index 中:")
            for eid in result["missing_in_index"]:
                print(f"      - {eid}")
        if result["unused_in_index"]:
            print("    [UNUSED] 以下证据在 index 中但未被任何报告引用:")
            for eid in result["unused_in_index"]:
                print(f"      - {eid}")

    # 3. 汇总
    print(f"\n{'=' * 60}")
    print("汇总")
    print(f"{'=' * 60}")
    coverage = (total_with_evidence / total_conclusions * 100) if total_conclusions else 0
    print(f"  总结论数: {total_conclusions}")
    print(f"  有证据结论: {total_with_evidence} ({coverage:.0f}%)")
    print(f"  Index 记录数: {len(index)}")
    unused_count = len(set(index.keys()) - all_refs)
    print(f"  未被引用的 index 记录: {unused_count}")
    if unused_count > 0:
        for eid in sorted(set(index.keys()) - all_refs):
            print(f"    - {eid}")

    if all_missing:
        print("\n  [ACTION] 需要补充以下证据到 evidence_index.jsonl:")
        for eid in sorted(all_missing):
            print(f"    - {eid}")
    else:
        print("\n  [PASS] 所有报告引用的证据均在 index 中")

    # 返回退出码
    has_issues = bool(schema_errors or all_missing)
    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
