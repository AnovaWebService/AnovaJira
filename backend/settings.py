import os
from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve()

# Директория хранения media-файлов
MEDIA_ROOT = BASE_DIR / "media"

# Ссылка на подключение к БД
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///main.sqlite3")

# Флаг отладки
DEBUG = bool(os.getenv("DEBUG", True))

# Данные, по которым будет работать бекенд.
HOST = os.getenv("HOST", "0.0.0.0")  # noqa: S104
PORT = int(os.getenv("PORT", 8080))  # noqa: PLW1508

# Секретный ключ проекта, для хеширования паролей, и так же их валидации
SECRET_KEY = os.getenv("SECRET_KEY", "d9847115-9b80-4f47-ba09-be5539325d0a")
