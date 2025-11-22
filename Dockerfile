FROM python:3.12-slim

WORKDIR /app

# Install SQL Server ODBC driver
RUN apt-get update && apt-get install -y curl gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

RUN python manage.py collectstatic --noinput --clear

ENV DEBUG=False

EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 --timeout 120 --workers 2 --env DJANGO_SETTINGS_MODULE=production_settings temple_attendance.wsgi:application"]