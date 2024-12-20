from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel


# Define a type variable to allow generic responses
T = TypeVar("T")


class StandardResponse(GenericModel, Generic[T]):
    data: Optional[T]  # Optional to handle cases where there's no data
    message: str
    status_code: int