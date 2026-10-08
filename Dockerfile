FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY manage.py .
COPY mono ./mono
COPY studio ./studio
RUN DJANGO_DEBUG=true python manage.py collectstatic --noinput
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn mono.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --access-logfile -"]
