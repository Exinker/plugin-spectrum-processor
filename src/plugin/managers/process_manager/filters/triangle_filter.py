from collections.abc import Mapping

import numpy as np

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from spectrumlab.spectra import Spectrum


class TriangleFilter(AbstractFilter):

    def __call__(self, spectra: Mapping[int, Spectrum]) -> Mapping[int, Spectrum]:

        processed_spectra = {}
        for n, spectrum in spectra.items():
            intensity = np.convolve(spectrum.intensity, [.25, .5, .25], mode='same')
            processed_spectra[n] = Spectrum(
                intensity=intensity,
            )
        return processed_spectra
