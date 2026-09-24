from dataclasses import asdict, dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class ApiErrorResponse(Generic[T]):
    """Represent a structured error response"""

    timestamp: str
    errors: T | None
    message: str
    trace: list[str] | None
    path: str | None
    status: int | None = None

    def to_dict(self) -> dict[str, object]:
        """Convert the error response to a dictionary excluding null fields"""
        response = asdict(self)

        return {
            key: value
            for key, value in response.items()
            if value is not None
        }