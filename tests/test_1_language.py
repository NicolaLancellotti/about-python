from collections.abc import Callable, Generator, Iterator
from typing import Any, Final, NoReturn, Optional, TypeAlias, overload

import pytest


def values() -> None:
    final_variable: Final[int] = 0
    assert final_variable == 0
    # final_variable = 1  # Error (no runtime checking)


def test_if_expression() -> None:
    assert (1 if 3 > 2 else 2) == 1


def test_control_flow() -> None:
    x: int = 1
    # ______________________________________
    # If

    if x == 1:
        assert True
    elif x == 2:
        assert False
    else:
        assert False

    optional_value: Optional[int] = 10
    if value := optional_value:  # walrus operator
        assert value == 10
    else:
        assert False

    # ______________________________________
    # Match

    def get_tuple() -> tuple[int, str]:
        return (1, "1")

    match get_tuple():
        case (-1, "-1") | (0, "0"):
            pass
        case (_, y) as t if y == "1":
            assert t[0] == 1
            assert t[1] == "1"
        case _:
            pass

    # ______________________________________
    # For / while
    # x = 8, 6

    for x in range(8, 4, -2):
        # continue
        # break  # skip the optional else clause
        pass
    else:
        pass

    x = 8
    while x > 4:
        x -= 2
    else:
        pass


def test_functions_arguments() -> None:
    def f(positional: int, /, positional_or_keyword: int, *, keyword: int) -> None:
        pass

    f(1, 2, keyword=3)
    f(1, positional_or_keyword=2, keyword=3)


def test_functions_variadic_arguments() -> None:
    def f(*args: int) -> tuple[int, ...]:
        return args

    tuple1: tuple[int, int, int] = (1, 2, 3)
    assert f(1, 2, 3) == tuple1
    assert f(*tuple1) == tuple1


def test_functions_with_keyword_arguments() -> None:
    def f(**keyword_args: int) -> dict[str, int]:
        return keyword_args

    keyword_args = {"x": 1, "y": 2}
    assert f(x=1, y=2) == keyword_args
    assert f(**keyword_args) == keyword_args


def test_functions_with_default_argument() -> None:
    def f1(arg: int, default_list: Optional[list[int]] = None) -> list[int]:
        arg_list = default_list if default_list is not None else []
        arg_list.append(arg)
        return arg_list

    assert f1(1) == [1]
    assert f1(2) == [2]

    def f2(arg: int, default_list: list[int] = []) -> list[int]:
        default_list.append(arg)
        return default_list

    assert f2(1) == [1]
    assert f2(2) == [1, 2]


def test_functions_closures() -> None:
    captured: int = 1

    def f1() -> int:
        return captured

    def f2(x: int = captured) -> int:
        return x

    assert f1() == 1
    assert f2() == 1

    captured = 2
    assert f1() == 2
    assert f2() == 1


def test_functions_lambdas() -> None:
    # They are syntactically restricted to a single expression
    assert (lambda x, y: x + y)(1, 2) == 3

    x: int = 1
    lambda1: Callable[[], int] = lambda: x
    lambda2: Callable[[], int] = lambda x=x: x  # type: ignore

    assert lambda1() == 1
    assert lambda2() == 1
    x = 2
    assert lambda1() == 2
    assert lambda2() == 1


def test_functions_no_return() -> None:
    def no_return() -> NoReturn:  # type: ignore
        while True:
            pass


def test_functions_overload() -> None:
    @overload
    def overloaded_function(x: int) -> str:
        ...

    @overload
    def overloaded_function(x: list[int]) -> int:
        ...

    def overloaded_function(x: Any) -> Any:
        return_value: Any = None
        if isinstance(x, int):
            return_value = x
        elif isinstance(x, list):
            return_value = x[0]
        return return_value

    assert overloaded_function(1) == 1
    assert overloaded_function([1, 2]) == 1


x: int = 0


def test_scopes() -> None:
    y: int = 1  # local variable
    z: int = 1  # local variable

    def f() -> None:
        global x
        assert x == 0
        x = 2

        nonlocal y
        assert y == 1
        y = 2

        z: int = 2
        assert z == 2

    f()
    assert x == 2  # global variable
    assert y == 2  # local variable
    assert z == 1  # local variable


def test_pacakges() -> None:
    import tests.my_package as p
    from tests.my_package.my_module import my_file as f

    assert p.my_function(1) == 1
    assert f.my_function(1) == 1


from tests.my_package import *  # type: ignore


def test_pacakges_all() -> None:
    assert my_function(1) == 1
    with pytest.raises(NameError):
        secret_function()  # Error: it is not in __all__ # type: ignore


IntToInt: TypeAlias = Callable[[int], int]


def test_decorators() -> None:
    from functools import wraps

    def increment(increment_value: int) -> Callable[[IntToInt], IntToInt]:
        def decorator(f: IntToInt) -> IntToInt:
            @wraps(f)
            def wrap(x: int) -> int:
                return f(x) + increment_value

            return wrap

        return decorator

    @increment(2)
    def increment_by_2(x: int) -> int:
        """increment_by_2 doc"""
        return x

    assert increment_by_2(1) == 3
    assert increment_by_2.__doc__ == "increment_by_2 doc"


def test_exceptions() -> None:
    class MyException(Exception):
        def __init__(self, message: str, expression: int) -> None:
            super().__init__(message, expression)

        def __str__(self) -> str:
            return f"{self.message} - {self.expression}"

        @property
        def message(self) -> str:
            return self.args[0]

        @property
        def expression(self) -> int:
            return self.args[1]

    try:
        raise MyException("message", 1)
    except MyException as exception:
        # `exception` is cleared at the end of the except clause
        assert exception.message == "message"
        assert exception.expression == 1
    except (TypeError, NameError) as exc:
        raise  # re-raise   # exception chaining
        raise RuntimeError  # exception chaining
        raise RuntimeError from exc  # exception chaining
        raise RuntimeError from None  # do not chain
    else:
        # It is executed if the control flow leaves the try suite, no exception was raised,
        # and no return, continue, or break statement was executed.
        assert False
    finally:
        # If the finally clause raises another exception, the saved exception is set as the
        # context of the new exception.
        # If the finally clause executes a return, break or continue statement, the saved
        # exception is discarded
        pass


def test_exception_groups(capsys: pytest.CaptureFixture[str]) -> None:
    # Multiple except* clauses can execute, each handling part of the exception group.
    # Each clause executes at most once and handles an exception group of all matching exceptions.
    # Each exception in the group is handled by at most one except* clause, the first that matches it.

    # Any remaining exceptions that were not handled by any except* clause are re-raised at the end,
    # combined into an exception group along with all exceptions that were raised from within except* clauses.

    with pytest.raises(ExceptionGroup):
        try:
            raise ExceptionGroup(
                "group", [ValueError(1), TypeError(2), OSError(3), OSError(4)]
            )
        except* TypeError as e:
            print(e.exceptions)
            pass
        except* OSError as e:
            print(e.exceptions)
            pass

    assert capsys.readouterr().out == "(TypeError(2),)\n(OSError(3), OSError(4))\n"


def test_iterators() -> None:
    iterator: Iterator[int] = iter([1, 2])
    assert next(iterator) == 1
    assert next(iterator) == 2

    class MyIterator:
        def __init__(self, value: int) -> None:
            self.value = value
            super().__init__()

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            if self.value == 0:
                raise StopIteration
            self.value -= 1
            return self.value

    assert list(MyIterator(3)) == [2, 1, 0]


def test_generators() -> None:
    generator_comprehension = (i for i in reversed(range(3)))
    assert list(generator_comprehension) == [2, 1, 0]

    def my_generator(value: int) -> Generator[int, None, None]:
        for i in reversed(range(value)):
            yield i
        return  # it raises StopIteration

    assert list(my_generator(3)) == [2, 1, 0]

    def two_times_my_generator(value: int) -> Generator[int, None, None]:
        yield from my_generator(value)
        yield from my_generator(value)

    assert list(two_times_my_generator(3)) == [2, 1, 0, 2, 1, 0]

    # Generator[YieldType, SendType, ReturnType]
    def another_generator() -> Generator[int, bool, str]:
        try:
            flag: bool = yield 1
            if flag:
                yield 2

            try:
                yield 3
            except Exception:
                yield 4

            return "Done"
        finally:
            pass  # clean up when close() is called

    generator = another_generator()
    assert next(generator) == 1
    assert generator.send(True) == 2
    assert next(generator) == 3
    assert generator.throw(RuntimeError) == 4
    try:
        next(generator)
    except StopIteration as e:
        assert e.value == "Done"


def test_call_by_sharing() -> None:
    list1: list[int] = [1, 2]
    list2: list[int] = list1
    assert id(list1) == id(list2)
    assert list1 is list2
    assert list1 == list2

    list2 = [1, 2]
    assert id(list1) != id(list2)
    assert list1 is not list2
    assert list1 == list2

    list3: list[list[bool]] = 2 * [[False]]
    list3[0][0] = True
    assert list3[0][0] == True
    assert list3[1][0] == True
