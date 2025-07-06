# Issues & Insights Tracker

Lightweight portal for receiving file‑based feedback (bug reports, invoices, images) and turning it into structured data for analytics.

| Layer      | Tech |
|------------|------|
| Frontend   | **SvelteKit** + Tailwind |
| Auth       | Email / Password **+ Google OAuth** (Auth.js) |
| Backend    | **FastAPI** + SQLAlchemy + PostgreSQL |
| Realtime   | Server‑Sent Events (SSE) |
| Worker     | APScheduler (30‑min stats) |
| Tests      | Pytest (≥ 80 %) + Playwright e2e |
| CI         | GitHub Actions |
| Docker     | Single `docker-compose up` |
| Hosting    | Frontend static build auto‑deployed on **Netlify** |

---

## Features
* **Auth & RBAC** – `ADMIN`, `MAINTAINER`, `REPORTER`
* **Issue CRUD** – title · markdown description · file upload · severity · status workflow
* **Realtime list** – auto‑refresh via SSE
* **Dashboard** – live counts of open issues per severity
* **Daily stats** – worker writes to `daily_stats` every 30 min
* **Swagger** – `/api/docs`
* **CI** – lint + Pytest + Playwright on every push

---

## Quick Start (local)

```bash
git clone https://github.com/your‑org/tracker25.git
cd tracker25
cp .env.example .env   # edit DB / secret / Google client ID
docker compose up --build
```

* API docs → <http://localhost:8000/api/docs>  
* App UI  → <http://localhost:5173>

---

## Demo Credentials

| Role | Email | Password |
|------|---------------------------|----------|
| **Admin** | admin@example.com      | test1234 |
| Maintainer | maintainer@example.com | test1234 |
| Reporter | reporter@example.com   | test1234 |

Google OAuth logs any Google account in as a **REPORTER** on first use.

---

## Architecture

```
SvelteKit UI  ←SSE─┐
                  ├── FastAPI  ──→ PostgreSQL
APScheduler worker ┘
```

---

## Scripts

| Dir | Command | Purpose |
|-----|---------|---------|
| root | `docker compose up -d` | start db, api, worker |
| backend | `pytest --cov=app` | backend tests + coverage |
| frontend | `npx playwright test` | e2e happy‑path |
| frontend | `npm run dev` | hot‑reload dev server |

---

## CI (GitHub Actions)

1. Postgres service  
2. Python deps → **Pytest + coverage**  
3. Node deps → **Playwright e2e**  
4. Docker image build

Status badge  
![CI](https://github.com/your-org/tracker25/actions/workflows/ci.yml/badge.svg)

---

## Netlify (bonus)

`frontend/dist` auto‑deployed on Netlify. Redirect rule if backend on another domain:

```
/api/* https://api.yourdomain.com/:splat  200
```

---

## Trade‑Offs

* **SSE vs WebSockets** – simpler, native.
* **APScheduler vs Celery** – lighter stack.
* **Numeric dashboard** – no SSR chart issues.

---

Happy shipping 🚀
