from plugin.config import (
    PLUGIN_CONFIG,
)
from plugin.exceptions import exception_wrapper
from plugin.managers.data_manager import DataManager
from plugin.managers.process_manager import ProcessManager
from plugin.managers.process_manager.filters import load_filter
from plugin.types import XML


def plugin_factory() -> 'Plugin':

    data_manager = DataManager()
    process_manager = ProcessManager(
        filter=load_filter(PLUGIN_CONFIG.filter_type),
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
    def run(
        self,
        xml: XML,
    ) -> str:

        data = self.data_manager.parse(
            xml=xml,
        )
        processed_spectra = self.process_manager.process(
            spectra=data.spectra,
        )

        result = self.data_manager.build(
            xml=xml,
            processed_spectra=processed_spectra,
        )
        return result
