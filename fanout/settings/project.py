# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import environ

from fanout import constants
import os

env = environ.Env(
    DEBUG=(bool, False),
)  # set default values and casting
ENVIRONMENT = os.environ.get("APP_ENV", constants.Environments.DEVELOPMENT).lower()
BACKEND_PORT = int(os.environ.get("DEVELOP_BACKEND_PORT", 8000))
DEBUG = os.environ.get("DEBUG", "") == "true"
ROOT_URLCONF = "fanout.settings.urls"

GRAPHENE = {"SCHEMA": "fanout.apps.schema.application_schema"}  # Where your Graphene schema lives

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="psql://fanout:fanout@psql/fanout",
    ),
}

FEDERATION_HOSTNAME = os.environ.get("FEDERATION_HOSTNAME", "localhost").lower()

MANAGERS = ADMINS = [
    ("Lee Bailey", "l@lwb.co"),
]
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "noreply@" + FEDERATION_HOSTNAME)

AUTH_USER_MODEL = "users.User"

INSTALLED_APPS = [
    "django.contrib.auth",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_object_actions",
    "graphene_django",
    "storages",
    "rest_framework",
    "django_filters",
    "django_extensions",
    "timezone_field",
    "debug_toolbar",
    "anymail",
    "rest_framework.authtoken",
    "sorl.thumbnail",
    "fanout.apps.federation",
    "fanout.apps.users",
    "fanout.apps.content",
    "fanout.apps.customers",
]

SITE_ROOT = PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)
PROJECT_MODULE = SITE_ROOT.split("/")[-1]

SERVE_MEDIA = True
USE_TZ = True

# BELOW IS CONFUSING!
# MEDIA_{ROOT,URL} -> User generated content
MEDIA_ROOT = root("static", "uploads")
MEDIA_URL = "/dj-static/uploads/"

# STATIC_{ROOT,URL} -> Python-collected static content
STATIC_ROOT = root("static", "assets")
STATIC_URL = "/dj-static/assets/"

# Where to collect ^above^ from:
STATICFILES_DIRS = []

# Where the admin stuff lives
ADMIN_MEDIA_PREFIX = "/dj-static/assets/admin/"

# django-mediagenerator search directories
# files are defined in assets.py
GLOBAL_MEDIA_DIRS = []

TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

IS_TEST = False

SITE_ID = 1

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": ("%(levelname)s %(asctime)s |" "%(pathname)s:%(lineno)d (in %(funcName)s) |" " %(message)s ")
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "fanout": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

TEST_EXCLUDE = ("django",)
FIXTURE_DIRS = [
    root(PROJECT_ROOT, "fixtures"),
]

BASE_DIR = root(PROJECT_ROOT)

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

ACCOUNT_OPEN_SIGNUP = False

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
CORS_ALLOW_CREDENTIALS = True

SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

TEMPLATES = [
    {
        # See:
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See:
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [
            str(SITE_ROOT + "/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            # See:
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            # ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
            ],
        },
    },
]


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

if not DEBUG:
    BASE_URL = os.environ.get("BASE_URL", f"https://{FEDERATION_HOSTNAME}")
    EMAIL_BACKEND = "django_ses.SESBackend"

else:
    BASE_URL = f"http://{FEDERATION_HOSTNAME}:{BACKEND_PORT}"
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

APPEND_SLASH = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "OPTIONS": {
            "MAX_ENTRIES": 50_000,
        },
    }
}

if "REDIS_URL" in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ["REDIS_URL"],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }


class DebugToolbarInternalIPs:
    def __contains__(self, ip):
        # Allow access from any IP for DEBUG=True
        return DEBUG


INTERNAL_IPS = DebugToolbarInternalIPs()

DEBUG_TOOLBAR_CONFIG = {
    # Toolbar options
    # 'RESULTS_CACHE_SIZE': 3,
    # 'SHOW_COLLAPSED': True,
    # Panel options
    "SQL_WARNING_THRESHOLD": 100,  # milliseconds
}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME", "")
AWS_DEFAULT_ACL = "private"
AWS_S3_FILE_OVERWRITE = False

if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "fanout.apps.utils.s3storages.S3PrivateStorage"
    THUMBNAIL_STORAGE = "fanout.apps.utils.s3storages.S3PublicStorage"

if "REDIS_URL" in os.environ:
    redis_url = urlparse(os.environ["REDIS_URL"])

    THUMBNAIL_REDIS_DB = "16"
    THUMBNAIL_REDIS_PASSWORD = redis_url.password or ""
    THUMBNAIL_REDIS_HOST = redis_url.hostname
    THUMBNAIL_REDIS_PORT = redis_url.port or 6379

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
