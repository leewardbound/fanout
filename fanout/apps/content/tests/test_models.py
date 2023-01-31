def q_author_activities(actorId):
    return (
        """
    query {
        activities(actorId: "%s") {
          id, objectType, verb
        }
    }
    """
        % actorId
    )


def test_create_note(project_fixture_common):
    author = project_fixture_common.other_actors[0]
    response = project_fixture_common.query(q_author_activities(author.id))
    assert len(response["data"]["activities"]) == 0

    response = project_fixture_common.mutation(
        """mutation createNote($input: CreateNoteInput!) {
        createNote(input: $input) {
            activity { objectType id verb }
        }
    }""",
        {"input": {"actorId": author.id, "content": author.summary}},
    )
    print(response)

    assert response["data"]["createNote"]["activity"]["verb"] == "CREATE"
    assert response["data"]["createNote"]["activity"]["objectType"] == "note"

    response = project_fixture_common.query(q_author_activities(author.id))
    assert len(response["data"]["activities"]) == 1
