# OpenWeather
## Установка зависимостей
### 1. Установка `pipenv`:

`pip install pipenv`

### 2. Установка переменной окружения `PIPENV_VENV_IN_PROJECT`, чтобы `pipenv` создал виртуальное окружение в директории с проектом:

`$env:PIPENV_VENV_IN_PROJECT=1` для `powershell` 

`export PIPENV_VENV_IN_PROJECT=1` для `cmd`

### 3. Установка виртуального окружения:

`pipenv install`

### 4. Активация виртуального окружения:

`pipenv shell`