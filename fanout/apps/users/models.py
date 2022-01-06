from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from fanout.apps.utils.models import UUIDMixin, TimestampMixin


class User(TimestampMixin, UUIDMixin, AbstractUser):
    pass

class AuditLog(TimestampMixin, UUIDMixin):
    performing_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='audit_log')
    type = models.CharField(max_length=64, db_index=True)
    message = models.CharField(max_length=512, null=True, blank=True)

    succeeded = models.BooleanField(default=True)
    extra_data = models.JSONField(null=True, blank=True)

    target_id = models.UUIDField(null=True, blank=True)
    target_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="targeting_audit_logs",
    )
    target = GenericForeignKey("target_content_type", "target_id")

