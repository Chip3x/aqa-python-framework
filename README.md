# AQA Python Framework

Фреймворк для автоматизации UI и API тестирования.

## Технологический стек

- **Python 3.11+**
- **pytest** — тестовый фреймворк
- **Playwright** — UI автоматизация
- **httpx** — HTTP клиент для API
- **Pydantic** — валидация данных
- **Allure** — отчётность
- **Poetry** — управление зависимостями

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd AQA_Python
```

### 2. Установка зависимостей

```bash
# Установка Poetry (если не установлен)
pip install poetry

# Установка зависимостей проекта
poetry install

# Установка браузеров Playwright
poetry run playwright install
```

### 3. Настройка окружения

```bash
# Копировать шаблон конфигурации
cp config/.env.example config/.env

# Заполнить секреты в config/.env
```

## Структура проекта

```
AQA_Python/
├── config/                 # Конфигурация
│   ├── settings.py        # Pydantic Settings
│   ├── .env.example       # Шаблон переменных
│   └── environments/      # Env-файлы окружений
├── src/                   # Исходный код
│   ├── api/              # API клиент и endpoints
│   ├── ui/               # Page Objects и компоненты
│   └── utils/            # Утилиты
├── tests/                 # Тесты
│   ├── api/              # API тесты
│   └── ui/               # UI тесты
├── fixtures/              # Pytest фикстуры
├── testdata/              # Тестовые данные и фабрики
└── pyproject.toml         # Конфигурация проекта
```

## Запуск тестов

### Базовые команды

```bash
# Все тесты
poetry run pytest

# API тесты
poetry run pytest tests/api/

# UI тесты
poetry run pytest tests/ui/

# Smoke тесты
poetry run pytest -m smoke

# Regression тесты
poetry run pytest -m regression
```

### Параметры запуска

```bash
# Выбор окружения
poetry run pytest --env=staging

# Выбор браузера
poetry run pytest --browser=firefox

# Запуск в headed режиме
poetry run pytest --headed

# Параллельный запуск
poetry run pytest -n auto

# С Allure отчётом
poetry run pytest --alluredir=allure-results
```

### Комбинированные примеры

```bash
# API smoke на staging
poetry run pytest tests/api/ -m smoke --env=staging -n auto

# UI тесты в Firefox headed
poetry run pytest tests/ui/ --browser=firefox --headed

# Полный прогон с отчётом
poetry run pytest --alluredir=allure-results -n auto
```

## Allure отчёты

```bash
# Генерация отчёта
allure generate allure-results -o allure-report --clean

# Открытие отчёта
allure open allure-report

# Или одной командой
allure serve allure-results
```

## Разработка

### Линтинг и форматирование

```bash
# Проверка кода
poetry run ruff check .

# Автоисправление
poetry run ruff check . --fix

# Форматирование
poetry run ruff format .

# Проверка типов
poetry run mypy src/
```

### Pre-commit хуки

```bash
# Установка хуков
poetry run pre-commit install

# Запуск на всех файлах
poetry run pre-commit run --all-files
```

## Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `ENV` | Окружение (dev/staging) | dev |
| `BASE_URL` | URL для UI тестов | - |
| `API_URL` | URL для API тестов | - |
| `BROWSER` | Браузер (chromium/firefox/webkit) | chromium |
| `HEADLESS` | Headless режим | true |
| `DEFAULT_TIMEOUT` | Таймаут UI (ms) | 30000 |
| `API_TIMEOUT` | Таймаут API (ms) | 10000 |
| `TEST_USER_EMAIL` | Email тестового пользователя | - |
| `TEST_USER_PASSWORD` | Пароль тестового пользователя | - |

### Добавление нового окружения

1. Создать файл `config/environments/<env>.env`
2. Добавить окружение в `settings.py` Literal type
3. Использовать: `pytest --env=<env>`

## CI/CD

Pipeline включает:

- **lint** — проверка кода (ruff, mypy)
- **test** — запуск тестов (smoke на MR, regression на main)
- **report** — генерация Allure отчёта

### GitLab CI Variables

Добавить в Settings → CI/CD → Variables:

- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`
- `JWT_SECRET`
- `OAUTH_CLIENT_ID`
- `OAUTH_CLIENT_SECRET`

## Написание тестов

### API тест

```python
@allure.epic("API")
@allure.feature("Users")
@pytest.mark.api
class TestUsers:

    @allure.title("Create user with valid data")
    @pytest.mark.smoke
    def test_create_user(self, users_api, user_data):
        user = users_api.create_user(user_data)
        assert user.email == user_data.email
```

### UI тест

```python
@allure.epic("UI")
@allure.feature("Login")
@pytest.mark.ui
class TestLogin:

    @allure.title("Login with valid credentials")
    @pytest.mark.smoke
    def test_login(self, login_page, dashboard_page):
        login_page.open()
        login_page.login(email, password)
        dashboard_page.assert_dashboard_loaded()
```

## Лицензия

MIT
