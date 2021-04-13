from __future__ import annotations
import copy
import logging
import typing

logging.basicConfig(level=logging.CRITICAL)

# ____________________________________________________________
# Utility


def bar(self, x: int) -> int:
    return x


# ____________________________________________________________
# Metaclasses


class Meta(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.class_property_from_meta: str = "class_property_from_meta"
        cls.instance_method_from_meta = lambda self: "instance_method_from_meta"

    def class_method_from_meta(cls) -> str:
        return "class_method_from_meta"


# ____________________________________________________________
# Descriptors


class LoggedAccess:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    # Descriptors that only define __get__()
    # are called non-data descriptors
    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info("Accessing %r giving %r", self.public_name, value)
        return value

    # If an object defines __set__() or __delete__(),
    # it is considered a data descriptor.
    def __set__(self, obj, value):
        logging.info("Updating %r to %r", self.public_name, value)
        setattr(obj, self.private_name, value)


# ____________________________________________________________
# Classes
#
# Instance lookup priority:
# - data descriptor
# - instance variable
# - non-data descriptor
# - class variable
# - __getattr__()


class ClassWithMetaClass(metaclass=Meta):
    def foo(self, x: int) -> str:
        return "ClassWithMetaClass"


class BaseClass(object):
    def __init_subclass__(cls, /, value, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.baz = lambda self: value

    def foo(self, x: int) -> str:
        return "BaseClass"


BaseAlias = BaseClass


class SomeClass(BaseAlias, ClassWithMetaClass, value="123"):
    # ______________________________________
    # Init
    def __init__(self, value: int) -> None:
        self.descriptor = 1
        self._value = value
        super().__init__()

    # ______________________________________
    # Instance Properties
    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        del self._value

    # ______________________________________
    # Methods
    def foo(self, x: int) -> str:
        return super().foo(x) + str(x)

    bar = bar

    def _private_method(self) -> None:
        pass

    # ______________________________________
    # Class Properties & Methods
    class_property: str = "class_property"
    _private_class_property: str = "private_class_property"
    __double_underscore: str = "__double_underscore"

    @classmethod
    def class_method(cls) -> str:
        cls.class_property
        cls._private_class_property
        return "class_method"

    # ______________________________________
    # Static Methods
    @staticmethod
    def static_method() -> str:
        return "static_method"

    # ______________________________________
    # Special Methods
    def __del__(self) -> None:
        # do not raise an exception
        pass

    def __str__(self) -> str:
        return "__str__"

    def __repr__(self) -> str:
        return "__repr__"

    def __copy__(self) -> SomeClass:
        return SomeClass(self.value)

    def __call__(self, x: int) -> int:
        return x + 1

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return 1

    # Membership test operations
    def __contains__(self, item) -> bool:
        return item in [0, 1]

    # Subscription
    def __getitem__(self, key) -> int:
        return key + 1

    # ______________________________________
    # Descriptor
    descriptor = LoggedAccess()


# ____________________________________________________________
# Class with slots


class ClassWithSlots(object):
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y


# ____________________________________________________________
# Run


def run() -> None:
    instance: SomeClass = SomeClass(10)

    # ______________________________________
    # Types
    assert instance.__class__ == type(instance)
    assert isinstance(instance, SomeClass)
    assert issubclass(SomeClass, BaseAlias)

    # ______________________________________
    # Instance properties
    instance.value = 100
    assert instance.value == 100
    # del instance.value

    # ______________________________________
    # Instance methods
    value, result = 10, "BaseClass10"

    assert SomeClass.foo(instance, value) == result
    assert instance.foo(value) == result
    assert instance.bar(1) == 1

    assert instance.baz() == "123"  # type: ignore

    method_object = instance.foo
    assert method_object(value) == result
    method_object2 = SomeClass.foo.__get__(instance, SomeClass)  # type: ignore
    assert method_object2(value) == result

    instance_object = method_object.__self__  # type: ignore
    assert instance_object is instance

    function_object = method_object.__func__  # type: ignore
    assert function_object(instance_object, value) == result

    # ______________________________________
    # Class properties
    assert SomeClass.class_property == "class_property"
    assert SomeClass._SomeClass__double_underscore == "__double_underscore"  # type: ignore

    # ______________________________________
    # Class & static methods

    assert SomeClass.class_method() == "class_method"
    assert instance.class_method() == "class_method"

    assert SomeClass.static_method() == "static_method"
    assert instance.static_method() == "static_method"

    # ______________________________________
    # Special methods
    assert str(instance) == "__str__"
    assert f"{instance!s}" == "__str__"
    assert f"{instance!r}" == "__repr__"

    new = copy.copy(instance)
    assert new.value == 100

    # Call
    assert instance(10) == 11

    assert len(instance) == 1

    # Membership test operations
    assert 0 in instance
    assert 2 not in instance

    # Subscription
    assert instance[10] == 11

    # ______________________________________
    # Meta

    assert instance.instance_method_from_meta() == "instance_method_from_meta"  # type: ignore

    assert SomeClass.class_property_from_meta == "class_property_from_meta"
    assert instance.class_property_from_meta == "class_property_from_meta"  # type: ignore

    assert SomeClass.class_method_from_meta() == "class_method_from_meta"
    # instance.class_method_from_meta()  # error

    # ______________________________________
    # Descriptor
    assert instance.descriptor == 1

    # ______________________________________
    # Class with slots

    class_with_slots: ClassWithSlots = ClassWithSlots(x=1, y=2)
    # class_with_slots.z = 1 # error
