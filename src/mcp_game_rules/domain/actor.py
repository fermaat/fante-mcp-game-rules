from pydantic import BaseModel, Field

from mcp_game_rules.domain.attributes import Attributes


class Actor(BaseModel):
    name: str
    attributes: Attributes = Field(default_factory=Attributes)
    skills: dict[str, int] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
