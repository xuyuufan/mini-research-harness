import { Artifact } from "@/lib/types";

type ArtifactListPanelProps = {
  artifacts: Artifact[];
  createdAtLabel: string;
  downloadLabel: string;
  emptyLabel: string;
  getDownloadUrl: (artifact: Artifact) => string;
  heading: string;
  nameLabel: string;
  typeLabel: string;
};

export function ArtifactListPanel({
  artifacts,
  createdAtLabel,
  downloadLabel,
  emptyLabel,
  getDownloadUrl,
  heading,
  nameLabel,
  typeLabel,
}: ArtifactListPanelProps) {
  return (
    <section className="rounded border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-lg font-semibold">{heading}</h2>
      {artifacts.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-sm">
            <thead className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="py-2 pr-3 font-semibold">{nameLabel}</th>
                <th className="py-2 pr-3 font-semibold">{typeLabel}</th>
                <th className="py-2 pr-3 font-semibold">{createdAtLabel}</th>
                <th className="py-2 text-right font-semibold">{downloadLabel}</th>
              </tr>
            </thead>
            <tbody>
              {artifacts.map((artifact) => (
                <tr key={artifact.id} className="border-b border-slate-100 last:border-b-0">
                  <td className="py-3 pr-3 font-medium text-slate-950">{artifact.name}</td>
                  <td className="py-3 pr-3 text-slate-600">{artifact.artifact_type}</td>
                  <td className="py-3 pr-3 text-slate-600">
                    {new Date(artifact.created_at).toLocaleString()}
                  </td>
                  <td className="py-3 text-right">
                    <a
                      className="rounded border border-slate-300 px-3 py-2 text-sm font-medium hover:bg-slate-50"
                      href={getDownloadUrl(artifact)}
                    >
                      {downloadLabel}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-sm text-slate-500">{emptyLabel}</p>
      )}
    </section>
  );
}
