FROM python:3.11-slim

# Устанавливаем Poetry
ENV POETRY_VERSION=1.6.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Копируем только файлы с описанием зависимостей
COPY pyproject.toml poetry.lock* ./

# Отключаем создание виртуальных окружений и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi

# Копируем остальной код проекта
COPY . .

# Создаём и настраиваем права для директории статических файлов
RUN mkdir -p /app/staticfiles \
 && chmod -R 755 /app/staticfiles

EXPOSE 8000

# Команда запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]