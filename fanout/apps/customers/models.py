from typing import Mapping

from django.db import models

from fanout.apps.common.auditlog import AuditLogType
from fanout.apps.utils.models import AuditableMixin, TimestampMixin


class Customer(AuditableMixin, TimestampMixin):
    email = models.EmailField(null=True, blank=True)
    user = models.OneToOneField("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="customer")

    @classmethod
    def collect_customer(cls, email, user=None, ip=None, datapoints: Mapping[str, str] = None):
        datapoints = datapoints or {}
        if user:
            try:
                existing_by_user = cls.objects.get(user=user)
                if email and existing_by_user.email != email:
                    existing_by_user.email = email
                    existing_by_user.save()
                existing_by_user.set_data(datapoints)
                existing_by_user.create_audit_log(
                    AuditLogType.CUSTOMER_UPDATED,
                    "Found customer by user session",
                    performing_user=user,
                    extra_data={"ip": ip, **datapoints},
                )
                return existing_by_user
            except cls.DoesNotExist:
                pass

        try:
            existing_by_email = cls.objects.filter(email=email, user=user).first()
            if not existing_by_email:
                raise cls.DoesNotExist

            if user:
                existing_by_email.user = user
                existing_by_email.save()

            existing_by_email.set_data(datapoints)
            existing_by_email.create_audit_log(
                AuditLogType.CUSTOMER_UPDATED,
                "Found customer by email address",
                performing_user=user,
                extra_data={"ip": ip, **datapoints},
            )
            return existing_by_email
        except cls.DoesNotExist:
            pass

        customer = Customer.objects.create(email=email, user=user)
        customer.set_data(datapoints)
        customer.create_audit_log(
            AuditLogType.CUSTOMER_CREATED, performing_user=user, extra_data={"ip": ip, **datapoints}
        )
        return customer

    def set_data(self, update: Mapping[str, str] = None, delete_missing=False):
        all_points = list(self.datapoints.all())
        updated = []
        if not update:
            return self.datapoints.delete()
        for datapoint in all_points:
            if datapoint.key not in update:
                if delete_missing:
                    datapoint.delete()
            else:
                datapoint.value = update[datapoint.key]
                datapoint.save()
                updated.append(datapoint.key)
        if update:
            for key in filter(lambda k: k not in updated, update.keys()):
                self.datapoints.create(key=key, value=update[key])

    def get_all_data(self):
        return {point.key: point.value for point in self.datapoints.all()}

    def subscribe_to_actor(self, actor_id):
        from fanout.apps.federation.models import Actor

        actor = Actor.objects.get(id=actor_id)
        sub, created = self.subscriptions.get_or_create(actor=actor)
        if created:
            audit_log_type = AuditLogType.SUBSCRIPTION_CREATED
        else:
            audit_log_type = AuditLogType.SUBSCRIPTION_UPDATED

        sub.create_audit_log(audit_log_type, performing_user=self.user, extra_data=self.get_all_data())

        return sub, created

    def __str__(self):
        return self.email or self.user


class FollowOptions(models.TextChoices):
    UNFOLLOW = "unfollow", "Unfollow"
    FOLLOW = "follow", "Follow"


class Subscription(AuditableMixin, TimestampMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscriptions")
    actor = models.ForeignKey("federation.Actor", on_delete=models.CASCADE, related_name="subscriptions")
    type = models.CharField(max_length=32, default=FollowOptions.FOLLOW, choices=FollowOptions.choices)

    class Meta:
        unique_together = ["customer", "actor"]

    def __str__(self):
        return f"{self.customer} {self.get_type_display()} {self.actor}"


class CustomerDataPoint(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="datapoints")
    key = models.CharField(max_length=256)
    value = models.TextField()
