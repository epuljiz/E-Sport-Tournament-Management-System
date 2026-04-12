from pydantic import BaseModel, Field
from datetime import date

class PlayerBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    nickname: str = Field(min_length=1, max_length=50)
    position: str = Field(min_length=1, max_length=50)
    birth_date: date
    nationality: str | None = Field(None, max_length=50)

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=80)
    last_name: str | None = Field(None, min_length=1, max_length=80)
    nickname: str | None = Field(None, min_length=1, max_length=50)
    position: str | None = Field(None, min_length=1, max_length=50)
    birth_date: date | None = None
    nationality: str | None = Field(None, max_length=50)

class PlayerResponse(PlayerBase):
    id: int
    team_id: int

    model_config = {"from_attributes": True}
