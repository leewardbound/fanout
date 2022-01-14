from django.contrib.admin import ModelAdmin

from fanout.apps.common import admin

from . import models


@admin.register(models.User)
class UserAdmin(ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]


@admin.register(models.AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ["created_at", "type", "performing_user", "succeeded", "target", "extra_data"]
