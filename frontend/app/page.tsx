"use client";

import { useEffect, useMemo, useState } from "react";

import { AgentExecutionLogPanel } from "@/components/AgentExecutionLogPanel";
import { GeneratedPlanPanel } from "@/components/GeneratedPlanPanel";
import { ProjectSidebar } from "@/components/ProjectSidebar";
import { ReportPanel } from "@/components/ReportPanel";
import { TaskInputPanel } from "@/components/TaskInputPanel";
import { createProject, executeWorkflow, generatePlan, getProject, listProjects } from "@/lib/api";
import { Artifact, Project, ProjectDetail } from "@/lib/types";

export default function HomePage() {
  const [description, setDescription] = useState(
    "Turn research and coding tasks into a traceable workflow with plan, agent logs, and a final report.",
  );
  const [error, setError] = useState<string | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [name, setName] = useState("Mini research workflow");
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [detail, setDetail] = useState<ProjectDetail | null>(null);

  const report = useMemo<Artifact | null>(() => {
    return detail?.artifacts.find((artifact) => artifact.artifact_type === "markdown") ?? null;
  }, [detail]);

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
      await generatePlan(selectedProjectId);
      setDetail(await getProject(selectedProjectId));
    });
  }

  async function handleExecuteWorkflow() {
    if (!selectedProjectId) return;
    await runAction(async () => {
      const result = await executeWorkflow(selectedProjectId);
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
      <TaskInputPanel
        description={description}
        isBusy={isBusy}
        name={name}
        onCreateProject={handleCreateProject}
        onDescriptionChange={setDescription}
        onNameChange={setName}
      />
      <div className="grid min-h-[calc(100vh-129px)] grid-cols-1 lg:grid-cols-[320px_1fr]">
        <ProjectSidebar
          onSelectProject={handleSelectProject}
          projects={projects}
          selectedProjectId={selectedProjectId}
        />
        <section className="space-y-4 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3 rounded border border-slate-200 bg-white p-4">
            <div>
              <h1 className="text-2xl font-bold">{detail?.project.name ?? "Mini Research Harness"}</h1>
              <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">
                {detail?.project.description ??
                  "Create a project, generate a plan, execute deterministic local agents, and inspect the report artifact."}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                className="rounded border border-slate-300 px-3 py-2 text-sm font-medium hover:bg-slate-50 disabled:cursor-not-allowed disabled:text-slate-400"
                disabled={isBusy || !selectedProjectId}
                onClick={handleGeneratePlan}
                type="button"
              >
                Generate Plan
              </button>
              <button
                className="rounded bg-slate-950 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                disabled={isBusy || !selectedProjectId}
                onClick={handleExecuteWorkflow}
                type="button"
              >
                Run Workflow
              </button>
            </div>
          </div>
          {error ? (
            <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>
          ) : null}
          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            <GeneratedPlanPanel steps={detail?.task_steps ?? []} />
            <AgentExecutionLogPanel runs={detail?.agent_runs ?? []} steps={detail?.task_steps ?? []} />
          </div>
          <ReportPanel report={report} />
          <section className="rounded border border-slate-200 bg-white p-4">
            <h2 className="mb-2 text-lg font-semibold">Harness vs Chatbot</h2>
            <p className="text-sm leading-6 text-slate-700">
              This app treats work as a project with persisted steps, assigned local agents, execution logs,
              statuses, and a generated artifact. A normal chatbot is mostly a conversation transcript; this harness
              makes the workflow inspectable, resumable, and testable.
            </p>
          </section>
        </section>
      </div>
    </main>
  );
}
