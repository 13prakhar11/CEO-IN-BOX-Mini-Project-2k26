function Col({ title, ex }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5">
      <h3 className="font-serif text-lg text-navy-900">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed">{ex?.final_board_resolution}</p>
      <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-slate-600">
        {ex?.critical_actions?.map((a, i) => <li key={i}>{a}</li>)}
      </ol>
    </div>
  );
}

export default function Compare({ before, after }) {
  return (
    <section>
      <h2 className="mb-2 font-serif text-xl text-navy-900">Decision change after crisis</h2>
      <div className="grid gap-4 md:grid-cols-2">
        <Col title="Before" ex={before?.executive_decision} />
        <Col title="After" ex={after?.executive_decision} />
      </div>
    </section>
  );
}
