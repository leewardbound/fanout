from dataclasses import dataclass

from django.db import models
from django.utils.module_loading import import_string

from fanout.apps.utils.models import TimestampMixin, from_choices


class SettingsHandlers(models.TextChoices):
    SYSTEM = 'fanout.apps.common.settings.SystemSettingsHandler', 'System Settings'

class Settings(TimestampMixin):
    id = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField()
    handler = models.CharField(**from_choices(SettingsHandlers))

    @property
    def settings(self):
        handler = import_string(self.handler)
        return handler(**self.data)

    @classmethod
    def initialize(cls, id, handler):
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            return cls.objects.create(id=id, handler=handler)

    @classmethod
    def SYSTEM(cls):
        return cls.initialize('SYSTEM', SettingsHandlers.SYSTEM)

@dataclass
class SystemSettingsHandler:
    primary_hostname: str