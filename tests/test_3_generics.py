from typing import Callable, Concatenate, Generic, ParamSpec, TypeVar, TypeVarTuple


def test_generics() -> None:
    T = TypeVar("T")
    P = ParamSpec("P")

    # ParamSpec is only valid when used in Concatenate
    # or as the first argument to Callable,
    # or as parameters for user-defined Generics
    def identity(f: Callable[P, T]) -> Callable[P, T]:
        return f

    def sum(x: int, y: int) -> int:
        return x + y

    assert identity(sum)(1, 2) == 3

    # Concatenate
    def value1_for_arg0(f: Callable[Concatenate[int, P], T]) -> Callable[P, T]:
        def ff(*args: P.args, **kwargs: P.kwargs) -> T:
            return f(1, *args, **kwargs)

        return ff

    assert value1_for_arg0(sum)(2) == 3


def test_generic_classes() -> None:
    T = TypeVar("T")
    S = TypeVar("S")

    class GenericClass(Generic[T, S]):
        def __init__(self, t: T, s: S) -> None:
            self.t = t
            self.s = s
            super().__init__()

    instance1: GenericClass[str, int] = GenericClass(t="1", s=1)
    assert instance1.t == "1"
    assert instance1.s == 1

    Ts = TypeVarTuple("Ts")

    class VariadicGenericClass(Generic[*Ts]):
        def __init__(self, *args: *Ts) -> None:
            self.args = args
            super().__init__()

    instance2: VariadicGenericClass[str, int] = VariadicGenericClass("1", 1)

    arg0: str = instance2.args[0]
    assert arg0 == "1"

    arg1: int = instance2.args[1]
    assert arg1 == 1
