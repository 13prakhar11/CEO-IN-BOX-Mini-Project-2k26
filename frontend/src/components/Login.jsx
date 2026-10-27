import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Login({ onLogin }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setError("");
    try { await api.login(form.username, form.password); onLogin(); nav("/"); }
    catch (err) { setError(err.message); }
    finally { setBusy(false); }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-navy-900 p-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-lg bg-white p-6">
        <h1 className="font-serif text-2xl text-navy-900">AutoCEO boardroom</h1>
        <p className="mb-5 text-sm text-slate-500">Sign in to run the board.</p>
        <label className="mb-1 block text-sm font-medium" htmlFor="u">Username</label>
        <input id="u" className="field mb-3" autoComplete="username" required
          value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <label className="mb-1 block text-sm font-medium" htmlFor="p">Password</label>
        <input id="p" type="password" className="field mb-4" autoComplete="current-password" required
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        {error && <p role="alert" className="mb-3 text-sm text-red-700">{error}</p>}
        <button className="btn btn-primary w-full" disabled={busy}>{busy ? "Signing in..." : "Sign in"}</button>
      </form>
    </div>
  );
}
