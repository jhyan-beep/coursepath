# CoursePath

CoursePath is a FastAPI backend for planning a path through course prerequisites. It models a course catalog as a directed graph, then uses graph traversal to show which courses are available now, which courses are still blocked, and which sequence of prerequisites leads to a target course.

## Features

- List a built-in course catalog
- Read individual course details
- Normalize course codes like `ecs122a` to `ECS122A`
- Show courses available from a completed-course list
- Show blocked courses with missing prerequisites
- Generate a target-course prerequisite path
- Build a simple term-by-term plan with a configurable course limit
- Pytest coverage for API and planner behavior
- GitHub Actions CI
- Dockerfile for local container runs

## Tech Stack

- FastAPI
- Pydantic
- Pytest
- Docker

## API Overview

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/courses` | List the course catalog |
| GET | `/courses/{course_code}` | Read one course |
| POST | `/plan` | Generate recommendations and a term plan |

Example plan request:

```bash
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{"completed":["ECS020","ECS032A"],"target":"ECS122A","max_courses_per_term":2}'
```

## Run Locally

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs:

```text
http://localhost:8000/docs
```

## Run with Docker

```bash
docker build -t coursepath .
docker run --rm -p 8000:8000 coursepath
```

## Run Tests

```bash
pytest
```

## Example Resume Bullet

Built CoursePath, a FastAPI course prerequisite planner that models a catalog as a directed graph, recommends available courses, explains blocked courses, generates prerequisite paths to target classes, and validates behavior with pytest and GitHub Actions CI.
