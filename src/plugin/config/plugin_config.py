from enum import Enum
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_FILTER_TYPE = 'triangle'


class LoggingLevel(Enum):

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class PluginConfig(BaseSettings):

    logging_level: LoggingLevel = Field(LoggingLevel.INFO, alias='LOGGING_LEVEL')
    skip_data_exceptions: bool = Field(True, alias='SKIP_DATA_EXCEPTIONS')

    filter_type: Literal['triangle'] = Field(DEFAULT_FILTER_TYPE, alias='FILTER_TYPE')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


PLUGIN_CONFIG = PluginConfig()
