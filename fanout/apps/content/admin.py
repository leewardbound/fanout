from django.contrib.admin import ModelAdmin

from fanout.utils.admin import register

from . import models


@register(models.Note)
class NoteAdmin(ModelAdmin):
    list_display = ["created_at", "actor", "content"]
