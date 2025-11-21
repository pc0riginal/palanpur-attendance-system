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

# PostgreSQL Database for all models and data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'defaultdb'),
        'USER': os.environ.get('DB_USER', 'avnadmin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'REDACTED'),
        'HOST': os.environ.get('DB_HOST', 'pg-363fbcb5-bapspalanapurmandir-becb.j.aivencloud.com'),
        'PORT': os.environ.get('DB_PORT', '24821'),
        'OPTIONS': {
            'sslmode': 'require',
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
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []

print(f"Production settings loaded:")
print(f"  - Database: PostgreSQL (Aiven)")
print(f"  - Allowed Hosts: {ALLOWED_HOSTS}")
print(f"  - Debug: {DEBUG}")