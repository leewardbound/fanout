import logging
import os
import sys

if "TEST_USE_ENV" not in os.environ:
    # Let's reset ENV variables values for testing
    os.environ["AWS_ACCESS_KEY_ID"] = ""
    os.environ["AWS_SECRET_ACCESS_KEY"] = ""
    os.environ["AWS_S3_BUCKET_NAME"] = ""

    del sys.modules["fanout.settings"]
    del sys.modules["fanout.settings.base"]
    del sys.modules["fanout.settings.defaults"]

from fanout.settings import *

SECRET_KEY = "Test Only Key"

IS_TEST = True

print("TEST MODE DEFAULTS, disabling unneeded plugins")

logging.disable(logging.CRITICAL)
DEBUG = True
print("TEST MODE: DEBUG=%s" % DEBUG)

# Once we reach a certain degree of complexity, this needs to be removed
print("TEST MODE: Using sqlite DB")
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ".sqlite-test-db",
}
print("TEST MODE: Use fast MD5PasswordHasher")
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

EMAIL_BACKEND = "fanout.conf.test_settings.MockEmailBackend"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
FULFILLMENT_SHIPPING_LIMIT = 1000  # Some tests run with 300 quantity, they expect valid shipping results
