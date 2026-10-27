import { useEffect, useState } from "react";
import { api } from "../api";
import ResultView from "./ResultView";

export default function History({ onUnauth }) {
  const [sessions, setSessions] = useState(null);
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState("");

  const handle = (err) => (err.status === 401 ? onUnauth() : setError(err.message));

  useEffect(() => { api.sessions().then((d) => setSessions(d.sessions)).catch(handle); }, []);

  const open = (id) => { setError(""); api.session(id).then(setDetail).catch(handle); };

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <h1 className="font-serif text-3xl text-navy-900">Past sessions</h1>
      {error && <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-800">{error}</p>}

      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr><th className="px-4 py-3 font-medium">Session ID</th><th className="px-4 py-3 font-medium">Checkpoints</th><th /></tr>
          </thead>
          <tbody>
            {sessions === null && <tr><td className="px-4 py-3" colSpan={3}>Loading...</td></tr>}
            {sessions?.length === 0 && <tr><td className="px-4 py-3" colSpan={3}>No sessions yet. Run an analysis from the dashboard.</td></tr>}
            {sessions?.map((s) => (
              <tr key={s.thread_id} className="border-t border-slate-100">
                <td className="px-4 py-3">{s.thread_id}</td>
                <td className="px-4 py-3">{s.checkpoints}</td>
                <td className="px-4 py-3 text-right"><button className="btn btn-ghost !py-1" onClick={() => open(s.thread_id)}>View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {detail && (
        <>
          <section className="rounded-lg border border-slate-200 bg-white p-5 text-sm">
            <h2 className="mb-2 font-serif text-xl text-navy-900">{detail.thread_id}</h2>
            <p><b>Scenario:</b> {detail.inputs.scenario}</p>
            {detail.inputs.crisis && <p><b>Crisis:</b> {detail.inputs.crisis}</p>}
            {detail.inputs.user_query && <p><b>Board question:</b> {detail.inputs.user_query}</p>}
          </section>
          <ResultView data={detail.result} />
        </>
      )}
    </div>
  );
}
