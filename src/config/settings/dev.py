# import os

from config.settings.base import *  # NOQA:F403

SECRET_KEY = "django-insecure-mp3m1$h1($o)*wekb!t2=y$b^u)16t8gt)m6r$xbyxnx647l(4"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ["django_extensions"]  # NOQA: F405

# if os.environ.get("GITHUB_WORKFLOW"):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "postgres",
#             "USER": "postgres",
#             "PASSWORD": "postgres",
#             "HOST": "0.0.0.0",
#             "PORT": 5432,
#         },
#     }
# else:
#     DATABASES = {
#         "default_sqllite": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",  # NOQA:F405
#         },
#         # "default_local": {
#         #     "ENGINE": "django.db.backends.postgresql",
#         #     "NAME": "test_db_Iryna",
#         #     "USER": "test_user",
#         #     "PASSWORD": "test",
#         #     "HOST": "localhost",
#         #     "PORT": 5432,
#         # },
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.environ.get("POSTGRES_DB"),
#             "USER": os.environ.get("POSTGRES_USER"),
#             "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#             "HOST": os.environ.get("POSTGRES_HOST"),
#             "PORT": os.environ.get("POSTGRES_PORT"),
#         },
#     }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA:F405
    }
}

STATIC_ROOT = BASE_DIR / "static/"  # NOQA:F405
STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media/"  # NOQA:F405
MEDIA_URL = "media/"
