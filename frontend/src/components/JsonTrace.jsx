export default function JsonTrace({ items }) {
  return (
    <div className="divide-y divide-slate-200 rounded-lg border border-slate-200 bg-white">
      {items.map(({ name, data }) => (
        <details key={name} className="group">
          <summary className="flex cursor-pointer items-center justify-between px-4 py-3 text-sm font-medium hover:bg-slate-50">
            {name}
            <span className="text-slate-400 transition-transform group-open:rotate-90" aria-hidden="true">&#9656;</span>
          </summary>
          <pre className="overflow-x-auto bg-navy-900 px-4 py-3 text-xs leading-relaxed text-slate-100">
            {JSON.stringify(data, null, 2)}
          </pre>
        </details>
      ))}
    </div>
  );
}
