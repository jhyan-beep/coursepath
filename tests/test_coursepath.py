from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_courses_returns_catalog_in_code_order() -> None:
    response = client.get("/courses")

    assert response.status_code == 200
    data = response.json()
    assert [course["code"] for course in data] == sorted(course["code"] for course in data)
    assert {"code": "ECS032A", "title": "Introduction to Programming", "credits": 4, "prerequisites": []} in data


def test_get_course_normalizes_course_code() -> None:
    response = client.get("/courses/ecs122a")

    assert response.status_code == 200
    assert response.json()["prerequisites"] == ["ECS020", "ECS036C"]


def test_get_course_returns_404_for_unknown_course() -> None:
    response = client.get("/courses/ecs999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Unknown course code: ECS999"


def test_plan_recommends_available_courses_from_completed_work() -> None:
    response = client.post(
        "/plan",
        json={"completed": ["ecs032a", "ecs020"], "max_courses_per_term": 2},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == ["ECS020", "ECS032A"]
    assert [course["code"] for course in data["available_now"]] == ["ECS036B"]
    assert {"code": "ECS122A", "title": "Algorithm Design and Analysis", "missing_prerequisites": ["ECS036C"]} in data[
        "blocked"
    ]


def test_plan_builds_target_path_and_term_plan() -> None:
    response = client.post(
        "/plan",
        json={"target": "ECS122A", "max_courses_per_term": 2},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["target_path"] == ["ECS020", "ECS032A", "ECS036B", "ECS036C", "ECS122A"]
    assert data["term_plan"] == [
        {"term": 1, "courses": ["ECS020", "ECS032A"]},
        {"term": 2, "courses": ["ECS036B"]},
        {"term": 3, "courses": ["ECS036C"]},
        {"term": 4, "courses": ["ECS122A"]},
    ]


def test_plan_skips_completed_courses_in_target_path() -> None:
    response = client.post(
        "/plan",
        json={"completed": ["ECS020", "ECS032A", "ECS036B"], "target": "ECS122A"},
    )

    assert response.status_code == 200
    assert response.json()["target_path"] == ["ECS036C", "ECS122A"]


def test_plan_returns_400_for_unknown_completed_course() -> None:
    response = client.post("/plan", json={"completed": ["ECS999"]})

    assert response.status_code == 400
    assert response.json()["detail"] == "Unknown course code(s): ECS999"
