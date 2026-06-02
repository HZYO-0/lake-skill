"""Simple test to verify test setup."""


def test_simple():
    """Simple test."""
    assert 1 + 1 == 2


def test_import():
    """Test that imports work."""
    from cli.bondlens.schema import Message
    assert Message is not None
