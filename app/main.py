from fastapi import FastAPI, HTTPException, status

from app.catalog import Course
from app.planner import (
    CoursePlannerError,
    available_courses,
    blocked_courses,
    build_term_plan,
    get_course,
    list_courses,
    normalize_completed,
    target_path,
)
from app.schemas import CourseRead, PlanRequest, PlanResponse


app = FastAPI(
    title="CoursePath",
    description="A graph-based course prerequisite planner.",
    version="0.1.0",
)


def serialize_course(course: Course) -> CourseRead:
    return CourseRead(
        code=course.code,
        title=course.title,
        credits=course.credits,
        prerequisites=list(course.prerequisites),
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/courses", response_model=list[CourseRead])
def read_courses() -> list[CourseRead]:
    return [serialize_course(course) for course in list_courses()]


@app.get("/courses/{course_code}", response_model=CourseRead)
def read_course(course_code: str) -> CourseRead:
    try:
        return serialize_course(get_course(course_code))
    except CoursePlannerError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.post("/plan", response_model=PlanResponse)
def create_plan(plan_request: PlanRequest) -> PlanResponse:
    try:
        completed = normalize_completed(plan_request.completed)
        available = available_courses(completed)
        return PlanResponse(
            completed=sorted(completed),
            available_now=[serialize_course(course) for course in available],
            blocked=blocked_courses(completed),
            target_path=target_path(plan_request.target, completed),
            term_plan=build_term_plan(
                completed=completed,
                target=plan_request.target,
                max_courses_per_term=plan_request.max_courses_per_term,
            ),
        )
    except CoursePlannerError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
