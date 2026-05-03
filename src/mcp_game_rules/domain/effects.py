from pydantic import BaseModel


class Effect(BaseModel):
    name: str
    magnitude: int = 1
    duration_turns: int | None = None
    source_rule_id: str | None = None
