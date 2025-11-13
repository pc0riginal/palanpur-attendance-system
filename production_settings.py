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

# MongoDB Configuration - ensure environment variables are used
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'temple_attendance')

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is required in production")

# Allowed hosts from environment
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []

print(f"Production settings loaded:")
print(f"  - MongoDB URI: {'Set' if MONGODB_URI else 'Not set'}")
print(f"  - MongoDB Name: {MONGODB_NAME}")
print(f"  - Allowed Hosts: {ALLOWED_HOSTS}")
print(f"  - Debug: {DEBUG}")