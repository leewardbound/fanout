from django.contrib.admin import ModelAdmin

from fanout.apps.common.admin import register

from . import models


@register(models.Domain)
class DomainAdmin(ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@register(models.Actor)
class ActorAdmin(ModelAdmin):
    list_display = [
        "id",
        "domain",
        "username",
        "type",
        "updated_at",
        "created_at",
        "summary_updated",
    ]
    search_fields = ["id", "domain__name", "username", "display_name"]
    list_filter = ["type"]
