import logging
import uuid

from django.db import models

log = logging.getLogger("fanout")


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at", "-created_at")


class AuditableMixin(UUIDMixin):
    def create_audit_log(self, type, message=None, performing_user=None, extra_data=None, succeeded=True):
        from fanout.apps.users.models import AuditLog

        log.info("AUDIT LOG: %s %s %s", type, message or "", extra_data or "")
        return AuditLog.objects.create(
            type=type,
            message=message,
            performing_user=performing_user,
            target=self,
            extra_data=extra_data,
            succeeded=succeeded,
        )

    class Meta:
        abstract = True


def from_choices(c, max_length=None):
    return {"choices": c.choices, "max_length": max_length or max([len(x) for x in c]), "default": c.choices[0]}


def get_client_ip(META):
    x_forwarded_for = META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = META.get("REMOTE_ADDR")
    return ip


def uuid4_string():
    return str(uuid.uuid4())
