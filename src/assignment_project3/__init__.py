# src/assignment_project3/__init__.py
"""
assignment-project3 – demonstartion package of Full SQLAlchemy 2.x + Alembic + 1-to-many and many-to-many relationships demo

Includes:
- ORM models: Experiment, DataPoint, Subject
- 1-to-many and many-to-many relationships
- full CRUD in main.py
- Alembic migrations (2 migrations)
"""

from .models import Base, Experiment, DataPoint, Subject, experiment_subject

__all__ = [
    "Base",
    "Experiment",
    "DataPoint",
    "Subject",
    "experiment_subject",
]

__version__ = "1.0.0"


def get_engine(echo: bool = False):
    """Pomocnicza funkcja do tworzenia silnika bazy danych"""
    from sqlalchemy import create_engine
    from pathlib import Path
    db_path = Path(__file__).parent / "assignment.db"
    return create_engine(f"sqlite:///{db_path}", echo=echo, future=True)
