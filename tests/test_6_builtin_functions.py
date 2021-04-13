def test_symbols() -> None:
    class BaseClass:
        def __init__(self) -> None:
            self.my_base_class_attribute: int = 0
            super().__init__()

    class Class(BaseClass):
        def __init__(self) -> None:
            self.my_class_attribute: int = 0
            super().__init__()

    instance = Class()

    # vars - Return the __dict__ attribute
    assert "my_class_attribute" in vars(instance)
    assert "my_base_class_attribute" in vars(instance)
    assert "__init__" not in vars(instance)

    # dir - List of valid attributes for the argument
    assert "my_class_attribute" in dir(instance)
    assert "my_base_class_attribute" in dir(instance)
    assert "__init__" in dir(instance)

    # dir - List of names in the current local scope
    assert "Class" in dir()

    # locals - Dictionary representing the current local symbol table
    assert "Class" in locals()
    assert locals() == vars()

    # globals - Dictionary implementing the current module namespace
    assert "test_symbols" in globals()


def test_strings() -> None:
    assert ascii("Italy 🇮🇹") == "'Italy \\U0001f1ee\\U0001f1f9'"
    assert repr("Italy 🇮🇹") == "'Italy 🇮🇹'"
    assert str("Italy 🇮🇹") == "Italy 🇮🇹"


def test_map() -> None:
    assert list(map(lambda x: x.upper(), ["a", "b"])) == ["A", "B"]


def test_sorted() -> None:
    import operator

    l = [(2, "a"), (1, "b"), (1, "a")]
    s = [(1, "a"), (1, "b"), (2, "a")]
    assert sorted(l, key=operator.itemgetter(0, 1)) == s
