import logging
import time
from collections.abc import Mapping

from plugin.managers.process_manager.filters.base_filter import AbstractFilter
from plugin.presentation.callbacks import AbstractProgressCallback, NullProgressCallback
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-spectrum-processor')


class ProcessManager:

    def __init__(
        self,
        filter: AbstractFilter,
    ) -> None:

        self.filter = filter

    def process(
        self,
        spectra: Mapping[int, Spectrum],
        progress_callback: AbstractProgressCallback | None = None,
    ) -> Mapping[int, Spectrum]:
        progress_callback = progress_callback or NullProgressCallback()
        started_at = time.perf_counter()

        LOGGER.debug(
            'Start to precess %s spectra...',
            len(spectra),
        )
        try:
            processed_spectra = self.filter(
                spectra=spectra,
            )
            return processed_spectra

        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for spectra processing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
