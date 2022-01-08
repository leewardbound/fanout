import factory


class PasswordSetter(factory.PostGenerationMethodCall):
    def call(self, instance, step, context):
        if context.value_provided and context.value is None:
            # disable setting the password, it's set by hand outside of the factory
            return

        return super().call(instance, step, context)


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = PasswordSetter("set_password", "test")

    class Meta:
        model = "users.User"
        django_get_or_create = ("username",)

    @factory.post_generation
    def with_actor(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        from fanout.apps.users.models import create_actor

        self.actor = create_actor(self)
        self.save(update_fields=["actor"])
        return self.actor


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True
