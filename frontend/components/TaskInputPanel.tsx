export function TaskInputPanel() {
  return (
    <section className="bg-white rounded-lg p-4 shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold mb-3">Task Input</h2>
      <textarea
        className="w-full min-h-36 p-3 rounded border border-slate-300"
        placeholder="Describe your research or coding task..."
      />
      <button className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Generate Plan
      </button>
    </section>
  );
}
