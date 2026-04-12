from pydantic import BaseModel, Field
from datetime import date, datetime

class TournamentBase(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    game: str = Field(min_length=2, max_length=100)
    start_date: date
    location: str = Field(min_length=2, max_length=200)

class TournamentCreate(TournamentBase):
    prelim_deadline: datetime
    final_deadline: datetime

class TournamentResponse(TournamentBase):
    id: int
    prelim_deadline: datetime
    final_deadline: datetime

    model_config = {"from_attributes": True}
