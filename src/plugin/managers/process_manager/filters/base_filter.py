from abc import ABC, abstractmethod
from collections.abc import Mapping

from spectrumlab.spectra import Spectrum


class AbstractFilter(ABC):

    @abstractmethod
    def __call__(self, spectra: Mapping[int, Spectrum]) -> Mapping[int, Spectrum]:
        raise NotImplementedError
