from collections.abc import Callable, Iterator
from typing import Literal, Optional, TypeVar, Generic, Any, Generator, AsyncGenerator
from functools import wraps
import asyncio

x: int = 0


def expressions() -> None:
    binary = 0b1010
    assert binary == 10
    octal = 0o12
    assert octal == 10
    hexadecimal = 0xA
    assert hexadecimal == 10

    imaginary = 1j

    x = [1, 2]
    y = x
    assert id(x) == id(y)
    assert x is y
    assert x == y

    y = [1, 2]
    assert id(x) != id(y)
    assert x is not y
    assert x == y

    assert 5 // 3 == 1  # Floot Division
    assert 5 % 3 == 2
    assert -5 // 3 == -2  # Floot Division
    assert -5 % 3 == 1

    assert -10 >> 1 == -5
    assert -10 << 1 == -20

    assert 2 ** 3 == 8
    assert 1 <= 2 <= 3
    assert not True == False
    assert 1 and "Hello" == "Hello"
    assert 1 or "Hello" == 1

    assert (1 if 3 > 2 else 2) == 1

    list = 2 * [[False]]
    list[0][0] = True
    assert list[0][0] == True
    assert list[1][0] == True


def statements() -> None:
    x = 1

    # ______________________________________
    # If
    if x == 1:
        pass
    elif x == 2:
        pass
    else:
        pass

    opt_value: Optional[int] = 10
    # walrus operator
    if value := opt_value:
        assert value == 10
    else:
        assert False

    # ______________________________________
    # For
    # x = 8, 6
    for x in range(8, 4, -2):
        break  # skip the optional else clause
        continue
    else:
        pass

    # ______________________________________
    # While
    while x < 4:
        break  # skip the optional else clause
        continue
    else:
        pass

    # ______________________________________
    # Try
    class MyException(Exception):
        def __init__(self, expression: int, message: str) -> None:
            self.expression = expression
            self.message = message

        def __str__(self) -> str:
            return str(self.expression) + " - " + self.message

    try:
        raise MyException(1, "message")
    except MyException as exc:
        # exc is cleared at the end of the except clause
        x, y = exc.args
        assert x == 1
        assert y == "message"
    except (TypeError, NameError) as exc:
        raise RuntimeError from exc  # exception chaining
        raise RuntimeError from None  # do not chain
        raise RuntimeError  # exception chaining
        raise  # re-raise             # exception chaining
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

    # ______________________________________
    # With statement
    Value = TypeVar("Value")  # Type variable

    class Lock(Generic[Value]):
        def __init__(self, value: Value) -> None:
            self._value = value

        def lock(self) -> Value:
            # lock
            return self._value

        def unlock(self) -> None:
            # unlock
            pass

    class LockGuard(Generic[Value]):
        def __init__(self, lock: Lock[Value]) -> None:
            self._lock = lock

        def __enter__(self) -> Value:
            return self._lock.lock()

        def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]:
            # If the suite was exited due to an exception, and the return value from the __exit__() method was false, the
            # exception is reraised. If the return value was true, the exception is suppressed, and execution continues with
            # the statement following the with statement.
            # If the suite was exited for any reason other than an exception, the return value from __exit__() is ignored,.
            self._lock.unlock()
            return False

    lock: Lock[int] = Lock(1)
    with LockGuard(lock) as value:
        assert value == 1


def functions() -> None:
    # ______________________________________
    # Arguments
    def function_with_arguments(
        pos1: int, pos2: int, /, pos_or_kwd: int, *, kwd1: int, kwd2: int
    ) -> None:
        pass

    function_with_arguments(1, 2, pos_or_kwd=3, kwd1=4, kwd2=5)

    # ______________________________________
    # Default value is evaluated only once

    # example 1
    def func_with_default_value1(a: int, L: list[int] = []) -> list[int]:
        L.append(a)
        return L

    func_with_default_value1(1)
    assert func_with_default_value1(2) == [1, 2]

    def func_with_default_value2(a: int, L: list[int] = None) -> list[int]:
        if L is None:
            L = []
        L.append(a)
        return L

    func_with_default_value2(1)
    assert func_with_default_value2(2) == [2]

    # example 2
    a_list = [1]
    get_last = lambda k=a_list: k[-1]

    assert get_last() == 1
    a_list.append(2)
    assert get_last() == 2

    a_list = [3]
    assert get_last() == 2

    # ______________________________________
    # Closure
    z = 1

    def closure(x: int, y: int) -> int:
        return x + y + z

    assert closure(1, 2) == 4

    # ______________________________________
    # Variadic
    def non_varargs(x: int, y: int, z: int) -> tuple[int, int, int]:
        return x, y, z

    def varargs(*args) -> tuple:
        return args

    args = (1, 2, 3)
    assert non_varargs(*args) == args
    assert varargs(1, 2, 3) == args  # Unpacking Argument Lists
    assert varargs(*args) == args  # Unpacking Argument Lists

    # ______________________________________
    # Keyword arguments
    def keyword_args(**kwargs) -> dict:
        return kwargs

    kwargs = {"x": 1, "y": 2}
    assert keyword_args(x=1, y=2) == kwargs
    assert keyword_args(**kwargs) == kwargs

    # ______________________________________
    # Lambdas
    # They are syntactically restricted to a single expression
    assert (lambda x, y: x + y)(2, 1) == 3

    bad_squares = []
    squares = []
    for x in range(5):
        bad_squares.append(lambda: x ** 2)
        squares.append(lambda n=x: n ** 2)

    assert bad_squares[2]() == 16
    assert squares[2]() == 4

    # ______________________________________
    # Use strings to call functions
    def foo() -> int:
        return 10

    foo_func = locals()["foo"]
    assert foo_func() == 10

    # ______________________________________
    # Decorators
    IntToInt = Callable[[int], int]

    def plus_one(f: IntToInt) -> IntToInt:
        @wraps(f)
        def wrap(x: int) -> int:
            return f(x) + 1

        return wrap

    @plus_one
    def plus_1(x: int) -> int:
        """plus_1 doc"""
        return x

    assert plus_1(1) == 2
    assert plus_1.__doc__ == "plus_1 doc"

    def plus_y(y: int) -> Callable[[IntToInt], IntToInt]:
        def decorator(f: IntToInt) -> IntToInt:
            @wraps(f)
            def wrap(x: int) -> int:
                return f(x) + y

            return wrap

        return decorator

    @plus_y(2)
    def plus_2(x: int) -> int:
        """plus_2 doc"""
        return x

    assert plus_2(1) == 3
    assert plus_2.__doc__ == "plus_2 doc"


def iterators_generators():
    # ______________________________________
    # Iterators
    class AnIterator:
        def __init__(self, value: int) -> None:
            self.value = value

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            if self.value == 0:
                raise StopIteration
            self.value -= 1
            return self.value

    assert list(AnIterator(3)) == [2, 1, 0]

    a_list = [1, 2]
    an_iter = iter(a_list)
    assert next(an_iter) == 1
    assert next(an_iter) == 2

    # ______________________________________
    # Generators
    def generator(value: int) -> Generator[int, None, None]:
        for i in reversed(range(value)):
            yield i
        return  # it raises StopIteration

    assert list(generator(3)) == [2, 1, 0]

    def repeat_two_times(value: int) -> Generator[int, None, None]:
        yield from generator(value)
        yield from generator(value)

    assert list(repeat_two_times(3)) == [2, 1, 0, 2, 1, 0]

    # generator comprehensions
    generator_expression = (i for i in reversed(range(3)))
    assert list(generator_expression) == [2, 1, 0]

    # example from "The Python Language Reference"
    def echo(value=None):
        print("Execution starts when 'next()' is called for the first time.")
        try:
            while True:
                try:
                    value = yield value
                except Exception as e:
                    value = e
        finally:
            print("Don't forget to clean up when 'close()' is called.")

    # generator = echo(1)
    # assert next(generator) == 1
    # assert next(generator) == None
    # assert generator.send(2) == 2
    # generator.throw(TypeError, "spam") == "spam"
    # generator.close()


def corutines():
    sleep = 0

    async def asynchronous_generator(value: int) -> AsyncGenerator[int, None]:
        for i in reversed(range(value)):
            await asyncio.sleep(sleep)
            yield i

    async def coroutine() -> None:
        await asyncio.sleep(sleep)

        list = []
        async for x in asynchronous_generator(2):
            list.append(x)
        assert list == [1, 0]

        # Asynchronous comprehensions
        # generator expression
        gen = (-1 * i async for i in asynchronous_generator(2))
        # list comprehension
        list = [i async for i in gen]
        assert list == [-1, 0]

        # An asynchronous context manager is a context manager that is able to
        # suspend execution in its enter and exit methods
        # async with EXPRESSION as TARGET:
        #     SUITE

    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine())


def scope() -> None:
    global x
    assert x == 0  # global variable

    y: int = 0
    z: int = 0

    def set_non_local() -> None:
        nonlocal y
        y = 1
        z = 1

    set_non_local()
    assert y == 1
    assert z == 0


def packages() -> None:
    def import_x() -> None:
        import package.moduleX.fileX

        assert package.moduleX.fileX.func_x() == "func_x"

    def import_y() -> None:
        import package  # __init__.py -> import package.moduleY

        assert package.moduleY.fileY.func_y() == "func_y"

    def import_as() -> None:
        import package.moduleY.fileY as FILE_Y

        assert FILE_Y.func_y() == "func_y"

    def from_import_as() -> None:
        from package.moduleY.fileY import func_y as FUNC_Y

        assert FUNC_Y() == "func_y"

        from package.moduleY import fileY as FILE_Y

        assert FILE_Y.func_y() == "func_y"

    def dir_func() -> None:
        import math as m

        print(dir(m))  # find out which names a module defines
        print(dir())  # lists the names you have defined currently

    import_x()
    import_y()
    import_as()
    from_import_as()
    # dir_func()
