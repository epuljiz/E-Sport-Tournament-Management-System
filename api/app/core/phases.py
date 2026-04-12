from datetime import datetime, timezone
from enum import Enum
from app.models.tournament import Tournament

class Phase(str, Enum):
    OPEN = "open"
    PRELIM_PASSED = "prelim_passed"
    CLOSED = "closed"

def get_tournament_phase(tournament: Tournament) -> Phase:
    """Odredi fazu turnira prema trenutnom vremenu (UTC)."""
    now = datetime.now(timezone.utc)
    prelim = tournament.prelim_deadline
    final = tournament.final_deadline

    # Dodajemo UTC ako nedostaje (SQLite kompatibilnost)
    if prelim.tzinfo is None:
        prelim = prelim.replace(tzinfo=timezone.utc)
    if final.tzinfo is None:
        final = final.replace(tzinfo=timezone.utc)

    if now < prelim:
        return Phase.OPEN
    if now < final:
        return Phase.PRELIM_PASSED
    return Phase.CLOSED
