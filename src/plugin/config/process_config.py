from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProcessFilterType(Enum):

    triangle = 'triangle'


class ProcessConfig(BaseSettings):

    filter_type: ProcessFilterType = Field(ProcessFilterType.triangle, alias='PROCESS_FILTER_TYPE')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


PROCESS_CONFIG = ProcessConfig()
