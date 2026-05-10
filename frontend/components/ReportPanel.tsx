import { Artifact } from "@/lib/types";

export function ReportPanel({ report }: { report: Artifact | null }) {
  return (
    <section className="rounded border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-lg font-semibold">Final Report</h2>
      {report ? (
        <pre className="max-h-[420px] overflow-auto whitespace-pre-wrap rounded border border-slate-200 bg-slate-950 p-4 text-sm leading-6 text-slate-100">
          {report.content}
        </pre>
      ) : (
        <p className="text-sm text-slate-500">Run the workflow to generate a report artifact.</p>
      )}
    </section>
  );
}
