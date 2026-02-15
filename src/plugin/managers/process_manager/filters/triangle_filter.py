import logging
from collections.abc import Mapping

import matplotlib.pyplot as plt
import numpy as np

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from spectrumlab.spectra import Spectrum


LOGGER = logging.getLogger('plugin-spectrum-processor')


class TriangleFilter(AbstractFilter):

    def __call__(self, spectra: Mapping[int, Spectrum]) -> Mapping[int, Spectrum]:

        processed_spectra = {}
        for n, spectrum in spectra.items():
            intensity = np.convolve(spectrum.intensity, [.25, .5, .25], mode='same')
            processed_spectra[n] = Spectrum(
                intensity=intensity,
            )

        if LOGGER.level <= logging.DEBUG:
            plt.subplots(figsize=(12, 6))

            plt.plot(
                np.concatenate([
                    spectrum.intensity
                    for spectrum in spectra.values()
                ]),
                label=r'$s_{0}$',
            )
            plt.plot(
                np.concatenate([
                    spectrum.intensity
                    for spectrum in processed_spectra.values()
                ]),
                label=r'$s$',
            )
            plt.grid(
                color='grey', linestyle=':',
            )
            plt.legend(
                loc='upper right',
            )
            plt.show()

        return processed_spectra
