"""Tests for privacy leakage."""

from pathlib import Path

from bondlens.privacy.leak_checker import check_for_leaks


def test_no_real_data_in_fixtures():
    """Test that no real data exists in fixtures."""
    fixtures_dir = Path("tests/fixtures")
    if not fixtures_dir.exists():
        return  # Skip if no fixtures directory

    has_leaks, report = check_for_leaks(fixtures_dir)
    assert not has_leaks, f"Privacy leaks found: {report}"


def test_no_real_data_in_examples():
    """Test that no real data exists in examples."""
    examples_dir = Path("examples")
    if not examples_dir.exists():
        return  # Skip if no examples directory

    has_leaks, report = check_for_leaks(examples_dir)
    assert not has_leaks, f"Privacy leaks found: {report}"
