FROM python:3.12-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

RUN python manage.py collectstatic --noinput --clear

ENV DEBUG=False

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --settings=production_settings && gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=production_settings temple_attendance.wsgi:application"]