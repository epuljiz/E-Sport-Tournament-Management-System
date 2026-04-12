from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.core.phases import Phase, get_tournament_phase
from app.models.registration import TournamentRegistration
from app.models.user import User
from app.repositories import tournament_repo, team_repo, registration_repo

async def register_team(db: AsyncSession, tournament_id: int, current_user: User) -> TournamentRegistration:
    """Prijava tima na turnir uz provjeru poslovnih pravila."""
    tournament = await tournament_repo.get_by_id(db, tournament_id)
    if not tournament:
        raise AppError("not_found", "Turnir nije pronađen", 404)

    # 1. Provjera faze
    phase = get_tournament_phase(tournament)
    if phase != Phase.OPEN:
        raise AppError("deadline_passed", "Prijave su zatvorene (rok je prošao)", 400)

    # 2. Provjera prava (team_admin smije prijaviti samo svoj tim)
    if current_user.role != "admin" and not current_user.team_id:
         raise AppError("forbidden", "Korisnik nema pridružen tim", 403)
    
    team_id = current_user.team_id # U stvarnosti admin bi mogao birati tim, ovdje pojednostavljujem

    # 3. Poslovno pravilo: Tim mora imati barem 5 igrača
    from sqlalchemy import func, select
    from app.models.player import Player
    
    count_stmt = select(func.count(Player.id)).where(Player.team_id == team_id)
    player_count = (await db.execute(count_stmt)).scalar_one()

    if player_count < 5:
        raise AppError("invalid_team", f"Tim mora imati barem 5 igrača za prijavu (trenutno: {player_count})", 400)

    # 4. Kreiranje prijave
    reg = TournamentRegistration(team_id=team_id, tournament_id=tournament_id)
    try:
        await registration_repo.create(db, reg)
        await db.refresh(reg, ["team"])
    except IntegrityError:
        raise AppError("duplicate", "Tim je već prijavljen na ovaj turnir", 409)
    
    return reg

async def list_registrations(db: AsyncSession, tournament_id: int) -> list[TournamentRegistration]:
    """Lista svih prijava za turnir."""
    return await registration_repo.get_by_tournament(db, tournament_id)

async def withdraw_registration(db: AsyncSession, tournament_id: int, reg_id: int, current_user: User) -> None:
    """Povlačenje prijave (odjava) s turnira."""
    reg = await registration_repo.get_by_id(db, reg_id)
    if not reg or reg.tournament_id != tournament_id:
        raise AppError("not_found", "Prijava nije pronađena", 404)

    # Provjera faze (ne može se odjaviti ako je CLOSED)
    tournament = reg.tournament
    phase = get_tournament_phase(tournament)
    if phase == Phase.CLOSED:
        raise AppError("deadline_passed", "Odjava više nije moguća jer je turnir zaključan", 400)

    # Provjera autorizacije
    if current_user.role == "team_admin" and reg.team_id != current_user.team_id:
        raise AppError("forbidden", "Ne možete odjaviti tuđi tim", 403)

    reg.status = "withdrawn"
    await db.flush()
