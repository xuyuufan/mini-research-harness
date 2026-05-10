import { AgentExecutionLogPanel } from "@/components/AgentExecutionLogPanel";
import { GeneratedPlanPanel } from "@/components/GeneratedPlanPanel";
import { ProjectSidebar } from "@/components/ProjectSidebar";
import { TaskInputPanel } from "@/components/TaskInputPanel";

const mockProjects = [
  { id: 1, name: "Build API Client", description: "Research API patterns and auth flow" },
  { id: 2, name: "Optimize Query", description: "Investigate slow SQLite query" },
];

const mockPlanSteps = [
  { step_number: 1, title: "Clarify requirements", assigned_agent: "Planner Agent", status: "completed" },
  { step_number: 2, title: "Research similar tools", assigned_agent: "Research Agent", status: "running" },
  { step_number: 3, title: "Draft implementation", assigned_agent: "Coder Agent", status: "pending" },
];

const mockRuns = [
  { id: 1, agent_name: "Planner Agent", step_title: "Clarify requirements", status: "completed", output: "Scope defined and milestones created." },
  { id: 2, agent_name: "Research Agent", step_title: "Research similar tools", status: "running", output: "Collecting benchmark references..." },
];

export default function HomePage() {
  return (
    <main className="min-h-screen p-6">
      <h1 className="text-2xl font-bold mb-4">Mini Research Harness</h1>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-1">
          <ProjectSidebar projects={mockProjects} />
        </div>
        <div className="lg:col-span-3 space-y-4">
          <TaskInputPanel />
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
            <GeneratedPlanPanel steps={mockPlanSteps} />
            <AgentExecutionLogPanel runs={mockRuns} />
          </div>
        </div>
      </div>
    </main>
  );
}
