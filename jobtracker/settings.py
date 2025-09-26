# jobtracker/settings.py

# ... other imports ...
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url # <-- Import dj_database_url

# Load environment variables from .env file (important for SECRET_KEY locally)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-hp#q5=vc!r(3n!rdwm8gs@61_+48^8qj5)ib#+diff*57!_gb_'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ


ALLOWED_HOSTS = []
if 'RENDER' in os.environ:
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jobtracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jobtracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configure PostgreSQL for Render deployment using DATABASE_URL
if 'RENDER' in os.environ:
    # Try to configure using DATABASE_URL environment variable first
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600, # Optional: Reuse database connections for 10 minutes
                conn_health_checks=True, # Optional: Enable connection health checks
            )
        }
    else:
        # Fallback to individual environment variables if DATABASE_URL isn't available
        # (Though linking the DB should provide DATABASE_URL)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql', # <-- Changed engine
                'NAME': os.environ.get('DB_NAME'),        # <-- From Render DB service
                'USER': os.environ.get('DB_USER'),        # <-- From Render DB service
                'PASSWORD': os.environ.get('DB_PASSWORD'),# <-- From Render DB service
                'HOST': os.environ.get('DB_HOST', 'postgres'), # <-- From Render DB service, fallback to 'postgres'
                'PORT': os.environ.get('DB_PORT', '5432'), # Default PostgreSQL port
                 'OPTIONS': {
                    'sslmode': 'require', # Often required by Render
                },
            }
        }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/' # Ensure leading slash

STATICFILES_DIRS = [
    # BASE_DIR / "core" / "static", # Uncomment if you create local static source folders later
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (Uploaded files like resumes)
# https://docs.djangoproject.com/en/5.2/topics/files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles') # Use a specific directory for uploads

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
