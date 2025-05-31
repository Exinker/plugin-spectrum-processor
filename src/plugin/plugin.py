import logging

from plugin.exceptions import exception_wrapper
from plugin.managers.data_manager import DataManager
from plugin.managers.process_manager import ProcessManager
from plugin.managers.process_manager.filters import load_filter


LOGGER = logging.getLogger('plugin-spectrum-processor')


def plugin_factory() -> 'Plugin':

    data_manager = DataManager()
    process_manager = ProcessManager(
        filter=load_filter(),
    )

    return Plugin(
        data_manager=data_manager,
        process_manager=process_manager,
    )


class Plugin:

    create = plugin_factory

    def __init__(
        self,
        data_manager: DataManager,
        process_manager: ProcessManager,
    ) -> None:

        self.data_manager = data_manager
        self.process_manager = process_manager

    @exception_wrapper
    def run(self, filepath: str) -> str:

        spectra = self.data_manager.parse(
            filepath=filepath,
        )
        processed_spectra = self.process_manager.process(
            spectra=spectra,
        )

        string = self.data_manager.build(
            filepath=filepath,
            processed_spectra=processed_spectra,
        )
        return string
