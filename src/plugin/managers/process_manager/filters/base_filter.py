from abc import ABC, abstractmethod
from collections.abc import Mapping

from spectrumlab.spectra import EmittedSpectrum


class AbstractFilter(ABC):

    @abstractmethod
    def __call__(self, spectra: Mapping[int, EmittedSpectrum]) -> Mapping[int, EmittedSpectrum]:
        raise NotImplementedError
