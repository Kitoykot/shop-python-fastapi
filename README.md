# Shop API

Учебный интернет-магазин на Python и FastAPI: товары, категории, корзина и авторизация с access/refresh-токенами в Redis. Данные хранятся в PostgreSQL, миграции выполняются через Alembic.

## Требования

- Docker с Docker Compose (на macOS — запущенный Docker Desktop).
- Для тестов на компьютере: Python 3.14 и библиотека PostgreSQL `libpq`, необходимая установленному `psycopg`. В Dockerfile она уже устанавливается. На macOS её можно установить через `brew install libpq`.

Все команды выполняются из корня проекта. Примеры рассчитаны на shell macOS/Linux.

## Запуск приложения в Docker

Создайте локальный файл настроек: .env.local

Заполните `POSTGRES_PASSWORD` в `.env.local`. Случайный пароль можно сгенерировать командой: openssl rand -hex 24

`.env.local` исключён из Git и Docker-образа. В репозитории хранится только шаблон `.env.local.example`.

Проверьте конфигурацию и запустите приложение:

```bash
docker compose --env-file .env.local config --quiet
docker compose --env-file .env.local up -d --build app
```

Compose запустит PostgreSQL и Redis приложения, дождётся их готовности и успешного выполнения `migrations-app`, затем запустит FastAPI. Первый запуск создаёт новую базу: данные из PostgreSQL на компьютере автоматически не переносятся.

- API: http://127.0.0.1:8001/api/v1
- Swagger UI: http://127.0.0.1:8001/docs

Nginx для запуска не требуется. Если он уже установлен на компьютере, запросы можно проксировать на `http://127.0.0.1:8001`.

Проверка состояния и просмотр логов:

## Настройки и подключение к базам

| PostgreSQL приложения | `127.0.0.1:5434` | `postgres:5432` |
| Redis приложения | `127.0.0.1:6381` | `redis:6379` |
| Тестовый PostgreSQL | `127.0.0.1:5433` | `postgres-test:5432` |
| Тестовый Redis | `127.0.0.1:6380` | `redis-test:6379` |

Для подключения к PostgreSQL приложения из DBeaver используйте имя базы, пользователя и пароль из `.env.local`. Host и Port заполняются отдельно.

## Разработка и миграции

Каталоги `app/` и `config/` подключены в контейнер, Uvicorn работает с `--reload`. Изменения Python-кода в этих каталогах вызывают перезапуск приложения без пересборки.

При изменении зависимостей или Dockerfile пересоберите образ:

```bash
docker compose --env-file .env.local up -d --build app
```

Для явного применения новых миграций к БД приложения:

```bash
docker compose --env-file .env.local run --rm --build migrations-app
```

Каталог `migrations/` копируется в образ при сборке, поэтому здесь используется `--build`. Контейнер миграций удаляется после завершения, данные PostgreSQL сохраняются.

## Тесты

Сейчас pytest запускается **на компьютере**, а тестовые PostgreSQL и Redis — в Docker. Адреса `127.0.0.1:5433` и `127.0.0.1:6380` заданы в `tests/integration/conftest.py`. Команда `docker compose exec app pytest` не подходит для текущей настройки: внутри контейнера `127.0.0.1` указывает на сам контейнер.

Создайте и активируйте виртуальное окружение (если оно уже существует, достаточно активации):

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Для импорта настроек приложения при HTTP-тестах нужен локальный `.env` или соответствующие переменные окружения. Для запуска тестов создайте `.env` со следующими значениями; если файл уже используется для локального запуска приложения, сохраните его существующие настройки:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=shop_test
DB_USER=shop_test
DB_PASSWORD=shop_test
REDIS_HOST=127.0.0.1
REDIS_PORT=6380
REDIS_DB=0
```

`.env` и `.env.local` — разные файлы: первый читают настройки Python при локальном запуске, второй используется Compose. `.env` тоже исключён из Git. HTTP-тесты подменяют зависимости приложения тестовыми фикстурами.

Поднимите тестовые сервисы и примените тестовые миграции:

```bash
docker compose --env-file .env.local up -d --wait postgres-test redis-test
docker compose --env-file .env.local run --rm --build migrations
```

`migrations` работает с **тестовой** базой, `migrations-app` — с базой приложения.

Запустите тесты:

```bash
# Все тесты
python -m pytest -q

# Сервисы с моками, без подключения к БД
python -m pytest tests/unit -q

# Репозитории с настоящими PostgreSQL/Redis
python -m pytest tests/integration/repositories -q

# HTTP-маршруты
python -m pytest tests/integration/api -q

# Один файл
python -m pytest tests/integration/repositories/auth/session_repository/test_create_tokens.py -q
```

Организация фикстур:

- `tests/integration/conftest.py` — тестовые подключения и пользователь.
- `tests/integration/api/conftest.py` — подмена подключения FastAPI и авторизации.
- Вложенные `conftest.py` в тестах репозиториев — создание соответствующих репозиториев.

Изменения PostgreSQL откатываются после каждого теста через внешнюю транзакцию. Уже существовавшие данные не очищаются. Фикстура Redis очищает базу `0` отдельного тестового сервера до и после теста через `flushdb()`. Эти фикстуры рассчитаны на последовательный запуск тестов.

## Остановка

Остановить приложение и его базы, сохранив контейнеры:

```bash
docker compose --env-file .env.local stop app postgres redis
```

Остановить и удалить контейнеры всего Compose-проекта, включая тестовые:

```bash
docker compose --env-file .env.local down
```