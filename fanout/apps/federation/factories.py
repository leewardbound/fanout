import factory
from django.conf import settings
from django.utils import timezone

from fanout.apps.federation import models
from fanout.apps.federation.models import ActorTypes, activitypub_id_generator
from fanout.constants import URLPrefixes
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
    id = factory.LazyAttribute(lambda o: activitypub_id_generator(URLPrefixes.ACTORS, domain=o.domain)(o.username))
    followers_url = factory.LazyAttribute(lambda o: "{}/followers".format(o.id))
    inbox_url = factory.LazyAttribute(lambda o: "{}/inbox.json".format(o.id))
    outbox_url = factory.LazyAttribute(lambda o: "{}/outbox.json".format(o.id))

    class Meta:
        model = models.Actor

    @factory.post_generation
    def local(self, create, extracted, **kwargs):
        if not extracted and not kwargs:
            return

        self.domain = models.Domain.objects.get_or_create(name=settings.FEDERATION_HOSTNAME)[0]
        self.id = activitypub_id_generator(URLPrefixes.ACTORS, domain=self.domain)(self.username)
        self.save(update_fields=["domain", "id"])
