FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

# Установка зависимостей PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Установка зависимостей Python
RUN pip install SQLAlchemy psycopg2-binary

# Инструкции по запуску сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
