import { useState } from "react";
import { api } from "../api";
import { SAMPLES } from "../samples";
import Loader from "./Loader";
import ResultView from "./ResultView";
import Compare from "./Compare";

const newId = () => `session_${Date.now().toString(36)}`;

export default function Dashboard({ onUnauth }) {
  const [form, setForm] = useState({ scenario: "", crisis: "", user_query: "", session_id: newId() });
  const [result, setResult] = useState(null);
  const [previous, setPrevious] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [rerun, setRerun] = useState(false);
  const [newCrisis, setNewCrisis] = useState("");

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const run = async (payload, isRerun = false) => {
    setLoading(true); setError("");
    try {
      const data = await api.run(payload);
      setPrevious(isRerun ? result : null);
      setResult(data);
      setRerun(false);
    } catch (err) {
      if (err.status === 401) onUnauth();
      else setError(err.message);
    } finally { setLoading(false); }
  };

  const submit = (e) => { e.preventDefault(); run(form); };
  const submitRerun = (e) => {
    e.preventDefault();
    setForm({ ...form, crisis: newCrisis });
    run({ ...form, crisis: newCrisis }, true);
  };

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <header>
        <h1 className="font-serif text-3xl text-navy-900">Run the board</h1>
        <p className="text-sm text-slate-500">Describe a business situation. Four specialists report, the CEO decides, an auditor checks the work.</p>
      </header>

      <form onSubmit={submit} className="space-y-4 rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-slate-500">Try a sample:</span>
          {SAMPLES.map((s) => (
            <button type="button" key={s.label} className="btn btn-ghost !py-1 text-xs"
              onClick={() => setForm({ ...form, scenario: s.scenario, crisis: s.crisis, user_query: s.user_query })}>
              {s.label}
            </button>
          ))}
        </div>
        <div>
          <label htmlFor="scenario" className="mb-1 block text-sm font-medium">Business scenario</label>
          <textarea id="scenario" rows={3} required className="field" value={form.scenario} onChange={set("scenario")} />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label htmlFor="crisis" className="mb-1 block text-sm font-medium">Crisis event (optional)</label>
            <textarea id="crisis" rows={2} className="field" value={form.crisis} onChange={set("crisis")} />
          </div>
          <div>
            <label htmlFor="q" className="mb-1 block text-sm font-medium">Board question (optional)</label>
            <textarea id="q" rows={2} className="field" value={form.user_query} onChange={set("user_query")} />
          </div>
        </div>
        <div className="flex flex-wrap items-end gap-4">
          <div className="w-full sm:w-64">
            <label htmlFor="sid" className="mb-1 block text-sm font-medium">Session ID</label>
            <input id="sid" className="field" value={form.session_id} onChange={set("session_id")} />
          </div>
          <button className="btn btn-primary" disabled={loading}>{loading ? "Running..." : "Run analysis"}</button>
        </div>
      </form>

      {error && <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-800">{error}</p>}
      {loading && <Loader />}

      {result && !loading && (
        <>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-slate-500">Session {result.session_id}, completed in {result.elapsed}s</p>
            <button className="btn btn-ghost" onClick={() => setRerun(!rerun)}>Inject crisis and re-run</button>
          </div>

          {rerun && (
            <form onSubmit={submitRerun} className="space-y-3 rounded-lg border border-amber-300 bg-amber-50 p-4">
              <label htmlFor="nc" className="block text-sm font-medium">New crisis event</label>
              <textarea id="nc" rows={2} required className="field" value={newCrisis} onChange={(e) => setNewCrisis(e.target.value)} />
              <button className="btn btn-primary">Re-run with this crisis</button>
            </form>
          )}

          {previous && <Compare before={previous} after={result} />}
          <ResultView data={result} />
        </>
      )}
    </div>
  );
}
