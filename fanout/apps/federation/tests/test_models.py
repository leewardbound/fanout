from fanout.apps.common.tests import local_fanout
from fanout.apps.federation import models
from fanout.apps.federation.factories import ActorFactory


def test_actor_factory(local_fanout):
    actor = ActorFactory(domain=local_fanout.domain)
    assert actor.domain.name == "localhost"
    assert "https://localhost/" in actor.id
    assert models.Actor.objects.count() == len(local_fanout.other_actors) + 2, "there should be N+1 actors"


def test_local_fanout_fixture(local_fanout):
    actor = local_fanout.other_actors[0]
    assert actor.domain.name == "localhost"
    assert "https://localhost/" in actor.id
    assert (
        models.Actor.objects.count() == len(local_fanout.other_actors) + 1
    ), "there should be N actors (plus 1 service account for the domain)"
