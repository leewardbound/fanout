from django.contrib.admin import ModelAdmin, display
from django.utils.safestring import mark_safe

from fanout.utils.admin import register

from . import models


@register(models.Customer)
class CustomerAdmin(ModelAdmin):
    @display()
    def customer_data(self, obj):
        return mark_safe("<br />".join(f"<b>{k}</b>: {v}" for k, v in obj.get_all_data().items()))

    list_display = ["created_at", "email", "related_user", "customer_data"]


@register(models.Subscription)
class ActorAdmin(ModelAdmin):
    pass
