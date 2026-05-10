import { AgentRun } from "@/lib/types";

export function AgentExecutionLogPanel({ runs }: { runs: AgentRun[] }) {
  return (
    <section className="bg-white rounded-lg p-4 shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold mb-3">Agent Execution Logs</h2>
      <div className="space-y-2">
        {runs.map((run) => (
          <article key={run.id} className="p-2 rounded bg-slate-50 border border-slate-200">
            <p className="font-medium">{run.agent_name}</p>
            <p className="text-sm text-slate-600">Step: {run.step_title}</p>
            <p className="text-xs text-slate-500">Status: {run.status}</p>
            <p className="text-sm mt-1">{run.output}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
