from __future__ import annotations
from types import NotImplementedType
from typing import Callable

def special_case_repr(new_repr: Callable[..., str|NotImplementedType]):
    """
    Decorator that overrides a classes __repr__ method, but calls the old __repr__ method if it returns NotImplemented.
    """
    def decorator[T](cls: T) -> T:
        old_repr = cls.__repr__
        def handler(*args, **kwargs) -> str:
            result = new_repr(*args, **kwargs)
            if result is NotImplemented:
                return old_repr(*args, **kwargs)
            else:
                return result
        cls.__repr__ = handler
        return cls
    return decorator


__all__ = ["special_case_repr"]
