@echo off
echo ==================================================
echo   Pokretanje E-Sport Tournament Management Systema
echo ==================================================
echo.

echo [1/3] Pokretanje baze podataka (Docker)...
docker compose up -d
echo.

echo [2/3] Pokretanje FastAPI Backenda (otvorit ce se novi prozor)...
:: Ulazi u api, provjerava venv, instalira pakete i pokrece uvicorn
start "FastAPI Backend" cmd /k "cd api && if not exist .venv (python -m venv .venv) && call .venv\Scripts\activate.bat && if not exist .env (copy .env.example .env) && pip install -r requirements.txt && uvicorn app.main:app --reload"

echo [3/3] Pokretanje Vue Frontenda (otvorit ce se novi prozor)...
:: Ulazi u web, instalira npm pakete i pokrece vite server
start "Vue Frontend" cmd /k "cd web && npm install && npm run dev"

echo.
echo ==================================================
echo Svi procesi su pokrenuti! 
echo Frontend ce biti dostupan na http://localhost:5173
echo Backend API na http://127.0.0.1:8000
echo ==================================================
pause
