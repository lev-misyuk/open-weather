# OpenWeather API

## Установка зависимостей и виртуального окружения
### 1. Установка `pipenv`:

`pip install pipenv`

### 2. Установка переменной окружения `PIPENV_VENV_IN_PROJECT`, чтобы `pipenv` создал виртуальное окружение в директории с проектом:

`$env:PIPENV_VENV_IN_PROJECT=1` для `powershell` 

`export PIPENV_VENV_IN_PROJECT=1` для `bash`

`set PIPENV_VENV_IN_PROJECT=1` для `cmd`

### 3. Создание файла `.env` с переменными окружения:

`cp example.env .env` для `bash`

`copy example.env .env` для `cmd`

`cpi "example.env" ".env"` для `powershell`

Далее в файл `.env` необходимо вручную дописать все необходимые переменные окружения (например `SQLALCHEMY_DATABASE_URI` и `SQLALCHEMY_TRACK_MODIFICATIONS`)

### 4. Установка виртуального окружения:

`pipenv install`

### 5. Активация виртуального окружения:

`pipenv shell`

## Инициализация базы данных и сервиса миграций, запуск сервиса
### 1. Инициализация базы данных sqlite:

`flask db init`

### 2. Создание первой миграции:

`flask db migrate -m "Initial migration"`

### 3. Применение миграции к базе данных:

`flask db upgrade`

### 4. Запуск сервиса:

`flask run`