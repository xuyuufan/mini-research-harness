# Mini Research Harness Demo Guide

## Project Overview

Mini Research Harness is a small local workflow tool for turning research and coding tasks into traceable project flows. Instead of leaving work inside a loose chat transcript, it stores a project, a generated plan, agent execution logs, and a final report.

The current agents are deterministic mocks. The project is designed to demonstrate workflow structure, persistence, bilingual output, and testability without requiring real OpenAI or Anthropic API keys.

## Problem

Ordinary chatbots are useful for quick answers, but longer research and coding tasks often become hard to manage:

- The task plan is scattered across conversation turns.
- It is difficult to see which steps were completed.
- Agent outputs are not stored as structured records.
- Final deliverables are mixed with intermediate discussion.
- The workflow is hard to test, replay, or reuse.

For project work, this makes it harder to explain what happened and harder to trust that the process will keep working.

## Solution

Mini Research Harness organizes the task as structured workflow state:

- `Project` stores the user task and project description.
- `TaskStep` stores the generated plan and step status.
- `AgentRun` stores each mock agent execution record.
- `Artifact` stores generated outputs.
- `Final Report` summarizes the workflow and explains the result.

This turns a research task from an unstructured chatbot conversation into a small, inspectable workflow system.

## Local Setup

Start the backend:

```powershell
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

Backend API docs:

```text
http://127.0.0.1:8000/docs
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend app:

```text
http://localhost:3000
```

## English Demo Flow

1. Open `http://localhost:3000`.
2. Select `English` in the language switcher.
3. Create a project, for example:
   - Project name: `Research workflow harness`
   - Task brief: `Turn a loose research task into a traceable workflow.`
4. Click `Create Project`.
5. Click `Generate Plan`.
6. Point out the four generated task steps.
7. Click `Run Workflow`.
8. Review the `Agent Execution Logs`.
9. Scroll to the `Final Report`.
10. Point out the section titled `Why this is not a plain chatbot`.

## Chinese Demo Flow

1. Open `http://localhost:3000`.
2. Select `中文` in the language switcher.
3. Create a Chinese project, for example:
   - Project name: `论文复现助手`
   - Task brief: `输入一篇论文，然后根据论文思路复现出代码实现。`
4. Click `创建项目`.
5. Click `生成计划`.
6. Point out that the generated plan is in Chinese, including a first step containing `明确`.
7. Click `运行 Workflow`.
8. Review the Chinese agent logs.
9. Scroll to the Chinese final report.
10. Point out the section containing `为什么`.

## What to Point Out During Demo

- This is not a normal chatbot. It stores structured workflow state instead of only chat messages.
- Workflow state is saved as `Project`, `TaskStep`, `AgentRun`, and `Artifact` records.
- The final report is an artifact generated from the workflow trace.
- The UI and generated workflow output support both English and Chinese.
- The backend has pytest smoke tests for health checks, English workflow, Chinese workflow, report artifacts, and SQLite foreign key enforcement.
- Current agents are deterministic mocks, so the demo does not depend on real LLM APIs or API keys.

## Current Limitations

- No real OpenAI or Anthropic API integration yet.
- No PDF or paper upload yet.
- No real code execution agent yet.
- No user login system yet.
- No advanced agent orchestration or dependency graph yet.

## Roadmap

- Connect real LLM APIs for dynamic plan and report generation.
- Add PDF or paper upload for research workflows.
- Add GitHub repository inspection for coding workflows.
- Export artifacts as Markdown, PDF, or downloadable files.
- Improve agent orchestration with richer step dependencies and context handoff.
