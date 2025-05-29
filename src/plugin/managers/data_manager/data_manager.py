import logging
import time
from base64 import b64encode
from collections.abc import Mapping
from io import StringIO
import xml.etree.ElementTree as ElementTree

import matplotlib.pyplot as plt
import numpy as np

from plugin.managers.data_manager.exceptions import (
    DataManagerError,
    LoadDataXMLError,
    ParseDataXMLError,
    ParseSpectraXMLError,
)
from plugin.managers.data_manager.parsers import AtomSpectraParser
from plugin.managers.data_manager.parsers.atom_spectra_parser import numpy_array_from_b64
from plugin.managers.data_manager.utils import load_xml
from spectrumlab.spectra import Spectrum


LOGGER = logging.getLogger('plugin-spectrum-processor')


class DataManager:

    def parse(
        self,
        filepath: str,
    ) -> Mapping[int, Spectrum]:

        started_at = time.perf_counter()
        try:
            xml = load_xml(filepath)
        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error

        try:
            spectra = AtomSpectraParser.from_xml(xml=xml)
            return spectra
        except ParseSpectraXMLError as error:
            LOGGER.error('Parse `spectra` is failed: %r', error)
            raise ParseSpectraXMLError from error
        except Exception as error:
            LOGGER.error('Parse `spectra` is failed with unexpected error: %r', error)
            raise ParseSpectraXMLError from error
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for data parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )

    def build(
        self,
        filepath: str,
        processed_spectra: Mapping[int, Spectrum],
    ) -> str:

        try:
            xml = load_xml(filepath)
        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error

        try:
            buffer = np.concat([
                spectrum.intensity
                for spectrum in processed_spectra.values()
            ], dtype=np.double).tobytes()
            xml.find('probes/probe/spe/data/yvals').text = b64encode(buffer).decode('utf-8')

            string = ElementTree.tostring(
                xml.getroot(),
                encoding='utf-8',
            ).decode('utf-8')
            return string
        except Exception as error:
            raise DataManagerError from error

        else:

            if LOGGER.level <= logging.DEBUG:
                xpath = 'probes/probe/spe/data/yvals'

                xml = load_xml(filepath)
                spectrum_before = numpy_array_from_b64(
                    buffer=xml.find(xpath).text,
                    dtype=np.double,
                )

                xml = StringIO()
                xml.write(string)
                xml.seek(0)
                spectrum_after = numpy_array_from_b64(
                    buffer=ElementTree.parse(xml).find(xpath).text,
                    dtype=np.double,
                )

                plt.plot(spectrum_before, label='before')
                plt.plot(spectrum_after, label='after')
                plt.xlabel('$\lambda$, нм')
                plt.ylabel('$I$, %')
                plt.legend(
                    loc='upper left',
                )
                plt.grid(
                    color='grey', linestyle=':',
                )
                plt.show()

            if LOGGER.level <= logging.DEBUG:
                with open('.xml', 'w') as file:
                    file.write(string)