import logging
from functools import wraps

LOGGER = logging.getLogger('plugin-spectrum-processor')


def get_initial_exception(error: Exception) -> Exception:

    parent = error.__cause__ or error.__context__
    if parent is None:
        return error

    return get_initial_exception(parent)


def exception_wrapper(func):

    @wraps(func)
    def wrapped(*args, **kwargs):

        try:
            result = func(*args, **kwargs)

        except Exception as error:
            LOGGER.warning('Spectra processing ware not completed successfully!')
            raise get_initial_exception(error)

        else:
            LOGGER.info('Spectra processing are completed!')
            return result

    return wrapped


class PluginError(Exception):
    pass
