from .base_filter import AbstractFilter
from .triangle_filter import TriangleFilter


def load_filter(__type: str) -> AbstractFilter:

    if __type == 'triangle':
        return TriangleFilter()
    
    raise NotImplementedError(f'Filter {__type} is not supported yet!')


__all__ = [
    load_filter,
]
