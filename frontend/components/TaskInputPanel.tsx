type TaskInputPanelProps = {
  createProjectLabel: string;
  description: string;
  descriptionLabel: string;
  descriptionPlaceholder: string;
  isBusy: boolean;
  name: string;
  nameLabel: string;
  namePlaceholder: string;
  onCreateProject: () => void;
  onDescriptionChange: (value: string) => void;
  onNameChange: (value: string) => void;
};

export function TaskInputPanel({
  createProjectLabel,
  description,
  descriptionLabel,
  descriptionPlaceholder,
  isBusy,
  name,
  nameLabel,
  namePlaceholder,
  onCreateProject,
  onDescriptionChange,
  onNameChange,
}: TaskInputPanelProps) {
  return (
    <section className="border-b border-slate-200 bg-white p-4">
      <div className="grid gap-3 lg:grid-cols-[280px_1fr_auto] lg:items-end">
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-slate-700">{nameLabel}</span>
          <input
            className="w-full rounded border border-slate-300 px-3 py-2"
            onChange={(event) => onNameChange(event.target.value)}
            placeholder={namePlaceholder}
            value={name}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-slate-700">{descriptionLabel}</span>
          <textarea
            className="h-20 w-full resize-none rounded border border-slate-300 px-3 py-2"
            onChange={(event) => onDescriptionChange(event.target.value)}
            placeholder={descriptionPlaceholder}
            value={description}
          />
        </label>
        <button
          className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          disabled={isBusy || !name.trim()}
          onClick={onCreateProject}
          type="button"
        >
          {createProjectLabel}
        </button>
      </div>
    </section>
  );
}
