import logging

import matplotlib.pyplot as plt
import numpy as np

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from spectrumlab.spectra import Spectrum


LOGGER = logging.getLogger('plugin-spectrum-processor')


def estimate_alpha(
    spectrum: Spectrum,
    n_chunks: int,
) -> float:

    alpha = np.zeros(n_chunks)
    fitness = np.zeros(n_chunks)
    for i in range(n_chunks):
        left, right = i*(spectrum.n_numbers // n_chunks), (i + 1)*(spectrum.n_numbers // n_chunks)

        mask = (left < np.arange(spectrum.n_numbers)) & (np.arange(spectrum.n_numbers) <= right)
        index_even = (np.arange(spectrum.n_numbers) % 2 == 0) & mask
        index_odd = (np.arange(spectrum.n_numbers) % 2 == 1) & mask

        x = 1 - np.mean(spectrum.intensity[index_even]) / np.mean(spectrum.intensity[index_odd])
        intensity = spectrum.intensity.copy()
        intensity[0::2] /= 1 - x/2
        intensity[1::2] /= 1 + x/2

        fitness[i] = np.sum((np.abs(np.diff(intensity)))**(1/2))
        alpha[i] = x

    alpha0 = alpha[np.argmin(fitness)]

    if LOGGER.level <= logging.DEBUG:

        fig, (ax_left, ax_right) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

        plt.sca(ax_left)
        plt.scatter(
            alpha, fitness,
            s=2,
        )
        plt.scatter(
            alpha0, min(fitness),
            color='red',
            s=4,
        )
        plt.xlabel(r'$\alpha$')
        plt.ylabel(r'$R$')
        plt.grid(
            color='grey', linestyle=':',
        )

        plt.sca(ax_right)
        plt.plot(
            spectrum.intensity,
            label='raw',
        )
        plt.plot(
            intensity,
            label=rf'$\alpha_{{{alpha0:.4f}}}$',
        )
        plt.grid(
            color='grey', linestyle=':',
        )
        plt.legend(
            loc='upper right',
        )

        fig.show()

    return alpha0


class ScaleFilter(AbstractFilter):

    def __init__(
        self,
        n_chunks: int,
    ) -> None:

        self.n_chunks = n_chunks

    def __call__(
        self,
        spectrum: Spectrum,
    ) -> Spectrum:

        alpha = estimate_alpha(
            spectrum=spectrum,
            n_chunks=self.n_chunks,
        )

        intensity_scaled = spectrum.intensity.copy()
        intensity_scaled[0::2] /= 1 - alpha/2
        intensity_scaled[1::2] /= 1 + alpha/2
        return Spectrum(
            intensity=intensity_scaled,
        )
