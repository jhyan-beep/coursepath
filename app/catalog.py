from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    code: str
    title: str
    credits: int
    prerequisites: tuple[str, ...] = ()


COURSE_CATALOG: dict[str, Course] = {
    "ECS020": Course(
        code="ECS020",
        title="Discrete Mathematics for Computer Science",
        credits=4,
    ),
    "ECS032A": Course(
        code="ECS032A",
        title="Introduction to Programming",
        credits=4,
    ),
    "ECS036B": Course(
        code="ECS036B",
        title="Software Development and Object-Oriented Programming",
        credits=4,
        prerequisites=("ECS032A",),
    ),
    "ECS036C": Course(
        code="ECS036C",
        title="Data Structures, Algorithms, and Programming",
        credits=4,
        prerequisites=("ECS036B",),
    ),
    "ECS050": Course(
        code="ECS050",
        title="Computer Organization and Machine-Dependent Programming",
        credits=4,
        prerequisites=("ECS036C",),
    ),
    "ECS122A": Course(
        code="ECS122A",
        title="Algorithm Design and Analysis",
        credits=4,
        prerequisites=("ECS020", "ECS036C"),
    ),
    "ECS150": Course(
        code="ECS150",
        title="Operating Systems",
        credits=4,
        prerequisites=("ECS036C", "ECS050"),
    ),
    "ECS154A": Course(
        code="ECS154A",
        title="Computer Architecture",
        credits=4,
        prerequisites=("ECS050",),
    ),
    "ECS165A": Course(
        code="ECS165A",
        title="Database Systems",
        credits=4,
        prerequisites=("ECS036C",),
    ),
    "ECS170": Course(
        code="ECS170",
        title="Artificial Intelligence",
        credits=4,
        prerequisites=("ECS122A",),
    ),
}
