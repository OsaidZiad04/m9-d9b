"""Learner-written tests for queries/warmups.py.

You write at least 2 tests here. The autograder verifies each test
function contains at least one assertion and is not left as the
placeholder `pytest.fail("Not implemented")`.

A driver fixture (`driver`) is provided via conftest.py — it points at
the same Neo4j instance the autograder uses, with the drill fixtures
already loaded.
"""

from queries.warmups import q1_list_recipes, q2_filter_by_cuisine, q3_subclass_traversal


def test_q1_list_recipes_returns_all_five(driver):
    cypher = q1_list_recipes()

    with driver.session() as session:
        rows = [record["name"] for record in session.run(cypher)]

    assert len(rows) == 5
    assert all(isinstance(name, str) for name in rows)
    assert all(name.strip() for name in rows)


def test_q3_traversal_picks_up_subclasses(driver):
    direct_cypher, direct_params = q2_filter_by_cuisine("Chinese")
    traversal_cypher, traversal_params = q3_subclass_traversal("Chinese")

    with driver.session() as session:
        direct_rows = {
            record["name"]
            for record in session.run(direct_cypher, direct_params)
        }

        traversal_rows = {
            record["name"]
            for record in session.run(traversal_cypher, traversal_params)
        }

    assert direct_rows
    assert traversal_rows
    assert direct_rows.issubset(traversal_rows)
    assert len(traversal_rows) > len(direct_rows)