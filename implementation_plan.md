# E-sports Tournament Management System - Implementation Plan

Ovaj plan detaljno opisuje razvoj web aplikacije za upravljanje e-sport turnirima, prateći točnu strukturu i metodologiju (6 predavanja).

## Pregled sustava
Aplikacija će omogućiti organizaciju e-sport turnira, registraciju profesionalnih igrača i timova, te praćenje faza natjecanja.

- **Stack**: FastAPI (Python), SQLAlchemy (ORM), PostgreSQL (Baza), Pydantic (Validacija).
- **Arhitektura**: Layered (Router -> Service -> Repository -> Model).

## Plan razvoja po koracima

### [KORAK 1] Infrastruktura i osnovni setup (Predavanje 1)
Postavljanje temelja aplikacije bez baze podataka.
- [ ] `esport/api/app/main.py`: App factory i sastavljanje aplikacije.
- [ ] `esport/api/app/core/config.py`: Pydantic settings za `.env`.
- [ ] `esport/api/app/core/logging.py`: Centralizirano logiranje.
- [ ] `esport/api/app/core/errors.py`: Globalni exception handler (`AppError`).
- [ ] `esport/api/app/routers/health.py`: Provjera rada API-ja.
- [ ] `esport/docker-compose.yml`: PostgreSQL kontejner.

### [KORAK 2] Baza podataka i osnovni modeli (Predavanje 2)
Povezivanje s bazom i definiranje organizacija i korisnika.
- [ ] `esport/api/app/core/database.py`: SQLAlchemy setup.
- [ ] `esport/api/app/models/user.py`: Korisnički računi (Admini).
- [ ] `esport/api/app/models/team.py`: E-sport organizacije (Timovi).
- [ ] `esport/api/app/seed.py`: Skripta za inicijalne podatke.

### [KORAK 3] Autentifikacija i Sigurnost (Predavanje 3)
Implementacija JWT sustava.
- [ ] `esport/api/app/core/security.py`: Hashiranje lozinki.
- [ ] `esport/api/app/core/jwt.py`: JWT logika.
- [ ] `esport/api/app/services/auth_service.py`: Prijava korisnika.
- [ ] `esport/api/app/routers/auth.py`: `/auth/login` endpoint.

### [KORAK 4] CRUD operacije za timove (Predavanje 4)
Implementacija punog ciklusa za upravljanje timovima.
- [ ] `esport/api/app/schemas/team.py`: Pydantic modeli.
- [ ] `esport/api/app/repositories/team_repo.py`: SQL upiti.
- [ ] `esport/api/app/services/team_service.py`: Poslovna logika za timove.
- [ ] `esport/api/app/routers/teams.py`: REST endpointi za CRUD.

### [KORAK 5] Kompleksna domena — Igrači i Turniri (Predavanje 5)
Implementacija glavnih entiteta i njihovih veza.
- [ ] `esport/api/app/models/player.py`: Igrači.
- [ ] `esport/api/app/models/tournament.py`: Turniri.
- [ ] `esport/api/app/models/participation.py`: Spojna tablica (Igrač -> Turnir).
- [ ] Implementacija Repositories, Services i Routers za sve nove entitete.

### [KORAK 6] Faze turnira i poslovna pravila (Predavanje 6)
Dodavanje "inteligentne" logike i validacije.
- [ ] `esport/api/app/core/phases.py`: Finite State Machine za faze turnira (Otvoreno, U tijeku, Završeno).
- [ ] Refiniranje `tournament_service.py` s provjerom rokova i faza.

---

## Verifikacija
- Svaki korak će biti testiran putem **Swagger UI** (`/docs`).
- Validacija baze podataka putem Docker kontejnera.
- Provjera logova za ispravan rad middleware-a.
