from dataclasses import asdict, dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class ApiResponseSuccess(Generic[T]):
    """Represent a successful response"""

    timestamp: str
    status: int | None
    data: T | None
    message: str
    trace: list[str] | None
    path: str | None

    def to_dict(self) -> dict[str, object]:
        """Convert the response to a dictionary excluding null fields"""
        response = asdict(self)

        return {
            key: value
            for key, value in response.items()
            if value is not None
        }