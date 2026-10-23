import pytest
from starter.domain import normalize_title

@pytest.mark.parametrize("value,expected", [("  Ship  ", "Ship"), ("x" * 120, "x" * 120), ("  🚀  ", "🚀")])
def test_normalize(value, expected):
    assert normalize_title(value) == expected

@pytest.mark.parametrize("value", ["", "  ", "x" * 121, None, 1, True, [], {}])
def test_reject(value):
    with pytest.raises(ValueError):
        normalize_title(value)
