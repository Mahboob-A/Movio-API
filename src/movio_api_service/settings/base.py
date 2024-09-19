"""
Django settings for movio_api_service project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from environ import Env

env = Env()

# TODO: Change the environment type to .prod when deploying to production
ENVIRONMENT_TYPE = ".dev"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")


APP_DIR = BASE_DIR / "core_apps"

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTH_APPS = [
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "django_elasticsearch_dsl", 
    "django_elasticsearch_dsl_drf",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.event_manager",
    "core_apps.stream",
    "core_apps.es_search", 
]

# installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # Auth middleware
    "core_apps.common.middlewares.AuthJWTMiddleware",
    
    # Video Body Data Validation 
    "core_apps.common.middlewares.VideoUploadMiddleware",
]

ROOT_URLCONF = "movio_api_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "movio_api_service.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# TODO: Change the environment type to .prod when deploying to production

DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



