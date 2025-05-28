from abc import ABC, abstractmethod

from spectrumlab.spectra import Spectrum


class AbstractFilter(ABC):

    @abstractmethod
    def __call__(self, spectrum: Spectrum) -> Spectrum:
        raise NotImplementedError
