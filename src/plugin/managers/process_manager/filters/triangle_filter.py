import numpy as np

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from spectrumlab.spectra import Spectrum


class TriangleFilter(AbstractFilter):

    def __call__(self, spectrum: Spectrum) -> Spectrum:

        intensity = np.convolve(spectrum.intensity, [.25, .5, .25], mode='same')
        return Spectrum(
            intensity=intensity,
        )
