#!/usr/bin/env python3
"""
SQLAlchemy models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


experiment_subject = Table(  # TABELA POŚREDNIA DLA M-M!
    "experiment_subject",
    Base.metadata,
    Column("experiment_id", Integer, ForeignKey("experiment.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subject.id"), primary_key=True)
)


class Experiment(Base):
    __tablename__ = "experiment"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    type = Column(Integer, nullable=False)
    finished = Column(Boolean, default=False)

    data_points = relationship("DataPoint", back_populates="experiment",
                               cascade="all, delete-orphan")  # Relacja 1-M! jeden eksperyment ma wiele DataPoint
    subjects = relationship("Subject", secondary=experiment_subject,
                            back_populates="experiments")  # Relacja M-M! Relacja wiele-do-wielu z Subject

    def __repr__(self) -> str:
        return f"<Experiment {self.id}: {self.title} (finished={self.finished})>"


class DataPoint(Base):
    __tablename__ = "data_point"

    id = Column(Integer, primary_key=True)
    real_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)

    experiment = relationship("Experiment", back_populates="data_points")  ## Relacja 1-1!

    def __repr__(self) -> str:
        return f"<DataPoint {self.id}: {self.real_value} → {self.target_value}>"


class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    gdpr_accepted = Column(Boolean, default=False, nullable=False)

    experiments = relationship("Experiment", secondary=experiment_subject, back_populates="subjects")  # Relacja M-M!

    def __repr__(self) -> str:
        return f"<Subject {self.id}: GDPR={self.gdpr_accepted}>"
