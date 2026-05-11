def normalize_language(language: str):
    return "zh" if language.lower().startswith("zh") else "en"


COPY = {
    "en": {
        "default_subject": "the task",
        "no_description": "No description was provided.",
        "no_project_description": "No project description was provided.",
        "plan_scope": "Clarify scope for {subject}",
        "plan_research": "Collect constraints, assumptions, and reference points",
        "plan_synthesis": "Turn findings into an implementation plan",
        "plan_report": "Create a final report with decisions and next actions",
        "planner_output": (
            "Scope locked for '{name}'. Task brief: {description} "
            "The workflow will track plan, execution logs, and report artifacts separately."
        ),
        "research_output": (
            "Research notes: identify the user goal, expected deliverables, local run constraints, "
            "data entities, and UI surfaces before implementation."
        ),
        "synthesis_output": (
            "Implementation strategy: keep deterministic local agents, persist every step, "
            "and expose a project detail endpoint that the UI can render directly."
        ),
        "reporter_output": (
            "Report draft completed: summarize objective, workflow trace, outputs, and how this differs "
            "from a plain chatbot transcript."
        ),
        "report_title": "Research Workflow Report: {name}",
        "goal": "Goal",
        "workflow_status": "Workflow Status",
        "completed": "{completed} of {total} steps completed.",
        "tracked_plan": "Tracked Plan",
        "execution_trace": "Agent Execution Trace",
        "not_chatbot": "Why this is not a plain chatbot",
        "not_chatbot_body": (
            "This harness stores a project, a planned sequence of task steps, structured agent runs, "
            "and a final report artifact. A normal chatbot usually leaves work as an unstructured "
            "conversation; this workflow makes ownership, status, outputs, and the final deliverable "
            "inspectable and repeatable."
        ),
        "step_line": "- Step {number}: {title} [{status}] assigned to {agent}",
        "workflow_explanation": {
            "chatbot": "A chatbot keeps context mainly as conversational turns.",
            "harness": "This harness persists projects, task steps, agent runs, statuses, and report artifacts.",
            "benefit": "The work can be inspected, resumed, tested, and explained as a project workflow.",
        },
    },
    "zh": {
        "default_subject": "任务",
        "no_description": "未提供任务描述。",
        "no_project_description": "未提供项目描述。",
        "plan_scope": "明确 {subject} 的范围",
        "plan_research": "收集约束、假设和参考信息",
        "plan_synthesis": "把调研结果整理成实施计划",
        "plan_report": "生成包含决策和后续行动的最终报告",
        "planner_output": (
            "已锁定项目 '{name}' 的范围。任务简介：{description} "
            "该 workflow 会分别追踪计划、执行日志和报告产物。"
        ),
        "research_output": "调研记录：先识别用户目标、预期交付物、本地运行约束、数据实体和 UI 展示区域。",
        "synthesis_output": (
            "实施策略：保留确定性的本地 agents，持久化每个步骤，"
            "并提供前端可直接渲染的项目详情接口。"
        ),
        "reporter_output": "报告草稿已完成：总结目标、workflow 轨迹、输出，以及它和普通 chatbot 的区别。",
        "report_title": "研究 Workflow 报告：{name}",
        "goal": "目标",
        "workflow_status": "Workflow 状态",
        "completed": "已完成 {completed} / {total} 个步骤。",
        "tracked_plan": "可追踪计划",
        "execution_trace": "Agent 执行轨迹",
        "not_chatbot": "为什么它不是普通 chatbot",
        "not_chatbot_body": (
            "这个 harness 会保存项目、计划步骤、结构化 agent run 和最终报告产物。"
            "普通 chatbot 通常只留下非结构化对话；这个 workflow 让负责人、状态、输出和"
            "最终交付物都可以被检查和复现。"
        ),
        "step_line": "- 步骤 {number}: {title} [{status}] 分配给 {agent}",
        "workflow_explanation": {
            "chatbot": "普通 chatbot 主要把上下文保存为对话轮次。",
            "harness": "这个 harness 会持久化项目、任务步骤、agent run、状态和报告产物。",
            "benefit": "这让工作可以被检查、继续、测试，并作为项目 workflow 来解释。",
        },
    },
}


def get_copy(language: str):
    return COPY[normalize_language(language)]
