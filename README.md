# Mini Research Harness

Beginner-friendly monorepo scaffold for a web-based multi-agent research workflow tool.

## Project structure

- `frontend/` - Next.js + React + Tailwind dashboard UI.
- `backend/` - FastAPI + SQLite API server with mock agent behavior.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000`.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Runs on `http://localhost:8000`.

## API endpoints included

- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `POST /projects/{project_id}/plan`
- `POST /projects/{project_id}/agent-runs`
- `GET /projects/{project_id}/agent-runs`

All planning and agent-run outputs are currently mocked for simple local development.
