import { Project } from "@/lib/types";

type ProjectSidebarProps = {
  projects: Project[];
  selectedProjectId: number | null;
  onSelectProject: (projectId: number) => void;
};

export function ProjectSidebar({ projects, selectedProjectId, onSelectProject }: ProjectSidebarProps) {
  return (
    <aside className="border-r border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">Projects</h2>
      <ul className="space-y-2">
        {projects.map((project) => {
          const selected = project.id === selectedProjectId;
          return (
            <li key={project.id}>
              <button
                className={`w-full rounded border p-3 text-left transition ${
                  selected
                    ? "border-blue-500 bg-blue-50 text-blue-950"
                    : "border-slate-200 bg-slate-50 hover:border-slate-300"
                }`}
                onClick={() => onSelectProject(project.id)}
                type="button"
              >
                <span className="block font-medium">{project.name}</span>
                <span className="mt-1 line-clamp-2 block text-sm text-slate-600">{project.description}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
