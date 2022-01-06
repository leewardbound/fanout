from fanout.apps.common import admin
from . import models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    list_filter = []
    search_fields = ["name"]


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
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
