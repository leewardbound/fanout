import logging
import uuid

from django.db import models
from django.forms.models import model_to_dict

log = logging.getLogger("fanout")


def _generate_id():
    return "".join(str(uuid.uuid4()).split("-")[1:3])


def _generate_medium_id():
    return "".join(str(uuid.uuid4()).split("-")[1:4])


class ShortIdMixin(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=_generate_id, editable=False)

    class Meta:
        abstract = True


class MediumIDMixin(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=_generate_id, editable=False)

    class Meta:
        abstract = True


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


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


def from_choices(c, max_length=None):
    return {"choices": c.choices, "max_length": max_length or max([len(x) for x in c]), "default": c.choices[0]}


def format_cents(c):
    return "${:0.2f}".format(c / 100)


def get_client_ip(META):
    x_forwarded_for = META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = META.get("REMOTE_ADDR")
    return ip


def uuid4_string():
    return str(uuid.uuid4())


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
