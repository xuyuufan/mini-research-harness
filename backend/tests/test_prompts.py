import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import models
from app.prompts import build_agent_run_prompt, build_plan_prompt, build_report_prompt


def make_project():
    return models.Project(name="Workflow audit", description="Inspect the research workflow end to end.")


def make_step():
    return models.TaskStep(
        step_number=2,
        title="Review source material",
        assigned_agent="Research Agent",
        status="pending",
    )


def make_run():
    return models.AgentRun(agent_name="Research Agent", status="completed", output="Found three relevant sources.")


def test_english_plan_prompt_contains_project_name():
    prompt = build_plan_prompt(make_project(), language="en")

    assert "Workflow audit" in prompt


def test_english_plan_prompt_mentions_four_task_steps():
    prompt = build_plan_prompt(make_project(), language="en")

    assert "4 task steps" in prompt


def test_chinese_plan_prompt_mentions_task_steps_or_four():
    prompt = build_plan_prompt(make_project(), language="zh")

    assert "任务步骤" in prompt or "4" in prompt


def test_agent_run_prompt_contains_step_title_and_assigned_agent():
    prompt = build_agent_run_prompt(make_project(), make_step(), language="en")

    assert "Review source material" in prompt
    assert "Research Agent" in prompt


def test_report_prompt_contains_agent_run_output():
    prompt = build_report_prompt(make_project(), [make_step()], [make_run()], language="en")

    assert "Found three relevant sources." in prompt


def test_report_prompt_requests_markdown_final_report():
    prompt = build_report_prompt(make_project(), [make_step()], [make_run()], language="en")

    assert "Markdown final report" in prompt
