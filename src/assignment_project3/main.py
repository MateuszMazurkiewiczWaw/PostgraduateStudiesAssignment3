#!/usr/bin/env python3

"""
assignment-project3 – main.py
Full SQLAlchemy 2.x + Alembic + 1-to-many and many-to-many relationships demo
"""

from sqlalchemy import create_engine, update, delete, select
from sqlalchemy.orm import sessionmaker
from models import Base, Experiment, DataPoint, Subject, experiment_subject
from pathlib import Path
from random import randint, uniform
from datetime import datetime


def main():
    db_path = Path(__file__).parent / "assignment.db"
    engine = create_engine(f"sqlite:///{db_path.absolute()}", echo=True, future=True)
    Base.metadata.create_all(engine)
    print(engine.connect())

    # Session Factory with context manager
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    print("Utworzono Baze Danychz relacją: Experiment (1) → DataPoint (wiele)")
    print("Klucz obcy: data_point.experiment_id → experiment.id")
    print("Relationship: Experiment.data_points (lista DataPoint)")
    print("Back_populates: DataPoint.experiment (pojedynczy Experiment)")
    print()

    with SessionLocal.begin() as session:
        # Exercise 1 - Adding 2 rows to the newly created Experiments table
        print("1. Dodawanie 2 wierszy do tabeli Experiments - exp1 & exp2".ljust(50), end=" ")
        exp1 = Experiment(
            title="Test Experiment Alpha",
            type=randint(1, 10),
            finished=False,
        )
        exp2 = Experiment(
            title="Test Experiment Beta",
            type=randint(1, 10),
            finished=False,
        )
        session.add_all([exp1, exp2])
        print("OK - Dodano 2 eksperymenty")
        print()

        # Exercise 2 - Adding 10 rows to the newly created DataPoints table (5 of each experiment exp1 and exp2)
        print("2. Dodawanie 10 wierszy do tabeli DataPoints (po 5 do kazdego eksperymentu exp1 & exp2)".ljust(50),
              end=" ")
        data_points = []
        for i in range(5):
            data_points.append(
                DataPoint(
                    real_value=round(uniform(0, 100), 2),
                    target_value=round(uniform(0, 100), 2),
                    experiment=exp1,
                )
            )
            data_points.append(
                DataPoint(
                    real_value=round(uniform(0, 100), 2),
                    target_value=round(uniform(0, 100), 2),
                    experiment=exp2,
                )
            )
        session.add_all(data_points)
        print("OK - Dodano 10 wierszy punktow danych")
        print()

        # Exercise 3 - Fetching and presenting of all available records
        print("3. Pobieranie i wyswietlanie wszystkich dostepnych rekordow".ljust(50), end=" ")
        experiments = session.scalars(select(Experiment)).all()
        data_points_all = session.scalars(select(DataPoint)).all()
        print("OK - Wyswietlam rekordy\n")

        print("Eksperymenty:")
        for exp in experiments:
            print(f"   • ID: {exp.id} | {exp.title} | type: {exp.type} | finished: {exp.finished}")

        print("\nPunkty danych (z przynaleznoscia):")
        for dp in data_points_all:
            exp_title = dp.experiment.title if dp.experiment else "—"
            print(
                f"   • DP {dp.id}: real={dp.real_value:.2f}, target={dp.target_value:.2f} → {exp_title}"
            )
        print()

        # Exercise 4 - Bulk update of the Experiments table (setting the finished flag = True)
        print("4. Hurtowa aktualizacja tabeli Experiments (ustawienie flagi finished = True)".ljust(50), end=" ")
        session.execute(update(Experiment).values(finished=True))
        print("OK - Zaktualizowano wszystkie eksperymenty")
        print()

        # Exercise 5 - Many-to-Many Relationship Demo (Subject table ↔ Experiments table)
        print("5. Demo relacji wiele-do-wielu (Subject ↔ Experiments)".ljust(50), end=" ")
        subject_a = Subject(gdpr_accepted=True)
        subject_b = Subject(gdpr_accepted=False)
        subject_c = Subject(gdpr_accepted=True)

        # Arrogation
        exp1.subjects.extend([subject_a, subject_b])
        exp2.subjects.extend([subject_b, subject_c])

        session.add_all([subject_a, subject_b, subject_c])
        print("OK - Przypisano flagi gdpr_accepted\n")

        # Refresh objects (to keep relationships up to date)
        session.refresh(exp1)
        session.refresh(exp2)

        # Data presentation
        print("Subject → Experiment:")
        for s in session.scalars(select(Subject)).all():
            exp_titles = [e.title for e in s.experiments]
            print(f"   • Subject {s.id} (GDPR: {s.gdpr_accepted}) → {exp_titles or 'brak'}")

        print("\nExperiment → Subject:")
        for exp in experiments:
            subj_ids = [s.id for s in exp.subjects]
            print(f"   • {exp.title} → Subject: {subj_ids or 'brak'}")
        print()

        # Exercise 6 - Bulk deletion of all records (including the intermediate table)
        print("6. Usuwanie hurtowe wszystkich rekordow (w tym tabeli posredniej)".ljust(50), end=" ")
        session.execute(delete(experiment_subject))
        session.execute(delete(DataPoint))
        session.execute(delete(Subject))
        session.execute(delete(Experiment))
        print("OK - Usunieto wszystkie wiersze z tabel")
        print()

        print("Wszystkie operacje zakończone sukcesem!")
        print("Mozesz teraz uruchomic:")
        print("alembic current")
        print("alembic history")
        print("i zobaczyc dwie migracje oraz czysta baze danych.")

    # Alembic DB data migration - sample steps
    # 1. Delete an old DB - if it already exists after previous run
    # rm src/assignment_project3/assignment.db
    # 2. Temporarily remove the Subject class and experiment_subject table from models.py. Leave only Experiment and DataPoint + the 1-to-many relationship.
    # 3. Generate new migration
    # cd src/assignment_project3
    # alembic revision --autogenerate -m "Initial with Experiment and DataPoint"
    # alembic upgrade head
    # 4. Add back Subject class + experiment_subject table + M2M relationship in models.py script.
    # 5. Generate second migration
    # alembic revision --autogenerate -m "Add Subject and M2M relation"
    # alembic upgrade head
    # alembic current                -> it will provide the ID of the last migration
    # alembic history --verbose      -> it will all migrations history


if __name__ == "__main__":
    main()
