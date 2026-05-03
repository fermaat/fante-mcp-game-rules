from enum import StrEnum

from pydantic import BaseModel, Field


class Attribute(StrEnum):
    STRENGTH = "strength"
    SPEED = "speed"
    INTELLECT = "intellect"
    WILLPOWER = "willpower"
    AWARENESS = "awareness"
    PRESENCE = "presence"


class Attributes(BaseModel):
    strength: int = Field(0, ge=0, le=8)
    speed: int = Field(0, ge=0, le=8)
    intellect: int = Field(0, ge=0, le=8)
    willpower: int = Field(0, ge=0, le=8)
    awareness: int = Field(0, ge=0, le=8)
    presence: int = Field(0, ge=0, le=8)

    def get(self, attr: Attribute) -> int:
        return int(getattr(self, attr.value))
