from django.contrib.admin import ModelAdmin

from fanout.apps.common import admin

from . import models


@admin.register(models.Note)
class NoteAdmin(ModelAdmin):
    list_display = ["created_at", "actor", "content"]
