# SPECTRUM-PROCESSOR

**SPECTRUM-PROCESSOR** - плагин для ПО [Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html) для обработки спектров.


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2025 г.

## Installation
### Установка Python
Для работы требуется установить Python версии 3.12. *Ссылку на последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*

### Установка виртуального окружения
Зависимости, необходимые для работы приложения, необходимо установить в виртуальное окружение `.venv`. Для этого в командной строке необходимо:
1. Зайти в папку с плагинами: `cd ATOM_PATH\Plugins\python`;
2. Установить пакетный менеджер `uv`: `pip install uv`;
3. Клонировать проект с удаленного репозитория: `git clone https://github.com/Exinker/plugin-spectrum-processor.git`;
4. Зайти в папку с плагином для расчета формы контура пика: `cd plugin-spectrum-processor`;
5. Создать виртуальное окружение и установить необходимые зависимости: `uv sync --no-dev`;

## Usage

### ENV
Преременные окружения плагина:
- `LOGGING_LEVEL: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' = 'INFO'` - уровень логгирования;

Преременные окружения алгоритма обработки спектра:
- `PROCESS_FILTER_TYPE: 'triangle' | 'scale' = 'triangle'` - тип фильтра;
- `PROCESS_WINDOW_SIZE: int = 8` - ширина окна (только для `'scale'` фильтра);
