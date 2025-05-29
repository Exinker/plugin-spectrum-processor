import logging
import os
import sys
from pathlib import Path

root = Path(__file__).parent.resolve()
sys.path = [
    str(root / '.venv'),
    str(root / '.venv\Lib\site-packages'),
    str(root / 'src'),
    *sys.path,
]
os.chdir(root)

import plugin
from plugin.config import PLUGIN_CONFIG
from plugin.managers.data_manager.exceptions import ParseFilepathXMLError
from plugin.managers.data_manager.parsers import FilepathParser
from plugin.loggers import *
from plugin.types import XML


LOGGER = logging.getLogger('plugin-spectrum-processor')
PLUGIN = plugin.plugin_factory()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('PLUGIN_CONFIG: %s', PLUGIN_CONFIG)

    try:
        filepath = FilepathParser.parse(config_xml)
    except ParseFilepathXMLError as error:
        LOGGER.error('%r', error)
        raise

    LOGGER.info(
        'Filepath to data: %r', filepath,
    )
    return PLUGIN.run(filepath)


if __name__ == '__main__':
    string = process_xml(
        config_xml=r'<input>C:\Users\Exinker\Documents\plugin-room\plugin-spectrum-processor\data\py_spe.xml</input>',
    )
    print(string)
