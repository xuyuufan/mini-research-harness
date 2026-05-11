# Mini Research Harness

A small local multi-agent research workflow harness. It turns a loose research or coding task into a traceable project with a plan, assigned local agents, execution logs, and a final markdown report.

This project does not call real OpenAI or Anthropic APIs. The agents are deterministic local mocks so the workflow can be developed and tested without credentials.

## What it does

- Creates research projects with a name and task brief.
- Generates ordered workflow steps for each project.
- Assigns each step to a local mock agent.
- Executes the workflow and stores agent run records.
- Generates a final report artifact.
- Shows the project, plan, logs, statuses, and report in the frontend.
- Supports English and Chinese UI text, generated plans, agent logs, and reports.

## Why this is not a plain chatbot

A normal chatbot keeps work as a conversation transcript. This harness stores structured workflow state:

- `Project`
- `TaskStep`
- `AgentRun`
- `Artifact`

That makes the work easier to inspect, resume, test, and explain.

## Project structure

- `frontend/` - Next.js + React + Tailwind workflow UI.
- `backend/` - FastAPI + SQLite API server with local mock agents.

## Demo guide

See [docs/demo-guide.md](docs/demo-guide.md) for a walkthrough you can use in demos, resumes, and interviews.

## Backend

```powershell
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

Runs on `http://127.0.0.1:8000`.

API docs are available at `http://127.0.0.1:8000/docs`.

### Provider configuration

The default agent provider is `local`.

```text
AGENT_PROVIDER=local
```

```powershell
$env:AGENT_PROVIDER = "local"
```

The local provider uses deterministic mock agents. The project does not currently connect to real OpenAI or Anthropic APIs.

### Backend tests

```powershell
cd backend
py -m pytest
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000`.

## Workflow

1. Open the frontend.
2. Choose `English` or `中文`.
3. Enter a project name and task brief.
4. Click `Create Project`.
5. Click `Generate Plan`.
6. Click `Run Workflow`.
7. Review the generated plan, agent execution logs, and final report.

## API endpoints

- `GET /health`
- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `POST /projects/{project_id}/plan`
- `POST /projects/{project_id}/agent-runs`
- `GET /projects/{project_id}/agent-runs`
- `POST /projects/{project_id}/execute`
- `GET /projects/{project_id}/artifacts`
- `GET /workflow-explanation`
