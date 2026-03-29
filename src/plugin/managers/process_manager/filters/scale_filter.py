import logging
from collections.abc import Mapping

import matplotlib.pyplot as plt
import numpy as np

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from spectrumlab.spectra import EmittedSpectrum
from spectrumlab.types import Array


LOGGER = logging.getLogger('plugin-spectrum-processor')


def estimate_mask_v1(
    spectrum: EmittedSpectrum,
    window_size: int,
) -> Array[bool]:
    n_chunks = spectrum.n_numbers // window_size

    mask = np.full(spectrum.n_numbers, False)
    for i in range(n_chunks):
        left, right = i*window_size, (i + 1)*window_size

        sign = np.sign(np.diff(spectrum.intensity[left:right]))
        n_sign_changes = np.sum(np.diff(sign[sign != 0]) != 0)
        mask[left:right] = (n_sign_changes == window_size - 2).item()

    return mask


def estimate_mask_v2(
    spectrum: EmittedSpectrum,
    window_size: int,
) -> Array[bool]:

    mask = np.full(spectrum.n_numbers, False)
    for i in range(spectrum.n_numbers):
        left = max(i - window_size // 2, 0)
        right = min(i + window_size // 2, spectrum.n_numbers)

        sign = np.sign(np.diff(spectrum.intensity[left:right]))
        n_sign_changes = np.sum(np.diff(sign[sign != 0]) != 0)
        if (n_sign_changes == window_size - 2).item():
            mask[i] = True

    return mask


def estimate_alpha(
    spectrum: EmittedSpectrum,
    mask: Array[bool],
) -> float:

    index_even = (np.arange(spectrum.n_numbers) % 2 == 0) & mask
    index_odd = (np.arange(spectrum.n_numbers) % 2 == 1) & mask

    R = np.mean(spectrum.intensity[index_even]) / np.mean(spectrum.intensity[index_odd])

    alpha = 2 * (1 - R) / (1 + R)
    if np.isfinite(alpha):
        return alpha
    return 0


def estimate_params(
    spectrum: EmittedSpectrum,
    mask: Array[bool],
) -> float:

    index_even = (np.arange(spectrum.n_numbers) % 2 == 0) & mask
    index_odd = (np.arange(spectrum.n_numbers) % 2 == 1) & mask

    R = np.mean(spectrum.intensity[index_even]) / np.mean(spectrum.intensity[index_odd])

    alpha = 2 * (1 - R) / (1 + R)
    if np.isfinite(alpha):
        return alpha
    return 0


class ScaleFilter(AbstractFilter):

    def __init__(
        self,
        window_size: int,
    ) -> None:

        self.window_size = window_size

    def __call__(
        self,
        spectra: Mapping[int, EmittedSpectrum],
    ) -> Mapping[int, EmittedSpectrum]:

        processed_spectra = {}
        for n, spectrum in spectra.items():
            alpha = estimate_alpha(
                spectrum=spectrum,
                window_size=self.window_size,
            )
            LOGGER.info(
                'Process %s alpha: %s', f'{n+1:>4}', f'{alpha:.4f}',
            )

            intensity_scaled = spectrum.intensity.copy()
            intensity_scaled[0::2] /= 1 - alpha/2
            intensity_scaled[1::2] /= 1 + alpha/2

            processed_spectra[n] = EmittedSpectrum(
                intensity=intensity_scaled,
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
