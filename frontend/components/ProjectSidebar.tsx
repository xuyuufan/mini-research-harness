import { Project } from "@/lib/types";

export function ProjectSidebar({ projects }: { projects: Project[] }) {
  return (
    <aside className="bg-white rounded-lg p-4 shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold mb-3">Projects</h2>
      <ul className="space-y-2">
        {projects.map((project) => (
          <li key={project.id} className="p-2 rounded bg-slate-50 border border-slate-200">
            <p className="font-medium">{project.name}</p>
            <p className="text-sm text-slate-600">{project.description}</p>
          </li>
        ))}
      </ul>
    </aside>
  );
}
