from plugin.config import ProcessFilterType

from .base_filter import AbstractFilter
from .triangle_filter import TriangleFilter


def load_filter(__filter_type: ProcessFilterType) -> AbstractFilter:

    match __filter_type:
        case ProcessFilterType.triangle:
            return TriangleFilter()

    raise NotImplementedError(f'Filter type `{__filter_type}` is not supported yet!')


__all__ = [
    load_filter,
]
