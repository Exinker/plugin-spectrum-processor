from plugin.config import ProcessFilterType, PROCESS_CONFIG

from .base_filter import AbstractFilter
from .scale_filter import ScaleFilter
from .triangle_filter import TriangleFilter


def load_filter() -> AbstractFilter:

    match PROCESS_CONFIG.filter_type:
        case ProcessFilterType.triangle:
            return TriangleFilter()
        case ProcessFilterType.scale:
            return ScaleFilter(
                n_chunks=PROCESS_CONFIG.n_chunks,
            )

    raise NotImplementedError(f'Filter type `{PROCESS_CONFIG.filter_type}` is not supported yet!')


__all__ = [
    load_filter,
]
