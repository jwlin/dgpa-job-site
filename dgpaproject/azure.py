from .settings import * 
import os

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
ALLOWED_HOSTS += ["dgpajobs.net"]

CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS += ["https://dgpajobs.net"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

SECRET_KEY = os.environ.get('SECRET_KEY')

STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT", "./static/") 

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')

DEBUG = True if os.environ.get('DEBUG') == "True" else False

ADMIN_ENABLED = True if os.environ.get('ADMIN_ENABLED') == "True" else False
