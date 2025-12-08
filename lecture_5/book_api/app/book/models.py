from typing import Optional
from sqlalchemy import CheckConstraint, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """The base class for all models.

    Attributes:
        id (int): Primary key, unique identifier for the record.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pass


class Book(Base):
    """SQLAlchemy model for storing book information.

    Represents a book record in the 'book_book' table.

    Attributes:
        title (str): Title of the book. Required.
        author (str): Author of the book. Required.
        year (Optional[int]): Publication year. Optional.
    """

    __tablename__ = "book__book"

    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('year >= 0 OR year IS NULL', name='year_non_negative_or_null'),
    )
