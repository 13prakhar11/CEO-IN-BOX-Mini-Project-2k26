import { useEffect, useState } from "react";

// The backend call is a single request, so progress is an estimate based on elapsed time.
const SPECIALISTS = ["Market", "Finance", "Operations", "Risk"];

export default function Loader() {
  const [t, setT] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setT((x) => x + 1), 1000);
    return () => clearInterval(id);
  }, []);
  const stage = t < 12 ? 0 : t < 22 ? 1 : 2;

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5" role="status" aria-live="polite">
      <p className="mb-4 text-sm text-slate-600">Running the board pipeline ({t}s). Estimated progress shown below.</p>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {SPECIALISTS.map((s, i) => (
          <Step key={s} name={s} state={stage > 0 ? "done" : "active"} delay={i * 150} />
        ))}
      </div>
      <div className="mt-3 grid grid-cols-2 gap-3">
        <Step name="Executive" state={stage === 1 ? "active" : stage > 1 ? "done" : "wait"} />
        <Step name="Auditor" state={stage === 2 ? "active" : "wait"} />
      </div>
    </div>
  );
}

function Step({ name, state, delay = 0 }) {
  const styles = {
    wait: "border-slate-200 text-slate-400",
    active: "border-teal-600 text-teal-700 animate-pulse",
    done: "border-emerald-600 bg-emerald-50 text-emerald-800",
  };
  return (
    <div className={`rounded-md border px-3 py-2 text-sm font-medium ${styles[state]}`} style={{ animationDelay: `${delay}ms` }}>
      {state === "done" ? "Done: " : state === "active" ? "Working: " : "Waiting: "}{name}
    </div>
  );
}
