from collections.abc import Iterable

from app.catalog import COURSE_CATALOG, Course
from app.schemas import BlockedCourse, TermPlan


class CoursePlannerError(ValueError):
    pass


def normalize_code(code: str) -> str:
    return code.strip().upper()


def normalize_completed(codes: Iterable[str]) -> set[str]:
    completed = {normalize_code(code) for code in codes if code.strip()}
    unknown = sorted(code for code in completed if code not in COURSE_CATALOG)
    if unknown:
        raise CoursePlannerError(f"Unknown course code(s): {', '.join(unknown)}")
    return completed


def list_courses() -> list[Course]:
    return [COURSE_CATALOG[code] for code in sorted(COURSE_CATALOG)]


def get_course(code: str) -> Course:
    normalized = normalize_code(code)
    try:
        return COURSE_CATALOG[normalized]
    except KeyError as exc:
        raise CoursePlannerError(f"Unknown course code: {normalized}") from exc


def available_courses(completed: set[str]) -> list[Course]:
    return [
        course
        for course in list_courses()
        if course.code not in completed
        and all(prerequisite in completed for prerequisite in course.prerequisites)
    ]


def blocked_courses(completed: set[str]) -> list[BlockedCourse]:
    blocked: list[BlockedCourse] = []
    for course in list_courses():
        if course.code in completed:
            continue
        missing = [prerequisite for prerequisite in course.prerequisites if prerequisite not in completed]
        if missing:
            blocked.append(
                BlockedCourse(
                    code=course.code,
                    title=course.title,
                    missing_prerequisites=missing,
                )
            )
    return blocked


def target_path(target: str | None, completed: set[str]) -> list[str]:
    if target is None:
        return []

    normalized_target = normalize_code(target)
    if normalized_target not in COURSE_CATALOG:
        raise CoursePlannerError(f"Unknown course code: {normalized_target}")

    path: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(code: str) -> None:
        if code in completed or code in visited:
            return
        if code in visiting:
            raise CoursePlannerError(f"Cycle detected at course: {code}")

        visiting.add(code)
        course = COURSE_CATALOG[code]
        for prerequisite in sorted(course.prerequisites):
            visit(prerequisite)
        visiting.remove(code)
        visited.add(code)
        path.append(code)

    visit(normalized_target)
    return path


def build_term_plan(
    completed: set[str],
    target: str | None,
    max_courses_per_term: int,
) -> list[TermPlan]:
    pending = set(target_path(target, completed)) if target else set(COURSE_CATALOG) - completed
    completed_so_far = set(completed)
    plan: list[TermPlan] = []
    term_number = 1

    while pending:
        ready = sorted(
            code
            for code in pending
            if all(prerequisite in completed_so_far for prerequisite in COURSE_CATALOG[code].prerequisites)
        )
        if not ready:
            raise CoursePlannerError("No valid course plan could be generated")

        selected = ready[:max_courses_per_term]
        plan.append(TermPlan(term=term_number, courses=selected))
        completed_so_far.update(selected)
        pending.difference_update(selected)
        term_number += 1

    return plan
