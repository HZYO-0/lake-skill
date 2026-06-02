"""Unified pre-release check script.

Runs all quality gates and reports results. Exit 0 if all pass, 1 otherwise.

Usage:
    python tools/check.py           # run all checks
    python tools/check.py --quick   # skip mypy (slow)
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], label: str, advisory: bool = False) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    try:
        r = subprocess.run(
            cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=120
        )
        output = r.stdout + r.stderr
        ok = r.returncode == 0
        if not ok and advisory:
            print(f"  [ADVISORY] {label}: {r.returncode}")
            print(output.strip()[-500:] if len(output.strip()) > 500 else output.strip())
            return True, output  # advisory = don't fail
        elif not ok:
            print(f"  [FAIL] {label}")
            print(output.strip()[-500:] if len(output.strip()) > 500 else output.strip())
            return False, output
        else:
            # Extract useful summary from output
            lines = output.strip().splitlines()
            summary = lines[-1] if lines else "ok"
            print(f"  [PASS] {label}: {summary}")
            return True, output
    except subprocess.TimeoutExpired:
        print(f"  [FAIL] {label}: timeout")
        return False, "timeout"
    except FileNotFoundError:
        print(f"  [SKIP] {label}: command not found")
        return True, "skipped"


def main() -> int:
    quick = "--quick" in sys.argv
    results: list[tuple[str, bool]] = []

    # 1. Check dev dependencies
    print("\nChecking dev dependencies...")
    try:
        import typer  # noqa: F401
        import pydantic  # noqa: F401
        import pytest  # noqa: F401
        import ruff  # noqa: F401
        print("  [PASS] Dev dependencies installed")
        results.append(("dev-deps", True))
    except ImportError as e:
        print(f"  [FAIL] Missing dependency: {e}")
        print("  Run: pip install -e '.[dev]'")
        results.append(("dev-deps", False))
        return 1

    # 2. Ruff lint
    ok, _ = run([sys.executable, "-m", "ruff", "check", "."], "Ruff lint")
    results.append(("ruff", ok))

    # 3. Pytest
    ok, out = run([sys.executable, "-m", "pytest", "-q"], "Pytest")
    if ok:
        # Extract test count
        for line in out.strip().splitlines():
            if "passed" in line:
                print(f"    Tests: {line.strip()}")
    results.append(("pytest", ok))

    # 4. Privacy scan (all directories)
    ok, _ = run(
        [sys.executable, "tools/check_no_real_private_data.py", "cli", "skill", "tools", "tests", "examples", "docs"],
        "Privacy scan",
    )
    results.append(("privacy-scan", ok))

    # 5. Network call scan
    ok, _ = run(
        [sys.executable, "tools/check_no_forbidden_network_calls.py", "cli", "skill"],
        "Network call scan",
    )
    results.append(("network-scan", ok))

    # 6. Mypy (advisory)
    if not quick:
        ok, out = run([sys.executable, "-m", "mypy", "cli"], "Mypy (advisory)", advisory=True)
        if ok:
            # Count errors
            error_count = out.count(" error:")
            print(f"    Mypy errors: {error_count} (advisory)")
        results.append(("mypy-advisory", True))  # always passes
    else:
        print("\n  [SKIP] Mypy (use --full to include)")
        results.append(("mypy-advisory", True))

    # Summary
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    all_pass = True
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
        if not ok:
            all_pass = False

    if all_pass:
        print("\n  All checks passed.")
    else:
        print("\n  Some checks failed. Fix issues above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
