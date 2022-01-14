import json

import pytest
from graphene_django.utils.testing import graphql_query


def q_author_activities(actorId):
    return (
        """
    query {
        activities(actorId: "%s") {
          id, type
        }
    }
    """
        % actorId
    )


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        response = graphql_query(*args, **kwargs, client=client)
        setattr(response, "json", lambda: json.loads(response.content))
        return response

    return func


def test_create_note(local_fanout, client_query):
    author = local_fanout.other_actors[0]
    response = client_query(q_author_activities(author.id)).json()
    assert len(response["data"]["activities"]) == 0

    response = client_query(
        """mutation createNote($input: CreateNoteInput!) {
        createNote(input: $input) {
            activity { type id }
        }
    }""",
        input_data={"actorId": author.id, "content": author.summary},
    ).json()

    assert response["data"]["createNote"]["activity"]["type"] == "CREATE"

    response = client_query(q_author_activities(author.id)).json()
    assert len(response["data"]["activities"]) == 1
