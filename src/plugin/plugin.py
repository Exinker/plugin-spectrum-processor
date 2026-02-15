import logging
from typing import Self

from plugin.exceptions import exception_wrapper
from plugin.managers.data_manager import DataManager
from plugin.managers.data_manager.exceptions import (
    DataManagerError,
    LoadDataXMLError,
    ParseDataXMLError,
    ParseFilepathXMLError,
    ParseSpectraXMLError,
)
from plugin.managers.data_manager.parsers import (
    AtomSpectraParser,
    FilepathParser,
)
from plugin.managers.data_manager.utils import load_xml
from plugin.managers.process_manager import ProcessManager
from plugin.managers.process_manager.filters import load_filter
from plugin.types import XML


LOGGER = logging.getLogger('plugin-spectrum-processor')


class Plugin:

    @classmethod
    def create(cls) -> Self:

        data_manager = DataManager()
        process_manager = ProcessManager(
            filter=load_filter(),
        )

        return cls(
            data_manager=data_manager,
            process_manager=process_manager,
        )

    def __init__(
        self,
        data_manager: DataManager,
        process_manager: ProcessManager,
    ) -> None:

        self.data_manager = data_manager
        self.process_manager = process_manager

    @exception_wrapper
    def run(self, config_xml: XML) -> str:

        try:
            filepath = FilepathParser.parse(config_xml)

        except ParseFilepathXMLError as error:
            LOGGER.error('%r', error)
            raise

        else:
            LOGGER.info('Filepath to data: %r', filepath)

        try:
            xml = load_xml(filepath)

        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error

        spectra = self.data_manager.parse(
            xml=xml,
        )
        processed_spectra = self.process_manager.process(
            spectra=spectra,
        )

        result = self.data_manager.build(
            xml=xml,
            processed_spectra=processed_spectra,
        )
        return result
