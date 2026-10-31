import pytest

from shotbench.cli import SelectionError, select_by_name


def test_select_by_name_returns_matching_object() -> None:
    class Item:
        def __init__(self, name: str) -> None:
            self.name = name

    selected = select_by_name([Item("first"), Item("second")], "second", "detector")

    assert selected.name == "second"


def test_select_by_name_lists_valid_choices() -> None:
    class Item:
        def __init__(self, name: str) -> None:
            self.name = name

    with pytest.raises(SelectionError, match="first, second"):
        select_by_name([Item("first"), Item("second")], "missing", "detector")

