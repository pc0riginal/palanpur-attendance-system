from temple_attendance.settings import *
import os

# Production-specific settings
DEBUG = False

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'attendanceDb',
        'USER': 'baps',
        'PASSWORD': 'Pramukh@71221',
        'HOST': 'pctest101.database.windows.net',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'host_is_server': True,
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}

# Use Django's built-in authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Allowed hosts from environment
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

# CSRF trusted origins
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins.split(',')]
else:
    CSRF_TRUSTED_ORIGINS = ['https://*.koyeb.app', 'http://*.koyeb.app']

print(f"Production settings loaded:")
print(f"  - Database: PostgreSQL (Aiven)")
print(f"  - Allowed Hosts: {ALLOWED_HOSTS}")
print(f"  - Debug: {DEBUG}")