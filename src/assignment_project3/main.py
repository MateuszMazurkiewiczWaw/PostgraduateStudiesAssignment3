#!/usr/bin/env python3

"""
assignment-project3 – main.py
Full SQLAlchemy 2.x + Alembic + 1-to-many and many-to-many relationships demo
"""

from sqlalchemy import create_engine, update, delete, select
from sqlalchemy.orm import sessionmaker
from models import Base, Experiment, DataPoint, Subject
from pathlib import Path
from random import randint, uniform
from datetime import datetime


def main():
    # db_path = Path("assignment.db")
    db_path = Path(__file__).parent / "assignment.db"
    engine = create_engine(f"sqlite:///{db_path.absolute()}", echo=True, future=True)
    Base.metadata.create_all(engine)
    print(engine.connect())
    Session = sessionmaker(bind=engine, future=True)
    session = Session()

    print("Baza utworzona z relacją: Experiment (1) → DataPoint (wiele)")
    print("Klucz obcy: data_point.experiment_id → experiment.id")
    print("Relationship: Experiment.data_points (lista DataPoint)")
    print("Back_populates: DataPoint.experiment (pojedynczy Experiment)")
    print()

    # 1. Dodaj 2 wiersze do Experiments

    # print("1: Dodawanie 2 wierszy do Experiments")
    # exp1 = Experiment(title="Test Experiment 1", type=randint(1, 10), finished=False)
    # exp2 = Experiment(title="Test Experiment 2", type=randint(1, 10), finished=False)
    # session.add_all([exp1, exp2])
    # session.commit()
    # print("Dodano 2 eksperymenty")
    # print()

    print("1. Dodawanie 2 wierszy do tabeli Experiments".ljust(50), "→", end=" ")
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
    session.commit()
    print("OK - Dodano 2 eksperymenty")
    # print(f"   → {exp1.title} (id={exp1.id}), {exp2.title} (id={exp2.id})")
    print()

    # 2. Dodaj 10 wierszy do DataPoints
    # print("2: Dodawanie 10 wierszy do DataPoints")
    # data_points = [
    #     DataPoint(real_value=uniform(0, 100), target_value=uniform(0, 100))
    #     for _ in range(10)
    # ]
    # session.add_all(data_points)
    # session.commit()
    # print("Dodano 10 punktów danych")
    # print()

    print("2. Dodawanie 10 wierszy do DataPoints (po 5 do każdego eksperymentu)".ljust(50), "→", end=" ")
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
    session.commit()
    print("OK - Dodano 10 punktów danych")
    print()

    # 3. Pobierz dodane dane i wyświetl
    # print("3: Pobieranie i wyświetlanie danych")
    # experiments = session.query(Experiment).all()
    # print("Eksperymenty:")
    # for exp in experiments:
    #     print(f"ID: {exp.id}, Title: {exp.title}, Type: {exp.type}, Finished: {exp.finished}")
    #
    # data_points_fetched = session.query(DataPoint).all()
    # print("\nPunkty danych:")
    # for dp in data_points_fetched:
    #     print(f"ID: {dp.id}, Real: {dp.real_value:.2f}, Target: {dp.target_value:.2f}")
    # print()

    print("3. Pobieranie i wyświetlanie wszystkich rekordów".ljust(50), "→", end=" ")
    experiments = session.scalars(select(Experiment)).all()
    data_points_all = session.scalars(select(DataPoint)).all()
    print("OK - Wyswietlam rekordy\n")

    print("Eksperymenty:")
    for exp in experiments:
        print(f"   • ID: {exp.id} | {exp.title} | type: {exp.type} | finished: {exp.finished}")

    print("\nPunkty danych (z przynależnością):")
    for dp in data_points_all:
        exp_title = dp.experiment.title if dp.experiment else "—"
        print(
            f"   • DP {dp.id}: real={dp.real_value:.2f}, target={dp.target_value:.2f} → {exp_title}"
        )
    print()

    # 4. Aktualizuj wszystkie Experiments (finished=True)
    # print("4: Aktualizacja hurtowa Experiments (finished=True)")
    # session.execute(update(Experiment).values(finished=True))
    # session.commit()
    # print("Zaktualizowano wszystkie eksperymenty")
    # print()
    #

    print("4. Hurtowa aktualizacja tabeli Experiments (finished = True)".ljust(50), "→", end=" ")
    session.execute(update(Experiment).values(finished=True))
    session.commit()
    print("OK - Zaktualizowano wszystkie eksperymenty")
    print()

    # ------------------------------------------------------------------ #
    # 5. DEMO RELACJI WIELE-DO-WIELU (Subject ↔ Experiment)
    # ------------------------------------------------------------------ #
    print("5. Demo relacji wiele-do-wielu (Subject ↔ Experiment)".ljust(50), "→", end=" ")
    subject_a = Subject(gdpr_accepted=True)
    subject_b = Subject(gdpr_accepted=False)
    subject_c = Subject(gdpr_accepted=True)

    # Przypisanie
    exp1.subjects.extend([subject_a, subject_b])
    exp2.subjects.extend([subject_b, subject_c])

    session.add_all([subject_a, subject_b, subject_c])
    session.commit()
    print("OK - Przypisano flagi gdpr_accepted\n")

    # Odśwież obiekty (żeby mieć aktualne relacje)
    session.refresh(exp1)
    session.refresh(exp2)

    print("Subject → Experiment:")
    for s in session.scalars(select(Subject)).all():
        exp_titles = [e.title for e in s.experiments]
        print(f"   • Subject {s.id} (GDPR: {s.gdpr_accepted}) → {exp_titles or 'brak'}")

    print("\nExperiment → Subject:")
    for exp in experiments:
        subj_ids = [s.id for s in exp.subjects]
        print(f"   • {exp.title} → Subject: {subj_ids or 'brak'}")
    print()

    # # 6. Usuń wszystkie wiersze z obu tabel
    # print(" 5: Usuwanie hurtowe wszystkich wierszy")
    # session.execute(delete(Experiment))
    # session.execute(delete(DataPoint))
    # session.commit()
    # print("Usunięto wszystkie wiersze z tabel")
    # print()

    print("6. Usuwanie hurtowe wszystkich rekordów".ljust(50), "→", end=" ")
    session.execute(delete(DataPoint))
    session.execute(delete(Subject))
    session.execute(delete(Experiment))
    session.commit()
    print("OK - Usunięto wszystkie wiersze z tabel")
    print()











    # ------------------------------------------------------------------ #
    # Koniec
    # ------------------------------------------------------------------ #
    print("Wszystkie operacje zakończone sukcesem!")
    print("Możesz teraz uruchomić:")
    print("  alembic current")
    print("  alembic history")
    print("i zobaczyć dwie migracje oraz czystą bazę.")

    session.close()

    #alembic revision --autogenerate -m "Initial migration with all tables"
    #alembic upgrade head
    #alembic revision --autogenerate -m "Add Subject and M2M relation"
    #alembic upgrade head
    #alembic current                - powinno pokazać ID ostatniej migracji
    #alembic history --verbose      - pokaże dwie migracje

if __name__ == "__main__":
    main()
