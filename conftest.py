from dataclasses import dataclass
from typing import List

import django.conf
import pytest

from fanout.apps.federation.models import Actor, Domain
from fanout.apps.users.factories import UserFactory
from fanout.apps.users.models import User


@pytest.fixture
def strong_pass():
    # Test password is very strong
    return "Fan0ut!!"


@pytest.fixture
def create_test_user(db, strong_pass):
    return UserFactory(password=strong_pass)


@pytest.fixture
def logged_in_client(client, create_test_user, strong_pass):
    test_user = create_test_user
    if test_user is not None:
        client.login(username=test_user.username, password=strong_pass)
        return client, test_user


@dataclass
class FanoutFixture:
    domain: Domain
    other_actors: List[Actor]
    settings: django.conf.Settings
    client: django.test.client.Client
    user: User


@pytest.fixture
def local_fanout(db, settings, logged_in_client):
    from fanout.apps.federation import factories, models

    settings.FEDERATION_HOSTNAME = "localhost"
    domain = models.Domain.LOCAL()
    actors = [factories.ActorFactory(domain=domain) for _ in range(5)]
    client, test_user = logged_in_client
    return FanoutFixture(domain=domain, other_actors=actors, settings=settings, client=client, user=test_user)
