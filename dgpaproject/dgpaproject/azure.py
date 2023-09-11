import os

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),  # localhost'; or an IP Address that your DB is hosted on
        'PORT': os.environ.get('DB_PORT')
    }
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

SECRET_KEY = os.environ.get('SECRET_KEY')

STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT", "./static/") 

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')

DEBUG = False