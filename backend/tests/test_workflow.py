import os
import sys
import tempfile
from pathlib import Path

db_path = os.path.join(tempfile.gettempdir(), "mini_research_harness_test.db")
if os.path.exists(db_path):
    os.remove(db_path)
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.database import engine
from app.main import app


def test_workflow_generates_plan_runs_and_report():
    client = TestClient(app)

    project = client.post(
        "/projects",
        json={
            "name": "论文复现",
            "description": "输入一篇论文，然后根据论文思路复现出代码实现。",
        },
    )
    assert project.status_code == 200
    project_id = project.json()["id"]

    plan = client.post(f"/projects/{project_id}/plan?language=zh")
    assert plan.status_code == 200
    plan_steps = plan.json()
    assert len(plan_steps) == 4
    assert "明确" in plan_steps[0]["title"]

    workflow = client.post(f"/projects/{project_id}/execute?language=zh")
    assert workflow.status_code == 200
    result = workflow.json()
    assert len(result["task_steps"]) == 4
    assert len(result["agent_runs"]) == 4
    assert "为什么" in result["report"]["content"]


def test_sqlite_foreign_keys_are_enabled():
    with engine.connect() as connection:
        assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar() == 1
