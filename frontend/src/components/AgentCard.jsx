export default function AgentCard({ title, role, badges, lists = [], text = [] }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5">
      <header className="mb-3">
        <h3 className="font-serif text-xl text-navy-900">{title}</h3>
        <p className="text-xs text-slate-500">{role}</p>
      </header>
      {badges && <div className="mb-4 flex flex-wrap gap-2">{badges}</div>}
      {text.map((t) => (
        <div key={t.label} className="mb-3">
          <h4 className="text-xs font-semibold text-slate-500">{t.label}</h4>
          <p className="text-sm leading-relaxed">{t.value}</p>
        </div>
      ))}
      {lists.map((l) => (
        <div key={l.label} className="mb-3">
          <h4 className="text-xs font-semibold text-slate-500">{l.label}</h4>
          {l.items?.length ? (
            <ul className="mt-1 list-disc space-y-1 pl-5 text-sm">{l.items.map((i, k) => <li key={k}>{i}</li>)}</ul>
          ) : (
            <p className="text-sm text-slate-400">None reported</p>
          )}
        </div>
      ))}
    </section>
  );
}
