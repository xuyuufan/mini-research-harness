import { TaskStep } from "@/lib/types";

export function GeneratedPlanPanel({ steps }: { steps: TaskStep[] }) {
  return (
    <section className="bg-white rounded-lg p-4 shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold mb-3">Generated Plan</h2>
      <ol className="space-y-2">
        {steps.map((step) => (
          <li key={step.step_number} className="p-2 rounded bg-slate-50 border border-slate-200">
            <p className="font-medium">
              {step.step_number}. {step.title}
            </p>
            <p className="text-sm text-slate-600">Agent: {step.assigned_agent}</p>
            <p className="text-xs text-slate-500">Status: {step.status}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}
