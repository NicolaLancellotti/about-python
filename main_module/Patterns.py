from typing import Any


def proxy() -> None:
    class A:
        def foo(self, s: str) -> str:
            return s

        def bar(self) -> int:
            return 10

    class Proxy:
        def __init__(self, value: A) -> None:
            self._value = value

        def foo(self, s: str) -> str:
            return self._value.foo(s.upper())

        def __getattr__(self, name) -> Any:
            return getattr(self._value, name)

    a = A()
    proxy = Proxy(a)
    assert proxy.foo("abc") == "ABC"
    assert proxy.bar() == 10


def frozen_classes() -> None:
    class FrozenClass:
        _isfrozen = False

        def __init__(self, isfrozen: bool) -> None:
            self._isfrozen = isfrozen

        def __setattr__(self, key: str, value: Any) -> None:
            if self._isfrozen and not hasattr(self, key):
                raise TypeError("%r is a frozen class" % self)
            object.__setattr__(self, key, value)

    class Subclass(FrozenClass):
        def __init__(self, value: int) -> None:
            self.value = value
            FrozenClass.__init__(self, True)

    instance = Subclass(10)
    instance.value
    # instance.x = 10  # Error
