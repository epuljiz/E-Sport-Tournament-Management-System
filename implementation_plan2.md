# E-sports Tournament Management System - Dio 2: Frontend i Deploy

Ovaj dokument je implementacijski plan za izgradnju Vue 3 frontend aplikacije i njen deploy na Render platformu (Predavanja 7-11). Time pokrivamo drugu i finalnu obranu projekta.

## Pregled tehnologija
- **Frontend Framework**: Vue 3 (Composition API)
- **Build alat**: Vite
- **Routing**: Vue Router
- **State Management**: Pinia
- **API Komunikacija**: Axios (s custom interceptorima)
- **Stilizacija**: Čisti (vlastiti) CSS
- **Deployment**: Render (uz besplatnu PostgreSQL bazu)

---

## Plan razvoja po koracima

### [KORAK 7] Frontend - Inicijalizacija i setup okoline (Predavanje 7)
Postavljanje modernog frontend Vue 3 okruženja uz Vite.
- Inicijalizacija projekta u mapi `esport/web` (odnosno `E-Sport-Tournament-Management-System/web`).
- Čišćenje defaultnog Vite templatea (`App.vue`, `style.css`).
- Dodavanje osnovnih CSS stilova.
- Instalacija i konfiguracija Pinia (State Management).
- Instalacija i konfiguracija Vue Routera.

### [KORAK 8] API Servis i Autentikacija klijenata (Predavanje 8)
Postavljanje Axios klijenta i komunikacija s backendom.
- Kreiranje `src/services/api.ts` za komunikaciju.
- Dodavanje interceptora za slanje JWT access tokena.
- Dodavanje interceptora za automatsko osvježavanje JWT tokena kod povratka 401 greške s backenda (refresh flow).
- Kreiranje Pinia storea: `src/stores/auth.ts` za pohranu logiranog korisnika i JWT tokena.

### [KORAK 9] Routing, Views i Route Guards (Predavanje 9)
Izgradnja prikaza aplikacije i usmjeravanja.
- `src/router/index.ts`: Definiranje minimalno 5 ruta (Login, Admin Početna, Admin Turniri, Tim Početna, Tim Igrači).
- `src/views/PrijavaView.vue`: Stranica za prijavu.
- `src/views/admin/*`: Prikazi za admine.
- `src/views/team/*`: Prikazi za upravitelje timova.
- Route guards: Zaštita ruta kako neautenticirani korisnici ne bi mogli ući unutar aplikacije i onemogućavanje pristupa admin rutama za obične korisnike (timove).

### [KORAK 10] UX Stanja, Prikazi i Forme (Predavanje 10)
Komunikacija korisnika s aplikacijom na naprednoj razini.
- Prikaz `loading` indikatora dok se dohvaćaju podaci s API-ja.
- Prikaz praznog stanja `empty` ako podaci ne postoje.
- Hvatanje i prikaz `error` poruka od API-ja (Pinia store `obavijesti.ts`).
- Forme (dodavanje igrača, kreiranje turnira, prijave) uz osnovnu validaciju prije slanja na backend.

### [KORAK 11] Deployment na Render (Predavanje 11)
Postavljanje backenda i frontenda na live server radi konačne predaje.
- Dodavanje `render.yaml` (ili ekvivalentnih konfiguracija) u direktorij `E-Sport-Tournament-Management-System`.
- Kreiranje baze na Render platformi.
- Konfiguracija varijabli okruženja (`.env` vs Render Env Variables).
- Rješavanje CORS-a u backendu za pristup s frontend domene.
- Uspješan Build frontenda u produkcijski kod.

---

## Verifikacija plana
- Aplikacija će imati zasebne `/admin` i `/team` frontend tokove.
- Nakon izgradnje frontenda odradit će se testiranje svih CRUD operacija.
