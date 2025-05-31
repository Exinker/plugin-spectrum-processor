from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProcessFilterType(Enum):

    triangle = 'triangle'
    scale = 'scale'


class ProcessConfig(BaseSettings):

    filter_type: ProcessFilterType = Field(ProcessFilterType.triangle, alias='PROCESS_FILTER_TYPE')
    window_size: int = Field(8, ge=4, le=256, alias='PROCESS_WINDOW_SIZE')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


PROCESS_CONFIG = ProcessConfig()
