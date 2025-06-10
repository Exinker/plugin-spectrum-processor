# SPECTRUM-PROCESSOR

**SPECTRUM-PROCESSOR** - плагин для ПО [Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html) для обработки спектров.


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2025 г.

## Installation

### Установка Git
Для работы требуется установить Git. *Последнюю версию можно скачать [здесь](https://git-scm.com/downloads/win).*

### Установка Python
Для работы требуется установить Python версии 3.12. *Последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*
Установка зависимостей выполняется с использованием пакетного менеджера `uv`, который можно установить командой: `pip install uv`;

### Установка виртуального окружения
Зависимости, необходимые для работы приложения, необходимо установить в виртуальное окружение `.venv`. Для этого в командной строке необходимо:
1. Зайти в папку с плагинами: `cd ATOM_PATH\Plugins\python`;
2. Клонировать проект с удаленного репозитория: `git clone https://github.com/Exinker/plugin-spectrum-processor.git`;
3. Зайти в папку с плагином для обработки спектров: `cd plugin-spectrum-processor`;
4. Создать виртуальное окружение и установить необходимые зависимости: `uv sync --no-dev`;

## Usage

### ENV
Преременные окружения плагина:
- `LOGGING_LEVEL: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' = 'INFO'` - уровень логгирования;

Преременные окружения алгоритма обработки спектра:
- `PROCESS_FILTER_TYPE: 'triangle' | 'scale' = 'triangle'` - тип фильтра;
- `PROCESS_WINDOW_SIZE: int = 8` - ширина окна (только для `'scale'` фильтра);
