def type_hints() -> None:
    from typing import Union, Optional, Literal, Any, AnyStr, NoReturn, overload
    from typing import Final, TypeVar, final, Generic, ClassVar, NewType
    from typing import Protocol, runtime_checkable
    from typing import NamedTuple, TypedDict
    import collections.abc

    Vector = list[float]  # Type alias
    Identifier = NewType("Identifier", int)  # NewType
    U = TypeVar("U", int, str)  # Type variables

    def foo(
        int_value: int,
        # from typing
        union_value: Union[int, str],
        optional_value: Optional[int],
        literal_value: Literal["yes", "no"],
        any_value: Any,  # Any is both a top type and bottom type
        any_str_value: AnyStr,
        alias_value: Vector,
        new_type_value: Identifier,
        type_variable_value: U,
        # from builtins
        tuple_value: tuple[int, str],
        list_value: list[int],
        dict_value: dict[int, int],
        set_value: set[int],
        type_value: type[int],
        # from collections.abc
        sequence_value: collections.abc.Sequence[int],
        callable_value: collections.abc.Callable[[int, int], int],
    ) -> U:
        x: int = any_value
        return type_variable_value

    assert (
        foo(
            int_value=0,
            union_value=0,
            optional_value=None,
            literal_value="yes",
            any_value=True,
            any_str_value=b"a",
            alias_value=[1.0],
            new_type_value=Identifier(1),
            type_variable_value="Hello",
            tuple_value=(1, "1"),
            list_value=[1],
            dict_value={1: 1},
            set_value={1},
            type_value=int,
            sequence_value=[1],
            callable_value=(lambda x, y: x + y),
        )
        == "Hello"
    )

    # ____________________________________________________________
    # Final

    final_var: Final[int] = 10

    # ____________________________________________________________
    # NoReturn

    def never_return() -> NoReturn:
        while True:
            pass

    # ____________________________________________________________
    # Overload

    @overload
    def bar(x: int) -> str:
        ...

    @overload
    def bar(x: list[int]) -> int:
        ...

    def bar(x: Any) -> Any:
        if isinstance(x, int):
            return str(x)
        if isinstance(x, list):
            return x[0]
        return x

    assert bar(1) == "1"
    assert bar([1, 2]) == 1

    # ____________________________________________________________
    #  Generic types

    T = TypeVar("T")
    S = TypeVar("S")

    @final
    class GenericClass(Generic[T, S]):
        class_var: ClassVar[int] = 0

        def __init__(self, t: T, s: S) -> None:
            self.t = t
            self.s = s

        def get_t(self) -> T:
            return self.t

    generic_class_value: GenericClass[str, int] = GenericClass(t="1", s=1)

    # ____________________________________________________________
    # Structural subtyping
    # runtime_checkable checks only the presence of the required
    # methods, not their type signatures

    K = TypeVar("K")

    @runtime_checkable
    class AProtocol(Protocol[K]):
        def foo(self, k: K) -> K:
            return k

    class C:
        def foo(self, k: float) -> float:
            return k

    def func(x: AProtocol[K], k: K) -> K:
        return x.foo(k)

    assert isinstance(C(), AProtocol)
    assert func(x=C(), k=1) == 1

    # ____________________________________________________________
    # NamedTuple

    class ANamedTuple(NamedTuple):
        string_value: str
        int_value: int = 0

    named_tuple_value: ANamedTuple = ANamedTuple(string_value="a")
    assert named_tuple_value.int_value == 0
    x, y = named_tuple_value
    assert x == named_tuple_value.string_value
    assert y == named_tuple_value.int_value

    # ____________________________________________________________
    # TypedDict
    # Special construct to add type hints to a dictionary.
    # At runtime it is a plain dict.
    class ATypedDict(TypedDict):
        string_value: str
        int_value: int

    typed_dict_1 = ATypedDict(string_value="a", int_value=0)
    typed_dict_2: ATypedDict = {"string_value": "a", "int_value": 0}
    dict_value: dict[str, Union[int, str]] = dict(string_value="a", int_value=0)
    assert typed_dict_1 == dict_value
    assert typed_dict_2 == dict_value

    # ____________________________________________________________
    # Annotations
    def annotations(x: str) -> None:
        pass

    # print("Annotations:", annotations.__annotations__)


def arguments() -> None:
    import sys

    sys.argv[0]  # "" -> standard input
    # "-c" -> -c command is used
    # full name of the located module -> -m command is used


def functional_programming() -> None:
    import functools
    import itertools
    import operator

    assert list(map(lambda x: x.upper(), ["a", "b"])) == ["A", "B"]
    assert [x.upper() for x in ["a", "b"]] == ["A", "B"]

    count_it = itertools.count(10, 5)
    assert next(count_it) == 10
    assert next(count_it) == 15
    assert next(count_it) == 20

    cycle_it = itertools.cycle([1, 2])
    assert next(cycle_it) == 1
    assert next(cycle_it) == 2
    assert next(cycle_it) == 1
    assert next(cycle_it) == 2

    chain_it = itertools.chain(["a"], (1,))
    assert next(chain_it) == "a"
    assert next(chain_it) == 1

    def sum(x: int, y: int) -> int:
        return x + y

    f = functools.partial(sum, y=10)
    assert f(1) == 11

    assert functools.reduce(operator.add, [1, 2, 3]) == 6
    # (18 / 3) / 3 = 2
    assert functools.reduce(operator.truediv, [18, 3, 3]) == 2

    l = [(2, "a"), (1, "b"), (1, "a")]
    s = [(1, "a"), (1, "b"), (2, "a")]
    assert sorted(l, key=operator.itemgetter(0, 1)) == s


def enumerations():
    from enum import Enum, Flag, unique, auto

    # Enum
    @unique
    class Color(Enum):
        RED = 1
        BLUE = 2
        GREEN = 3

        @classmethod
        def default(cls):
            return cls.RED

    assert Color.RED is Color.RED
    assert Color.default() == Color.RED

    assert Color.RED.name == "RED"
    assert Color.RED.value == 1
    assert Color.RED != 1

    for name, member in Color.__members__.items():
        name, member

    # Flag
    class Perm(Flag):
        R = auto()
        W = auto()
        X = auto()

    assert Perm.R in Perm.R | Perm.W


def data_classes():
    from dataclasses import dataclass, field, asdict, astuple

    @dataclass
    class ADataClass:
        string_value: str
        int_value: int = 0
        list_value: list = field(init=False, repr=True, default_factory=list)

        def foo(self) -> int:
            return self.int_value + 1

    p1 = ADataClass(string_value="name", int_value=0)
    p2 = ADataClass(string_value="name")

    assert p1 == p2
    assert p1.foo() == 1
    assert asdict(p1) == {"int_value": 0, "list_value": [], "string_value": "name"}
    assert astuple(p1) == ("name", 0, [])


def abstract_classes():
    from abc import ABC, abstractmethod

    class AbstractClass(ABC):
        @abstractmethod
        def abstract_method(self) -> str:
            pass

        @property
        @abstractmethod
        def my_abstract_property(self) -> int:
            pass

        # Structural subtyping
        @classmethod
        def __subclasshook__(cls, C):
            if cls is AbstractClass:
                if any("abstract_method" in C.__dict__ for C in C.__mro__) and any(
                    "my_abstract_property" in C.__dict__ for C in C.__mro__
                ):
                    return True
            return NotImplemented

    class NominalSubtype(AbstractClass):
        def abstract_method(self) -> str:
            return "NominalSubtype"

        @property
        def my_abstract_property(self) -> int:
            return 0

    class StructuralSubtype:
        def abstract_method(self) -> str:
            return "StructuralSubtype"

        @property
        def my_abstract_property(self) -> int:
            return 0

    assert isinstance(NominalSubtype(), AbstractClass)
    assert isinstance(StructuralSubtype(), AbstractClass)

    assert not isinstance(str, AbstractClass)

    AbstractClass.register(str)  # This is an error
    assert isinstance(str(), AbstractClass)


def regex():
    import re

    # Gready
    # {m}   -> from m repetitions
    # {m,n} -> from m to n repetitions
    # *     -> {0,}
    # +     -> {1,}
    # ?     -> {0,1}
    # Non-gready
    # {m,n}?    *?    +?    ??

    # \b -> matches the empty string, but only at the beginning or end of a word
    # \B -> matches the empty string, but only when it is not at the beginning or end of a word

    # ____________________________________________________________________________________
    # Determine if the RE matches at the beginning of the string.
    if x := re.match(r"abc", "abc-def-abc"):
        assert x.group() == "abc"
        assert x.span() == (0, 3)
    else:
        assert False

    # ____________________________________________________________________________________
    # Scan through a string, looking for any location where this RE matches.
    if x := re.search(r"abc", "def-abc-abc"):
        assert x.group() == "abc"
        assert x.span() == (4, 7)
    else:
        assert False

    # ____________________________________________________________________________________
    # Find all substrings where the RE matches, and returns them as an iterator
    it = re.finditer(r"abc", "abc-def-abc")
    y = next(it)
    assert y.group() == "abc"
    assert y.span() == (0, 3)

    y = next(it)
    assert y.group() == "abc"
    assert y.span() == (8, 11)

    # ____________________________________________________________________________________
    # IGNORECASE mode
    string = "ABC-def-abc"
    regex = r"abc"
    list = re.findall(regex, string)
    assert list == ["abc"]

    list = re.findall(regex, string, re.IGNORECASE)
    assert list == ["ABC", "abc"]

    # ____________________________________________________________________________________
    # DOTALL mode
    # .     ->  any character except a newline
    #           in DOTALL mode -> also matches a newline
    string = "a\nb"

    regex = r".*"

    list = re.findall(regex, string)
    assert list == ["a", "", "b", ""]

    list = re.findall(regex, string, re.DOTALL)
    assert list == ["a\nb", ""]

    # ____________________________________________________________________________________
    # ASCII mode
    string = "perché"
    regex = r"\w+"

    list = re.findall(regex, string)
    assert list == ["perché"]

    list = re.findall(regex, string, re.ASCII)
    assert list == ["perch"]

    # ____________________________________________________________________________________
    # MULTILINE mode
    # ^     ->  the start of the string
    #           in MULTILINE mode -> also matches immediately after each newline
    # $     ->  the end of the string or just before the newline at the end of the string
    #           in MULTILINE mode -> also matches before a newline
    # \A    ->  matches only at the start of the string
    # \Z    ->  matches only at the end of the string
    string = "a\nb"
    regex = r"^.*"

    list = re.findall(regex, string)
    assert list == ["a"]

    list = re.findall(regex, string, re.MULTILINE)
    assert list == ["a", "b"]

    # ____________________________________________________________________________________
    # Verbose mode
    # Whitespace in the regular expression that isn’t inside a character class
    # is ignored

    string = "abc-def-abc"
    regex = r"""
        \w+ # matches Unicode word characters
    """

    list = re.findall(regex, string, re.VERBOSE)
    assert list == ["abc", "def", "abc"]

    # ____________________________________________________________________________________
    # Grouping
    string = "1-2 3-4"
    regex = r"(\d)-(\d)"

    it = re.finditer(regex, string, re.VERBOSE)
    y = next(it)
    assert y.group(0, 1, 2) == ("1-2", "1", "2")
    y = next(it)
    assert y.groups() == ("3", "4")

    # Named Groups
    regex = r"(?P<num1>\d)-(?P<num2>\d)"

    it = re.finditer(regex, string, re.VERBOSE)
    y = next(it)
    assert y.groupdict() == {"num1": "1", "num2": "2"}
    assert y.group("num1") == "1"
    assert y.group("num2") == "2"
    # ----------------------------------------
    # Backreferences
    string = "1-2 3-3"
    regex = r"(\d)-\1"
    it = re.finditer(regex, string, re.VERBOSE)
    y = next(it)
    assert y.group(1) == "3"

    # Named Groups
    regex = r"(?P<num>\d)-(?P=num)"
    it = re.finditer(regex, string, re.VERBOSE)
    y = next(it)
    assert y.group("num") == "3"
    # ----------------------------------------
    # Non-capturing
    assert re.search("(\d)+", "z 1223").groups() == ("3",)
    assert re.search("(?:\d)", "z 1223").groups() == ()
    # ----------------------------------------
    # Lookahead Assertions
    # (?=...) -> Positive lookahead assertion
    # (?!...) -> Negative lookahead assertion
    regex = "1(?!-$).*"
    assert re.findall(regex, "1-") == []
    assert re.findall(regex, "1--") == ["1--"]

    # ____________________________________________________________________________________
    # Split strings
    assert re.split("-", "abc-def-ghi") == ["abc", "def", "ghi"]
    # ____________________________________________________________________________________
    # Search and Replace
    assert re.sub("-", "|", "abc-def-ghi") == "abc|def|ghi"
    assert re.subn("-", "|", "abc-def-ghi") == ("abc|def|ghi", 2)

    regex = r"(?P<num1>\d)-(?P<num2>\d)"
    string = "1-2 3-4"
    repl = r"\g<num2>-\g<num1>"
    result = "2-1 4-3"
    assert re.sub(regex, repl, string) == result

    assert (
        re.sub(regex, lambda m: m.group("num2") + "-" + m.group("num1"), string)
        == result
    )
