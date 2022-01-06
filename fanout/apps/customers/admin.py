from fanout.apps.common import admin
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'get_all_data']


@admin.register(models.Subscription)
class ActorAdmin(admin.ModelAdmin):
    pass
