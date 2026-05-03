from typing import Any, Literal

from pydantic import BaseModel

Op = Literal["eq", "neq", "gt", "gte", "lt", "lte", "in", "not_in", "contains"]


class Condition(BaseModel):
    field: str
    op: Op
    value: Any
