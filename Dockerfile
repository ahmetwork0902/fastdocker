FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app
COPY ./static /app/static
COPY ./nginx.conf /etc/nginx/nginx.conf

RUN pip install --no-cache-dir sqlalchemy psycopg2

CMD ["nginx", "-g", "daemon off;"]
