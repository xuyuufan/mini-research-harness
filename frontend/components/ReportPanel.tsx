import { Artifact } from "@/lib/types";

type ReportPanelProps = {
  downloadLabel: string;
  downloadUrl: string | null;
  emptyLabel: string;
  heading: string;
  report: Artifact | null;
};

export function ReportPanel({ downloadLabel, downloadUrl, emptyLabel, heading, report }: ReportPanelProps) {
  return (
    <section className="rounded border border-slate-200 bg-white p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">{heading}</h2>
        {report && downloadUrl ? (
          <a
            className="rounded border border-slate-300 px-3 py-2 text-sm font-medium hover:bg-slate-50"
            href={downloadUrl}
          >
            {downloadLabel}
          </a>
        ) : null}
      </div>
      {report ? (
        <pre className="max-h-[420px] overflow-auto whitespace-pre-wrap rounded border border-slate-200 bg-slate-950 p-4 text-sm leading-6 text-slate-100">
          {report.content}
        </pre>
      ) : (
        <p className="text-sm text-slate-500">{emptyLabel}</p>
      )}
    </section>
  );
}
