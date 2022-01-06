from django.db import models


class AuditLogType(models.TextChoices):
    SUBSCRIPTION_CREATED = 'subscription.created', "Subscription Created"
    SUBSCRIPTION_UPDATED = 'subscription.updated', "Subscription Updated"
    CUSTOMER_CREATED = 'customer.created', "Customer Created"
    CUSTOMER_UPDATED = 'customer.updated', "Customer Updated"
