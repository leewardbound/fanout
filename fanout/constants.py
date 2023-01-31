from django.db import models


class Environments:
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"  # local development environment


class URLPrefixes:
    ACTORS = "p"
    ACTIVITIES = "a"
    OBJECTS = "o"
