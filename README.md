# AQA Python Framework

A framework for UI and API test automation.

## Technology Stack

- **Python 3.11+**
- **pytest** — test framework
- **Playwright** — UI automation
- **httpx** — HTTP client for API
- **Pydantic** — data validation
- **Allure** — reporting
- **Poetry** — dependency management

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd AQA_Python
```

### 2. Install dependencies

```bash
# Install Poetry (if not installed)
pip install poetry

# Install project dependencies
poetry install

# Install Playwright browsers
poetry run playwright install
```

### 3. Environment setup

```bash
# Copy configuration template
cp config/.env.example config/.env

# Fill in secrets in config/.env
```

## Project Structure

```
AQA_Python/
├── config/                 # Configuration
│   ├── settings.py        # Pydantic Settings
│   ├── .env.example       # Variables template
│   └── environments/      # Environment-specific env files
├── src/                   # Source code
│   ├── api/              # API client and endpoints
│   ├── ui/               # Page Objects and components
│   └── utils/            # Utilities
├── tests/                 # Tests
│   ├── api/              # API tests
│   └── ui/               # UI tests
├── fixtures/              # Pytest fixtures
├── testdata/              # Test data and factories
└── pyproject.toml         # Project configuration
```

## Running Tests

### Basic commands

```bash
# All tests
poetry run pytest

# API tests
poetry run pytest tests/api/

# UI tests
poetry run pytest tests/ui/

# Smoke tests
poetry run pytest -m smoke

# Regression tests
poetry run pytest -m regression
```

### Run parameters

```bash
# Select environment
poetry run pytest --env=staging

# Select browser
poetry run pytest --browser=firefox

# Run in headed mode
poetry run pytest --headed

# Parallel run
poetry run pytest -n auto

# With Allure report
poetry run pytest --alluredir=allure-results
```

### Combined examples

```bash
# API smoke on staging
poetry run pytest tests/api/ -m smoke --env=staging -n auto

# UI tests in Firefox headed
poetry run pytest tests/ui/ --browser=firefox --headed

# Full run with report
poetry run pytest --alluredir=allure-results -n auto
```

## Allure Reports

```bash
# Generate report
allure generate allure-results -o allure-report --clean

# Open report
allure open allure-report

# Or with one command
allure serve allure-results
```

## Development

### Linting and formatting

```bash
# Check code
poetry run ruff check .

# Auto-fix
poetry run ruff check . --fix

# Format
poetry run ruff format .

# Type checking
poetry run mypy src/
```

### Pre-commit hooks

```bash
# Install hooks
poetry run pre-commit install

# Run on all files
poetry run pre-commit run --all-files
```

## Configuration

### Environment Variables

| Variable             | Description                       | Default  |
|----------------------|-----------------------------------|----------|
| `ENV`                | Environment (dev/staging)         | dev      |
| `BASE_URL`           | URL for UI tests                  | -        |
| `API_URL`            | URL for API tests                 | -        |
| `BROWSER`            | Browser (chromium/firefox/webkit) | chromium |
| `HEADLESS`           | Headless mode                     | false    |
| `DEFAULT_TIMEOUT`    | UI timeout (ms)                   | 15000    |
| `API_TIMEOUT`        | API timeout (ms)                  | 10000    |
| `TEST_USER_EMAIL`    | Test user email                   | -        |
| `TEST_USER_PASSWORD` | Test user password                | -        |

### Adding a new environment

1. Create file `config/environments/<env>.env`
2. Add environment to `settings.py` Literal type
3. Use: `pytest --env=<env>`

## CI/CD

Pipeline includes:

- **lint** — code checking (ruff, mypy)
- **test** — run tests (smoke on MR, regression on main)
- **report** — Allure report generation

### GitLab CI Variables

Add in Settings → CI/CD → Variables:

- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`
- `JWT_SECRET`
- `OAUTH_CLIENT_ID`
- `OAUTH_CLIENT_SECRET`

## Writing Tests

### API test

"""python
@allure.epic("API")
@allure.feature("Users")
@pytest.mark.api
class TestUsers:

    @allure.title("Create user with valid data")
    @pytest.mark.smoke
    def test_create_user(self, users_api, user_data):
        user = users_api.create_user(user_data)
        assert user.email == user_data.email
"""

### UI test

"""python
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
"""
