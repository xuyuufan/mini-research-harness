import { AgentRun, TaskStep } from "@/lib/types";

type AgentExecutionLogPanelProps = {
  runs: AgentRun[];
  steps: TaskStep[];
};

export function AgentExecutionLogPanel({ runs, steps }: AgentExecutionLogPanelProps) {
  const stepTitles = new Map(steps.map((step) => [step.id, step.title]));

  return (
    <section className="rounded border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-lg font-semibold">Agent Execution Logs</h2>
      <div className="space-y-2">
        {runs.map((run) => (
          <article key={run.id} className="rounded border border-slate-200 bg-slate-50 p-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="font-medium text-slate-950">{run.agent_name}</p>
              <span className="rounded bg-blue-100 px-2 py-1 text-xs text-blue-800">{run.status}</span>
            </div>
            <p className="mt-1 text-sm text-slate-600">
              Step: {run.task_step_id ? stepTitles.get(run.task_step_id) ?? "Unknown step" : "Manual run"}
            </p>
            <p className="mt-2 text-sm leading-6 text-slate-800">{run.output}</p>
          </article>
        ))}
      </div>
      {runs.length === 0 ? <p className="text-sm text-slate-500">No agent runs yet.</p> : null}
    </section>
  );
}
