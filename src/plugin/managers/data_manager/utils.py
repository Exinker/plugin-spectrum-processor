import logging
import xml.etree.ElementTree as ElementTree

from plugin.dto import AtomFilepath
from plugin.managers.data_manager.exceptions import (
    LoadDataXMLError,
)
from plugin.types import XML


LOGGER = logging.getLogger('plugin-spectrum-processor')


def load_xml(filepath: AtomFilepath) -> XML | None:
    """Load `xml` element object from file for a given `filepath`."""

    try:
        xml = ElementTree.parse(filepath)
    except FileNotFoundError as error:
        LOGGER.error('Parse `xml` is failed: %r', error)
        raise LoadDataXMLError('File not found: {!r}!'.format(filepath)) from error

    return xml
