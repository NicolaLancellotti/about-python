from collections.abc import Callable, Sequence
from typing import (
    Literal,
    LiteralString,
    NamedTuple,
    NewType,
    NotRequired,
    Optional,
    Required,
    TypeAlias,
    TypedDict,
    TypeGuard,
    Union,
    cast,
)


def test_booleans() -> None:
    assert not True == False
    assert 1 and "Hello" == "Hello"
    assert 10 or "Hello" == 10
    assert 1 <= 2 <= 3


def test_numbers() -> None:
    binary: int = 0b1010
    assert binary == 10
    octal: int = 0o12
    assert octal == 10
    hexadecimal: int = 0xA
    assert hexadecimal == 10
    complex_number: complex = 1 + 2j
    assert complex_number.real == 1
    assert complex_number.imag == 2

    assert 5 // 3 == 1  # Floor Division
    assert -5 // 3 == -2  # Floor Division
    assert 5 % 3 == 2
    assert -5 % 3 == 1

    assert -10 >> 1 == -5
    assert -10 << 1 == -20

    assert 2**3 == 8


def test_strings() -> None:
    abc_string: str = "abc"
    assert len(abc_string) == 3
    assert abc_string[0] == "a"
    assert abc_string[2:] == "c"

    # Concatenate
    assert "a" "b" == "ab"
    assert "a" + "b" == "ab"
    assert "".join(["a", "b"]) == "ab"  # Recommended idiom

    # Format
    assert "{0} - {1} - {0}".format("a", "b") == "a - b - a"
    assert "{A} - {B} - {A}".format(A="a", B="b") == "a - b - a"

    # Multiline strings
    multiline_string: str = """\
a
b\
c
"""
    assert multiline_string == "a\nbc\n"

    # Unicode
    assert "\U0001F1EE\U0001F1F9" == "🇮🇹"

    # Raw strings
    assert r"\n" == "\\n"

    # Formatted strings
    assert f"{1 + 2}" == "3"
    assert f"{1 + 2 = }" == "1 + 2 = 3"
    # Conversion fields
    assert f"{'à'!s}" == "à"  # str()
    assert f"{'à'!r}" == "'à'"  # repr()
    assert f"{'à'!a}" == "'\\xe0'"  # ascii()
    # Format specifier
    assert f"{123.456:7.5}" == " 123.46"
    assert f"{16:#0x}" == "0x10"

    # Formatted raw string
    assert rf"{1}-A\n" == "1-A\\n"


def test_tuples() -> None:
    tuple0: tuple[()] = ()
    assert tuple0 == ()

    tuple1: tuple[int] = (1,)
    assert tuple1[0] == 1

    tuple4: tuple[int, int, int, int] = (1, 2, 3, 4)
    assert tuple1 + (2, 3, 4) == tuple4

    a, b, c, d = tuple4
    assert a == 1 and b == 2 and c == 3 and d == 4
    a, *l, d = 1, 2, 3, 4
    assert a == 1 and l == [2, 3] and d == 4

    assert tuple(tuple4) is tuple4  # It does not make a copy


def test_named_tuples() -> None:
    class MyNamedTuple(NamedTuple):
        string_value: str
        int_value: int = 0

    instance: MyNamedTuple = MyNamedTuple(string_value="a")
    x, y = instance
    assert x == instance.string_value
    assert y == instance.int_value
    assert instance == ("a", 0)


def test_lists() -> None:
    list1: list[int] = [1, 2, 3, 4]

    assert list1[0] == 1
    assert list1[-1] == 4

    assert list1[0:2:1] == list1[:2] == [1, 2]
    assert list1[0:-1:2] == list1[::2] == [1, 3]
    assert list1[-1:-5:-1] == list1[::-1] == [4, 3, 2, 1]

    # In
    assert 1 in list1

    # Append
    list1.append(5)
    assert list1[-1] == 5

    # Remove
    list2: list[str] = ["a", "b", "c"]
    del list2[0]
    list2.remove("c")
    assert list2 == ["b"]

    # List comprehension
    assert [x for x in [1, 2, 3] if x > 1] == [2, 3]
    assert [j for i in [1, 2, 3] for j in range(i)] == [0, 0, 1, 0, 1, 2]

    # Is
    assert list1[:] is not list1  # It makes a copy
    assert list(list1) is not list1  # It makes a copy


def test_dictionaries() -> None:
    empty_dictionary: dict[str, int] = {}
    assert len(empty_dictionary) == 0

    dictionary: dict[str, int] = {"one": 1, "two": 2, "three": 3}
    dictionary2: dict[str, int] = dict(one=1, two=2, three=3)
    assert dictionary == dictionary2
    assert list(dictionary) == ["one", "two", "three"]

    # Iterate
    for key, value in dictionary.items():  # type: ignore
        pass

    # Get
    assert dictionary["one"] == 1
    # dictionary["four"]  # Error
    assert dictionary.get("one") == 1
    assert dictionary.get("four") == None
    assert dictionary.get("four", 4) == 4

    # Set default - if the key does not exist, insert the key
    dictionary.setdefault("five", 5)
    assert dictionary["five"] == 5
    dictionary.setdefault("five", 6)
    assert dictionary["five"] == 5

    # Delete
    del dictionary["one"]
    assert dictionary.get("one") == None

    # Dictionary comprehension
    assert {x: x**2 for x in range(4)} == {0: 0, 1: 1, 2: 4, 3: 9}


def test_typed_dictionaries() -> None:
    class MyTypedDict(TypedDict):
        string_value: Required[str]
        int_value: Required[int]
        bool_value: NotRequired[bool]

    instance = MyTypedDict(string_value="a", int_value=0)
    assert instance == {"string_value": "a", "int_value": 0}

    dictionary: dict[str, Union[int, str]] = dict(string_value="a", int_value=0)
    assert instance == dictionary


def test_sets() -> None:
    empty_set: set[int] = set()
    assert len(empty_set) == 0

    set1 = {1, 1, 2, 2, 3, 4}
    set1.add(2)

    assert set1 | {4, 5} == {1, 2, 3, 4, 5}
    assert set1 & {4, 2} == {2, 4}

    # Set comprehensions
    assert {x for x in "abcddeef" if x not in "abc"} == {"d", "e", "f"}


def test_enumerations() -> None:
    from enum import Enum, unique

    @unique
    class Color(Enum):
        RED = 1
        BLUE = 2
        GREEN = 3

    assert Color._member_names_ == ["RED", "BLUE", "GREEN"]
    assert Color.RED.name == "RED"
    assert Color.RED.value == 1


def test_flags() -> None:
    from enum import Flag, auto

    class Permissions(Flag):
        R = auto()
        W = auto()
        X = auto()

    assert Permissions.R in Permissions.R | Permissions.W


Vector: TypeAlias = list[float]
Identifier = NewType("Identifier", str)


def test_type_hints() -> None:
    union1: Union[int, str] = 0
    assert union1 == 0
    union2: int | str = 0
    assert union2 == 0

    optional: Optional[int] = None
    assert optional is None

    literal: Literal["yes", "no"] = "yes"
    assert literal == "yes"

    literal_string: LiteralString = "literal_string"
    assert literal_string == "literal_string"

    identifier: Identifier = Identifier("abc")
    assert identifier == "abc"

    vector: Vector = [1, 2]
    assert vector == [1, 2]

    sequence: Sequence[int] = [1, 2, 3]
    assert sequence == [1, 2, 3]

    callable: Callable[[int, int], int] = lambda x, y: x + y
    assert callable(1, 2) == 3

    # Cast
    def get_ten() -> object:
        return 10

    x_object: object = get_ten()

    x: int = cast(int, x_object)
    assert x == 10

    # TypeGuard
    def is_int(value: object) -> TypeGuard[int]:
        return isinstance(value, int)

    if is_int(x_object):
        sum: int = x_object + 1
        assert sum == 11
