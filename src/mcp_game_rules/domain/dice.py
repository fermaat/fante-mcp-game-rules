from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class PlotDieFace(StrEnum):
    OPPORTUNITY = "opportunity"
    COMPLICATION = "complication"
    BLANK = "blank"


class DicePolicy(BaseModel):
    d20s: int = Field(1, ge=1, le=10)
    keep: Literal["highest", "lowest", "all"] = "highest"
    plot_dice: int = Field(0, ge=0, le=10)

    @property
    def is_advantage(self) -> bool:
        return self.d20s > 1 and self.keep == "highest"

    @property
    def is_disadvantage(self) -> bool:
        return self.d20s > 1 and self.keep == "lowest"
