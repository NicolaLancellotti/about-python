from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ClassVar, Protocol, TypeVar, final, runtime_checkable

import pytest


def test_classes() -> None:
    class Base1:
        def foo(self) -> str:
            return "Base1"

    class Base2:
        def foo(self) -> str:
            return "Base2"

    @final
    class Class(Base1, Base2):
        # ______________________________________
        # Init

        def __init__(self, value: int) -> None:
            self._private_instance_attribute = value
            self.instance_attribute = "instance_attribute"
            super(Base1).__init__()
            super(Base2).__init__()

        # ______________________________________
        # Instance properties

        @property
        def instance_property(self) -> int:
            return self._private_instance_attribute

        @instance_property.setter
        def instance_property(self, value: int) -> None:
            self._private_instance_attribute = value

        @instance_property.deleter
        def instance_property(self) -> None:
            del self._private_instance_attribute

        # ______________________________________
        # Instance methods

        def instance_method(self) -> str:
            return "instance_method"

        # ______________________________________
        # Class attributes

        class_attribute: ClassVar[str] = "class_attribute"
        _private_class_attribute: ClassVar[str] = "_private_class_attribute"

        # ______________________________________
        # Class methods

        @classmethod
        def class_method(cls) -> str:
            cls.class_attribute
            cls._private_class_attribute
            return "class_method"

        # ______________________________________
        # Static methods

        @staticmethod
        def static_method() -> str:
            return "static_method"

    instance: Class = Class(value=0)

    assert instance.__class__ == type(instance) == Class
    assert isinstance(instance, Class)
    assert issubclass(Class, Base1)

    # Instance attributes
    assert instance.instance_attribute == "instance_attribute"

    # Instance Properties
    assert instance.instance_property == 0

    # Instance methods
    assert instance.instance_method() == "instance_method"
    assert Class.instance_method(instance) == "instance_method"

    # Class attributes
    assert instance.class_attribute == "class_attribute"
    assert Class.class_attribute == "class_attribute"

    # Class methods
    assert instance.class_method() == "class_method"
    assert Class.class_method() == "class_method"

    # Static methods
    assert instance.static_method() == "static_method"
    assert Class.static_method() == "static_method"

    # MRO - Method resolution order
    assert instance.foo() == "Base1"


def test_private_name_mangling() -> None:
    class Base:
        def baz(self) -> str:
            return self.__foo()

        def foo(self) -> str:
            return "Base"

        __foo = foo

    class Class(Base):
        def foo(self) -> str:
            return "Class"

    assert Class().baz() == "Base"


def test_slots() -> None:
    class Class:
        __slots__ = ["x", "y"]

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            super().__init__()

    instance: Class = Class(x=1, y=2)
    assert instance.x == 1
    with pytest.raises(AttributeError):
        instance.z = 1  # Error # type: ignore


def test_data_classes() -> None:
    from dataclasses import asdict, astuple, dataclass, field

    @dataclass(slots=True)
    class DataClass:
        string_value: str
        int_value: int = 0
        list_value: list[int] = field(init=False, repr=True, default_factory=list)

    instance = DataClass(string_value="name", int_value=0)
    assert asdict(instance) == {
        "string_value": "name",
        "int_value": 0,
        "list_value": [],
    }
    assert astuple(instance) == ("name", 0, [])


def test_abstract_classes():
    class AbstractClass(ABC):
        @abstractmethod
        def abstract_method(self) -> str:
            ...

        @property
        @abstractmethod
        def abstract_property(self) -> int:
            ...

        # Structural subtyping
        @classmethod
        def __subclasshook__(cls, C):  # type: ignore
            if cls is AbstractClass:
                if any("abstract_method" in C.__dict__ for C in C.__mro__) and any(  # type: ignore
                    "abstract_property" in C.__dict__ for C in C.__mro__  # type: ignore
                ):
                    return True
            return NotImplemented

    # Nominal subtype
    class NominalSubtype(AbstractClass):
        def abstract_method(self) -> str:
            return "NominalSubtype"

        @property
        def abstract_property(self) -> int:
            return 0

    assert isinstance(NominalSubtype(), AbstractClass)

    # Register a subclass as a virtual subclass
    assert not isinstance(str, AbstractClass)
    AbstractClass.register(str)  # This is an error
    assert isinstance(str(), AbstractClass)

    # Structural subtype
    class StructuralSubtype:
        def abstract_method(self) -> str:
            return "StructuralSubtype"

        @property
        def abstract_property(self) -> int:
            return 0

    assert isinstance(StructuralSubtype(), AbstractClass)


def test_protocols() -> None:
    # Structural subtyping
    # runtime_checkable checks only the presence of the required
    # methods, not their type signatures

    T = TypeVar("T")

    @runtime_checkable
    class MyProtocol(Protocol[T]):
        def foo(self, k: T) -> T:
            return k

    class Class:
        def foo(self, k: float) -> float:
            return k

    def func(x: MyProtocol[T], k: T) -> T:
        return x.foo(k)

    assert func(x=Class(), k=1) == 1
    assert isinstance(Class(), MyProtocol)  # It can be surprisingly slow


def test_meta_classes() -> None:
    class MetaClass(type):
        def __init__(
            cls,
            name: str,
            bases: tuple[type, ...],
            attrs: dict[str, Any],
            **kwargs: Any
        ):
            super().__init__(name, bases, attrs)
            cls.class_attribute: str = "class_attribute"
            cls.instance_method: Callable[[Any], str] = lambda self: "instance_method"

        def class_method(cls) -> str:
            return "class_method"

    class Base:
        pass

    class Class(Base, metaclass=MetaClass):
        def foo(self, x: int) -> str:
            return "ClassWithMetaClass"

    assert Class.class_attribute == "class_attribute"
    assert Class.class_method() == "class_method"

    instance = Class()
    assert instance.class_attribute == "class_attribute"  # type: ignore
    with pytest.raises(AttributeError):
        instance.class_method()  # Error # type: ignore

    assert instance.instance_method() == "instance_method"  # type: ignore
