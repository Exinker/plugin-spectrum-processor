"""Atom plugin to process spectrum."""

from datetime import datetime

import pkg_resources

from .plugin import plugin_factory


distribution = pkg_resources.get_distribution('plugin_spectrum_processor')
__name__ = 'plugin-spectrum-processor'
__version__ = distribution.version
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)

__all__ = [
    plugin_factory,
]
