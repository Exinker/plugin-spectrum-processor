import logging
import os
import sys
from pathlib import Path


root = Path(__file__).parent.resolve()
os.chdir(root)
sys.path.extend([
    str(root / '.venv'),
    str(root / '.venv\Lib\site-packages'),
    str(root / 'src'),
])

import plugin
from plugin.config import (
    PLUGIN_CONFIG,
)
from plugin.loggers import *
from plugin.types import XML


LOGGER = logging.getLogger('plugin-spectrum-processor')
PLUGIN = plugin.plugin_factory()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('PLUGIN_CONFIG: %s', PLUGIN_CONFIG)

    return PLUGIN.run(config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Users\Exinker\Documents\plugin-room\plugin-spectrum-processor\data\py_spe.xml</input>',
    )
    print(result)
