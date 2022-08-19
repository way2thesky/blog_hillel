# blog_hillel/settings/base.py

import os
import sys
import random
import pathlib
from typing import Any, Dict, List, Union  # pylint: disable=W0611

import environ


gettext = lambda string: string  # noqa: E731

NAME: str = "blog_hillel"
path: pathlib.Path = pathlib.Path(__file__).absolute()
BASE_DIR: str = str(path.parent.parent.parent)
sys.path.insert(0, str(BASE_DIR))

env: environ.Env = environ.Env()
env.read_env()

ENVIRONMENT: str = env("ENVIRONMENT")
SECRET_KEY: str = (
    env("SECRET_KEY")
    if env("SECRET_KEY", default="")
    else "".join(
        [
            random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")  # nosec
            for i in range(50)
        ]
    )
)

# db
DATABASES: Dict[str, Dict[str, Union[str, int]]] = {
    "default": env.db("DATABASE_URL"),
}

# apps
INSTALLED_APPS: List[str] = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    'django_celery_results',
    'django_extensions',
    'widget_tweaks',

    # blog_hillel
    "blog_hillel.apps.articles",

    # API
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'rest_framework_simplejwt',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',



]

MIDDLEWARE: List[str] = [
    # django
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
APPEND_SLASH: bool = True

TEMPLATES: List[Dict[str, Any]] = [  # noqa: ECE001
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(os.path.join(BASE_DIR, NAME, "templates"))],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                # django
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                # django
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]  # noqa: E501

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# i18n/l10n settings
LANGUAGE_CODE: str = "en"
LANGUAGES = [["en", gettext("English")]]  # type: ignore
DEFAULT_LANGUAGE: str = "en"
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True
USE_THOUSAND_SEPARATOR: bool = True


# static/media settings
MEDIA_ROOT: str = str(pathlib.Path(BASE_DIR).joinpath("media"))
STATIC_ROOT: str = str(pathlib.Path(BASE_DIR).joinpath("static"))
app_static: str = str(pathlib.Path(BASE_DIR).joinpath(NAME, "static"))
STATICFILES_DIRS: List[str] = [app_static]

STATIC_URL: str = "/static/"
MEDIA_URL: str = "/media/"

# site framework settings
SITE_ID: int = 1

# security settings
ALLOWED_HOSTS: List[str] = ["*"]

# protocol settings
URL_PROTOCOL: str = "https"

# env notice settings
ENVIRONMENT_NAME: str = ENVIRONMENT

# authentication settings
AUTHENTICATION_BACKENDS: List[str] = [
    "django.contrib.auth.backends.ModelBackend",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
