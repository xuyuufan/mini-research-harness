from . import models


def build_plan_prompt(project: models.Project, language: str = "en"):
    if language == "zh":
        return f"""你正在使用 Mini Research Harness。

请把下面的项目拆分成 4 个任务步骤。
每个任务步骤都必须包含 step number、title 和 assigned agent。
请输出结构化 JSON，或清晰结构化的文本，便于后续保存为 TaskStep。

项目名称: {project.name}
项目描述: {project.description}
"""

    return f"""You are using Mini Research Harness.

Break the project below into 4 task steps.
Each task step must include a step number, title, and assigned agent.
Return structured JSON or clearly structured text that can be saved as TaskStep records.

Project name: {project.name}
Project description: {project.description}
"""


def build_agent_run_prompt(project: models.Project, step: models.TaskStep, language: str = "en"):
    if language == "zh":
        return f"""你正在使用 Mini Research Harness。

请以 {step.assigned_agent} 的角色完成这个任务步骤。
输出应简洁，并且可以直接保存为 AgentRun output。

项目名称: {project.name}
项目描述: {project.description}
任务标题: {step.title}
分配的 agent: {step.assigned_agent}
任务状态: {step.status}
"""

    return f"""You are using Mini Research Harness.

Act as {step.assigned_agent} and complete this task step.
Keep the output concise and suitable for saving as an AgentRun output.

Project name: {project.name}
Project description: {project.description}
Step title: {step.title}
Assigned agent: {step.assigned_agent}
Step status: {step.status}
"""


def build_report_prompt(
    project: models.Project,
    steps: list[models.TaskStep],
    runs: list[models.AgentRun],
    language: str = "en",
):
    step_lines = "\n".join(
        f"- {step.step_number}. {step.title} | agent: {step.assigned_agent} | status: {step.status}" for step in steps
    )
    run_lines = "\n".join(f"- {run.agent_name}: {run.output}" for run in runs)

    if language == "zh":
        return f"""你正在使用 Mini Research Harness。

请基于项目、所有任务步骤和所有 agent runs 生成 Markdown 最终报告。
报告必须解释为什么这个 harness 不是普通 chatbot。

项目名称: {project.name}
项目描述: {project.description}

任务步骤:
{step_lines}

Agent runs:
{run_lines}
"""

    return f"""You are using Mini Research Harness.

Generate a Markdown final report from the project, all task steps, and all agent runs.
The report must explain why this harness is not a plain chatbot.

Project name: {project.name}
Project description: {project.description}

Task steps:
{step_lines}

Agent runs:
{run_lines}
"""
