from fanout.apps.common import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    list_filter = []
    search_fields = ["username", "email"]


@admin.register(models.AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["created_at", "type", "performing_user", "succeeded", "target", "extra_data"]
