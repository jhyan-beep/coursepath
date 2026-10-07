from pydantic import BaseModel, Field


class CourseRead(BaseModel):
    code: str
    title: str
    credits: int
    prerequisites: list[str] = Field(default_factory=list)


class BlockedCourse(BaseModel):
    code: str
    title: str
    missing_prerequisites: list[str]


class TermPlan(BaseModel):
    term: int
    courses: list[str]


class PlanRequest(BaseModel):
    completed: list[str] = Field(default_factory=list)
    target: str | None = None
    max_courses_per_term: int = Field(default=3, ge=1, le=6)


class PlanResponse(BaseModel):
    completed: list[str]
    available_now: list[CourseRead]
    blocked: list[BlockedCourse]
    target_path: list[str]
    term_plan: list[TermPlan]
