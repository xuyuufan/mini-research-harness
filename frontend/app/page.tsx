"use client";

import { useEffect, useMemo, useState } from "react";

import { AgentExecutionLogPanel } from "@/components/AgentExecutionLogPanel";
import { ArtifactListPanel } from "@/components/ArtifactListPanel";
import { GeneratedPlanPanel } from "@/components/GeneratedPlanPanel";
import { ProjectSidebar } from "@/components/ProjectSidebar";
import { ReportPanel } from "@/components/ReportPanel";
import { TaskInputPanel } from "@/components/TaskInputPanel";
import {
  createProject,
  executeWorkflow,
  generatePlan,
  getArtifactDownloadUrl,
  getProject,
  listProjects,
} from "@/lib/api";
import { Artifact, Language, Project, ProjectDetail } from "@/lib/types";

const copy = {
  en: {
    agentLogs: "Agent Execution Logs",
    artifactCreatedAt: "Created",
    artifactEmpty: "No artifacts yet.",
    artifactName: "Name",
    artifacts: "Artifacts",
    artifactType: "Type",
    chatbotHeading: "Harness vs Chatbot",
    chatbotText:
      "This app treats work as a project with persisted steps, assigned local agents, execution logs, statuses, and a generated artifact. A normal chatbot is mostly a conversation transcript; this harness makes the workflow inspectable, resumable, and testable.",
    createProject: "Create Project",
    defaultDescription:
      "Turn research and coding tasks into a traceable workflow with plan, agent logs, and a final report.",
    defaultName: "Mini research workflow",
    descriptionLabel: "Task brief",
    descriptionPlaceholder: "Describe the research or coding task to track...",
    download: "Download",
    downloadMarkdown: "Download Markdown",
    emptyLogs: "No agent runs yet.",
    emptyPlan: "No plan generated yet.",
    emptyReport: "Run the workflow to generate a report artifact.",
    fallbackDescription:
      "Create a project, generate a plan, execute deterministic local agents, and inspect the report artifact.",
    fallbackTitle: "Mini Research Harness",
    finalReport: "Final Report",
    generatePlan: "Generate Plan",
    language: "Language",
    manualRun: "Manual run",
    nameLabel: "Project name",
    namePlaceholder: "Research workflow harness",
    plan: "Generated Plan",
    projects: "Projects",
    runWorkflow: "Run Workflow",
    step: "Step",
    unknownStep: "Unknown step",
  },
  zh: {
    artifactCreatedAt: "创建时间",
    artifactEmpty: "还没有产物。",
    artifactName: "名称",
    artifacts: "产物",
    artifactType: "类型",
    agentLogs: "Agent 执行日志",
    chatbotHeading: "Harness 和普通 Chatbot 的区别",
    chatbotText:
      "这个应用把工作当作一个项目来管理：它会保存步骤、分配的本地 agents、执行日志、状态和最终产物。普通 chatbot 多数只是对话记录；这个 harness 让 workflow 可以被检查、继续推进和测试。",
    createProject: "创建项目",
    defaultDescription: "把研究和代码任务变成可追踪 workflow，包含计划、agent 日志和最终报告。",
    defaultName: "迷你研究 workflow",
    descriptionLabel: "任务简介",
    descriptionPlaceholder: "描述需要追踪的研究或代码任务...",
    download: "下载",
    downloadMarkdown: "下载 Markdown",
    emptyLogs: "还没有 agent 执行记录。",
    emptyPlan: "还没有生成计划。",
    emptyReport: "运行 workflow 后会生成报告产物。",
    fallbackDescription: "创建项目、生成计划、执行确定性的本地 agents，并查看报告产物。",
    fallbackTitle: "Mini Research Harness",
    finalReport: "最终报告",
    generatePlan: "生成计划",
    language: "语言",
    manualRun: "手动执行",
    nameLabel: "项目名称",
    namePlaceholder: "研究 workflow harness",
    plan: "生成的计划",
    projects: "项目",
    runWorkflow: "运行 Workflow",
    step: "步骤",
    unknownStep: "未知步骤",
  },
} satisfies Record<Language, Record<string, string>>;

export default function HomePage() {
  const [language, setLanguage] = useState<Language>("en");
  const t = copy[language];
  const [description, setDescription] = useState(t.defaultDescription);
  const [error, setError] = useState<string | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [name, setName] = useState(t.defaultName);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [detail, setDetail] = useState<ProjectDetail | null>(null);

  const report = useMemo<Artifact | null>(() => {
    return detail?.artifacts.find((artifact) => artifact.artifact_type === "markdown") ?? null;
  }, [detail]);
  const reportDownloadUrl = detail && report ? getArtifactDownloadUrl(detail.project.id, report.id) : null;

  function handleLanguageChange(nextLanguage: Language) {
    setLanguage(nextLanguage);
    setName((currentName) => (currentName === copy[language].defaultName ? copy[nextLanguage].defaultName : currentName));
    setDescription((currentDescription) =>
      currentDescription === copy[language].defaultDescription ? copy[nextLanguage].defaultDescription : currentDescription,
    );
  }

  async function refreshProjects(selectProjectId?: number) {
    const nextProjects = await listProjects();
    setProjects(nextProjects);
    const nextSelectedId = selectProjectId ?? selectedProjectId ?? nextProjects[0]?.id ?? null;
    setSelectedProjectId(nextSelectedId);
    if (nextSelectedId) {
      setDetail(await getProject(nextSelectedId));
    } else {
      setDetail(null);
    }
  }

  async function runAction(action: () => Promise<void>) {
    setError(null);
    setIsBusy(true);
    try {
      await action();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unknown error");
    } finally {
      setIsBusy(false);
    }
  }

  useEffect(() => {
    void runAction(() => refreshProjects());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleCreateProject() {
    await runAction(async () => {
      const project = await createProject(name.trim(), description.trim());
      await refreshProjects(project.id);
    });
  }

  async function handleSelectProject(projectId: number) {
    await runAction(async () => {
      setSelectedProjectId(projectId);
      setDetail(await getProject(projectId));
    });
  }

  async function handleGeneratePlan() {
    if (!selectedProjectId) return;
    await runAction(async () => {
      await generatePlan(selectedProjectId, language);
      setDetail(await getProject(selectedProjectId));
    });
  }

  async function handleExecuteWorkflow() {
    if (!selectedProjectId) return;
    await runAction(async () => {
      const result = await executeWorkflow(selectedProjectId, language);
      setDetail({
        project: result.project,
        task_steps: result.task_steps,
        agent_runs: result.agent_runs,
        artifacts: [result.report],
      });
      await refreshProjects(selectedProjectId);
    });
  }

  return (
    <main className="min-h-screen bg-slate-100 text-slate-950">
      <div className="border-b border-slate-200 bg-white px-4 py-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-xl font-bold">Mini Research Harness</h1>
          <div className="flex items-center gap-2 text-sm">
            <span className="font-medium text-slate-600">{t.language}</span>
            <div className="rounded border border-slate-300 bg-slate-50 p-1">
              <button
                className={`rounded px-3 py-1 ${language === "en" ? "bg-slate-950 text-white" : "text-slate-700"}`}
                onClick={() => handleLanguageChange("en")}
                type="button"
              >
                English
              </button>
              <button
                className={`rounded px-3 py-1 ${language === "zh" ? "bg-slate-950 text-white" : "text-slate-700"}`}
                onClick={() => handleLanguageChange("zh")}
                type="button"
              >
                中文
              </button>
            </div>
          </div>
        </div>
      </div>
      <TaskInputPanel
        createProjectLabel={t.createProject}
        description={description}
        descriptionLabel={t.descriptionLabel}
        descriptionPlaceholder={t.descriptionPlaceholder}
        isBusy={isBusy}
        name={name}
        nameLabel={t.nameLabel}
        namePlaceholder={t.namePlaceholder}
        onCreateProject={handleCreateProject}
        onDescriptionChange={setDescription}
        onNameChange={setName}
      />
      <div className="grid min-h-[calc(100vh-184px)] grid-cols-1 lg:grid-cols-[320px_1fr]">
        <ProjectSidebar
          heading={t.projects}
          onSelectProject={handleSelectProject}
          projects={projects}
          selectedProjectId={selectedProjectId}
        />
        <section className="space-y-4 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3 rounded border border-slate-200 bg-white p-4">
            <div>
              <h1 className="text-2xl font-bold">{detail?.project.name ?? t.fallbackTitle}</h1>
              <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">
                {detail?.project.description ?? t.fallbackDescription}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                className="rounded border border-slate-300 px-3 py-2 text-sm font-medium hover:bg-slate-50 disabled:cursor-not-allowed disabled:text-slate-400"
                disabled={isBusy || !selectedProjectId}
                onClick={handleGeneratePlan}
                type="button"
              >
                {t.generatePlan}
              </button>
              <button
                className="rounded bg-slate-950 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                disabled={isBusy || !selectedProjectId}
                onClick={handleExecuteWorkflow}
                type="button"
              >
                {t.runWorkflow}
              </button>
            </div>
          </div>
          {error ? (
            <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>
          ) : null}
          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            <GeneratedPlanPanel emptyLabel={t.emptyPlan} heading={t.plan} steps={detail?.task_steps ?? []} />
            <AgentExecutionLogPanel
              emptyLabel={t.emptyLogs}
              heading={t.agentLogs}
              manualRunLabel={t.manualRun}
              runs={detail?.agent_runs ?? []}
              stepLabel={t.step}
              steps={detail?.task_steps ?? []}
              unknownStepLabel={t.unknownStep}
            />
          </div>
          <ReportPanel
            downloadLabel={t.downloadMarkdown}
            downloadUrl={reportDownloadUrl}
            emptyLabel={t.emptyReport}
            heading={t.finalReport}
            report={report}
          />
          <ArtifactListPanel
            artifacts={detail?.artifacts ?? []}
            createdAtLabel={t.artifactCreatedAt}
            downloadLabel={t.download}
            emptyLabel={t.artifactEmpty}
            getDownloadUrl={(artifact) => getArtifactDownloadUrl(artifact.project_id, artifact.id)}
            heading={t.artifacts}
            nameLabel={t.artifactName}
            typeLabel={t.artifactType}
          />
          <section className="rounded border border-slate-200 bg-white p-4">
            <h2 className="mb-2 text-lg font-semibold">{t.chatbotHeading}</h2>
            <p className="text-sm leading-6 text-slate-700">{t.chatbotText}</p>
          </section>
        </section>
      </div>
    </main>
  );
}
