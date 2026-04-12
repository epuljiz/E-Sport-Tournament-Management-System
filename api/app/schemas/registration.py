from pydantic import BaseModel
from datetime import datetime

class RegistrationResponse(BaseModel):
    id: int
    tournament_id: int
    team_id: int
    status: str
    registered_at: datetime
    
    # Ovdje možemo dodati ime tima za listanje
    team_name: str | None = None

    @classmethod
    def from_orm_extra(cls, obj):
        res = cls.model_validate(obj)
        res.team_name = obj.team.name if obj.team else None
        return res

    model_config = {"from_attributes": True}
