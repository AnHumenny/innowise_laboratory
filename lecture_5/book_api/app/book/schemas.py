from typing import Optional
from pydantic import BaseModel, Field


class BookItemCreate(BaseModel):
    """Schema for creating a new book item.

    Attributes:
        title (str): Title of the book. Required. Minimum length is 1 character.
        author (str): Author of the book. Required. Minimum length is 1 character.
        year (Optional[int]): Publication year of the book. Optional.
                              Must be greater than or equal to 0 if provided.
    """

    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: Optional[int] = Field(None, ge=0)


class BookItemRead(BaseModel):
    """Schema for reading book items from the database.

    Attributes:
        id (int): Unique identifier of the book.
        title (str): Title of the book.
        author (str): Author of the book.
        year (Optional[int]): Publication year of the book. Optional.
    """

    id: int
    title: str
    author: str
    year: Optional[int]

    model_config = {
        "from_attributes": True
    }


class BookItemUpdate(BaseModel):
    """Schema for updating an existing book item.

    All fields are optional for partial updates.
    """

    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=0)


class MessageResponse(BaseModel):
    """
    Pydantic model for a standard API text response.

    Attributes:
        message (str): A textual message, typically indicating the result of an operation.
    """

    message: str
