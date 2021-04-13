__all__ = ["my_function"]

from tests.my_package.my_module.my_file import my_function  # type: ignore


def secret_function() -> None:
    pass
