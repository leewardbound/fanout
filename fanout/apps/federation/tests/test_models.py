from fanout.apps.federation import models
from fanout.apps.federation.factories import ActorFactory


def test_actor_factory(project_fixture_common):
    actor = ActorFactory(domain=project_fixture_common.domain)
    assert actor.domain.name == "localhost"
    assert "https://localhost/" in actor.id
    assert models.Actor.objects.count() == len(project_fixture_common.other_actors) + 2, "there should be N+2 actors"


def test_local_fanout_fixture(project_fixture_common):
    actor = project_fixture_common.other_actors[0]
    assert actor.domain.name == "localhost"
    assert "https://localhost/" in actor.id
    assert (
        models.Actor.objects.count() == len(project_fixture_common.other_actors) + 1
    ), "there should be N actors (plus 1 service account for the domain)"
