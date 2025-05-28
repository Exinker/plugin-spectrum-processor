import logging
import time
from base64 import b64encode
from collections.abc import Mapping
import xml.etree.ElementTree as ElementTree

import numpy as np

from plugin.dto import AtomData
from plugin.managers.data_manager.exceptions import (
    DataManagerError,
    LoadDataXMLError,
    ParseDataXMLError,
    ParseFilepathXMLError,
)
from plugin.managers.data_manager.parsers import (
    AtomDataParser,
    FilepathParser,
)
from plugin.managers.data_manager.parsers.atom_data_parser import (
    load_xml,
)
from plugin.types import XML
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-spectrum-processor')


class DataManager:

    def parse(
        self,
        xml: XML,
    ) -> AtomData:

        started_at = time.perf_counter()
        try:
            filepath = FilepathParser.parse(xml)
        except ParseFilepathXMLError as error:
            LOGGER.error('%r', error)
            raise
        else:
            LOGGER.info('Filepath to data: %r', filepath)
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for filepath parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )

        started_at = time.perf_counter()
        try:
            data = AtomDataParser.parse(filepath)
            return data
        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for data parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )

    def build(
        self,
        xml: XML,
        processed_spectra: Mapping[int, Spectrum],
    ) -> str:

        filepath = FilepathParser.parse(xml)

        started_at = time.perf_counter()
        try:
            tree = ElementTree.parse(filepath)

            buffer = np.concat([
                spectrum.intensity
                for spectrum in processed_spectra.values()
            ], dtype=np.double).tobytes()
            tree.find('probes').find('probe/spe/data/yvals').text = b64encode(buffer).decode('utf-8')

            return ElementTree.tostring(tree.getroot(), encoding='utf-8').decode('utf-8')
        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for build: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
