from collections.abc import Callable
from typing import Any, Generic, Optional, Self, TypeVar

import pytest


def test_dunder_methods() -> None:
    from copy import copy, deepcopy

    class Class:
        def __init__(self, values: list[int]) -> None:
            self.values = values

        def __del__(self) -> None:
            # do not raise an exception
            pass

        def __str__(self) -> str:
            return str(self.values)

        def __repr__(self) -> str:
            return repr(self.values)

        def __call__(self, y: int) -> list[int]:
            return [x + y for x in self.values]

        def __bool__(self) -> bool:
            return bool(self.values)

        def __len__(self) -> int:
            return len(self.values)

        def __contains__(self, value: int) -> bool:
            return value in self.values

        def __getitem__(self, index: int) -> int:
            return self.values[index]

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, Class):
                return self.values == other.values
            return False

        def __copy__(self) -> "Class":
            return Class(self.values)

        def __deepcopy__(self, _) -> "Class":
            return Class(self.values)

    instance = Class(values=[1, 2, 3])
    assert str(instance) == "[1, 2, 3]"
    assert repr(instance) == "[1, 2, 3]"
    assert instance(10) == [11, 12, 13]
    assert bool(instance)
    assert len(instance) == 3
    assert 1 in instance
    assert 0 not in instance
    assert instance[0] == 1
    assert instance == copy(instance) == deepcopy(instance)


def test_descriptors(capsys: pytest.CaptureFixture[str]) -> None:
    # Instance lookup priority:
    # - data descriptor
    # - instance variable
    # - non-data descriptor
    # - class variable
    # - __getattr__()

    DescriptorClass = TypeVar("DescriptorClass")
    DescriptorValue = TypeVar("DescriptorValue")

    class Descriptor(Generic[DescriptorClass, DescriptorValue]):
        def __set_name__(self, owner: type[DescriptorClass], name: str) -> None:
            self.name = "_" + name

        # Descriptors that only define __get__()
        # are called non-data descriptors
        def __get__(
            self, obj: DescriptorClass, objtype: Optional[type[DescriptorClass]] = None
        ) -> DescriptorValue:
            value = getattr(obj, self.name)
            print(f"{value = }")
            return value

        # If an object defines __set__() or __delete__(),
        # it is considered a data descriptor.
        def __set__(self, obj: DescriptorClass, value: DescriptorValue) -> None:
            setattr(obj, self.name, value)
            print(f"{value = }")

    class Class:
        value1 = Descriptor[Self, int]()
        value2 = Descriptor[Self, str]()

        def __init__(self) -> None:
            self.value1 = 0
            assert capsys.readouterr().out == "value = 0\n"

            self.value2 = "0"
            assert capsys.readouterr().out == "value = '0'\n"

            super().__init__()

    instance = Class()
    assert instance.value1 == 0
    assert capsys.readouterr().out == "value = 0\n"

    assert instance.value2 == "0"
    assert capsys.readouterr().out == "value = '0'\n"


def test_init_subclass() -> None:
    class Base(object):
        def __init_subclass__(cls, /, value: int, **kwargs: Any):
            super().__init_subclass__(**kwargs)
            cls.value: Callable[[], int] = lambda self: value  # type: ignore

    class Class(Base, value=123):
        pass

    assert Class().value() == 123


def test_setattr() -> None:
    class FrozenClass:
        _isfrozen = False

        def __init__(self, isfrozen: bool) -> None:
            self._isfrozen = isfrozen
            super().__init__()

        def __setattr__(self, key: str, value: Any) -> None:
            if self._isfrozen and not hasattr(self, key):
                raise TypeError("%r is a frozen class" % self)
            object.__setattr__(self, key, value)

    class Class(FrozenClass):
        def __init__(self, value: int) -> None:
            self.value = value
            super().__init__(True)

    instance: Class = Class(10)
    assert instance.value == 10
    with pytest.raises(TypeError):
        instance.x = 10  # Error


def test_getattr() -> None:
    class Class:
        def get_string(self, value: str) -> str:
            return value

        def get_int(self, value: int) -> int:
            return value

    class Proxy:
        def __init__(self, value: Class) -> None:
            self._value = value
            super().__init__()

        def get_string(self, s: str) -> str:
            return self._value.get_string(s.upper())

        def __getattr__(self, name: str) -> Any:
            return getattr(self._value, name)

    instance: Class = Class()
    proxy: Proxy = Proxy(instance)
    assert proxy.get_string("abc") == "ABC"
    assert proxy.get_int(10) == 10


def test_context_managers() -> None:
    LockValue = TypeVar("LockValue")

    class Lock(Generic[LockValue]):
        def __init__(self, value: LockValue) -> None:
            self._value = value
            super().__init__()

        def lock(self) -> LockValue:
            # lock
            return self._value

        def unlock(self) -> None:
            # unlock
            pass

    class LockGuard(Generic[LockValue]):
        def __init__(self, lock: Lock[LockValue]) -> None:
            self._lock = lock
            super().__init__()

        def __enter__(self) -> LockValue:
            return self._lock.lock()

        def __exit__(
            self,
            exception_type: Optional[Any],
            exception_value: Optional[Any],
            traceback: Optional[Any],
        ) -> bool:
            # If the suite was exited due to an exception, and the return value from the __exit__() method was false, the
            # exception is reraised. If the return value was true, the exception is suppressed, and execution continues with
            # the statement following the with statement.
            # If the suite was exited for any reason other than an exception, the return value from __exit__() is ignored,.
            self._lock.unlock()
            return False

    lock: Lock[int] = Lock(1)
    with LockGuard(lock) as value:
        assert value == 1


def test_annotations() -> None:
    def f(x: int) -> str:
        return str(x)

    assert f.__annotations__["x"] == int
