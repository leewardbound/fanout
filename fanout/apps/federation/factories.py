import factory
from django.conf import settings
from django.utils import timezone

from fanout.apps.federation import models
from fanout.apps.federation.models import ActorTypes
from fanout.factories import NoUpdateOnCreate


class DomainFactory(NoUpdateOnCreate, factory.django.DjangoModelFactory):
    name = factory.Faker("domain_name")
    info_updated = factory.LazyFunction(lambda: timezone.now())

    class Meta:
        model = "federation.Domain"
        django_get_or_create = ("name",)

    @factory.post_generation
    def with_service_actor(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.service_actor = ActorFactory(domain=self)
        self.save(update_fields=["service_actor"])
        return self.service_actor


class ActorFactory(NoUpdateOnCreate, factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    summary = factory.Faker("paragraph")
    domain = factory.SubFactory(DomainFactory)
    type = factory.Iterator(ActorTypes)
    id = factory.LazyAttribute(
        lambda o: "https://{}/users/{}".format(o.domain.name, o.username)
    )
    followers_url = factory.LazyAttribute(
        lambda o: "https://{}/users/{}followers".format(
            o.domain.name, o.username
        )
    )
    inbox_url = factory.LazyAttribute(
        lambda o: "https://{}/users/{}/inbox".format(
            o.domain.name, o.username
        )
    )
    outbox_url = factory.LazyAttribute(
        lambda o: "https://{}/users/{}/outbox".format(
            o.domain.name, o.username
        )
    )

    class Meta:
        model = models.Actor

    @factory.post_generation
    def local(self, create, extracted, **kwargs):
        if not extracted and not kwargs:
            return

        self.domain = models.Domain.objects.get_or_create(
            name=settings.FEDERATION_HOSTNAME
        )[0]
        self.id = "https://{}/actors/{}".format(self.domain, self.username)
        self.save(update_fields=["domain", "id"])