# E-sports Tournament Management System

Sustav za upravljanje e-sport turnirima, igračima i timovima.
Projekt prati strukturu i metodologiju kolegija **Razvoj web aplikacija**.

---

## Tehnologije

| Sloj     | Stack                                  |
|----------|----------------------------------------|
| Backend  | Python 3.11+, FastAPI, SQLAlchemy 2.0  |
| Baza     | PostgreSQL 16 (Docker Compose)         |
| Auth     | JWT (Access + Refresh tokeni)          |

---

## Preduvjeti

Prije pokretanja projekta trebate imati instalirano:

- **Python** ≥ 3.11 — [python.org](https://www.python.org/)
- **Docker Desktop** — [docker.com](https://www.docker.com/)
- **Git** — [git-scm.com](https://git-scm.com/)

---

## Brzo pokretanje

### 1. Postavljanje okoline i ENV varijabli

Uđite u `esport` direktorij i kopirajte primjer env varijabli:

```bash
cd esport/api

# Windows (PowerShell):
Copy-Item .env.example .env

# Linux/macOS:
cp .env.example .env
```

### 2. Pokretanje baze podataka (Docker)

Vratite se u root `esport` foldera i pokrenite PostgreSQL:

```bash
cd ..
docker compose up -d db
```

Provjera da baza radi:
```bash
docker compose ps
# Status treba biti "healthy"
```

### 3. Pokretanje Backenda (FastAPI)

```bash
cd api

# Kreiraj virtualno okruženje (jednom):
python -m venv .venv

# Aktiviraj ga:
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Linux/macOS:         source .venv/bin/activate

# Instaliraj zavisnosti:
pip install -r requirements.txt

# Pokreni dev server:
uvicorn app.main:app --reload
```

### 4. Provjera rada

- **Health check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) → `{"status": "ok"}`
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Struktura projekta

```
esport/
├── api/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py           # App factory
│   │   ├── core/             # Konfiguracija, greške, logging
│   │   ├── routers/          # API endpointi (moduli)
│   │   ├── services/         # Poslovna logika
│   │   ├── repositories/     # DB upiti
│   │   ├── models/           # SQLAlchemy modeli
│   │   └── schemas/          # Pydantic DTO-ovi
│   └── requirements.txt
├── docker-compose.yml        # PostgreSQL kontejner
├── implementation_plan.md    # Detaljan plan razvoja (6 koraka)
└── README.md                 # Ove upute
```

---

## Arhitektura slojeva

Projekt koristi strogo odvajanje odgovornosti prema modelu profesora:

1. **Router**: Prima HTTP zahtjev, poziva Service, vraća JSON.
2. **Service**: Provodi poslovna pravila i validaciju.
3. **Repository**: Izvršava SQL upite prema bazi.
4. **Model/Schema**: Određuje strukturu podataka.
