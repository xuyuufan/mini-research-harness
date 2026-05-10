import { TaskStep } from "@/lib/types";

export function GeneratedPlanPanel({ steps }: { steps: TaskStep[] }) {
  return (
    <section className="rounded border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-lg font-semibold">Generated Plan</h2>
      <ol className="space-y-2">
        {steps.map((step) => (
          <li key={step.id} className="rounded border border-slate-200 bg-slate-50 p-3">
            <p className="font-medium text-slate-950">
              {step.step_number}. {step.title}
            </p>
            <div className="mt-2 flex flex-wrap gap-2 text-xs">
              <span className="rounded bg-slate-200 px-2 py-1 text-slate-700">{step.assigned_agent}</span>
              <span className="rounded bg-emerald-100 px-2 py-1 text-emerald-800">{step.status}</span>
            </div>
          </li>
        ))}
      </ol>
      {steps.length === 0 ? <p className="text-sm text-slate-500">No plan generated yet.</p> : null}
    </section>
  );
}
