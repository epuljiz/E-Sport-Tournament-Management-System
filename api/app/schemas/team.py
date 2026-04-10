from pydantic import BaseModel, Field
from datetime import datetime

class TeamBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    organization_name: str | None = None

class TeamCreate(TeamBase):
    password: str = Field(min_length=6)

class TeamUpdate(BaseModel):
    name: str | None = None
    organization_name: str | None = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    admin_username: str | None = None

    model_config = {"from_attributes": True}
