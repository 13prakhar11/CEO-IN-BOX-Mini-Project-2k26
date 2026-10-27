import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Layout({ onLogout }) {
  const nav = useNavigate();
  const link = ({ isActive }) =>
    `block rounded-md px-3 py-2 text-sm ${isActive ? "bg-navy-700 text-white" : "text-slate-300 hover:bg-navy-800"}`;

  const logout = async () => { await api.logout().catch(() => {}); onLogout(); nav("/login"); };

  return (
    <div className="min-h-screen md:flex">
      <aside className="bg-navy-900 p-4 md:w-60 md:shrink-0">
        <div className="mb-4 md:mb-8">
          <p className="font-serif text-xl text-white">AutoCEO</p>
          <p className="text-xs text-slate-400">Enterprise decision agent</p>
        </div>
        <nav className="flex gap-2 md:block md:space-y-1" aria-label="Main">
          <NavLink to="/" end className={link}>Dashboard</NavLink>
          <NavLink to="/history" className={link}>History</NavLink>
          <button onClick={logout} className="block w-full rounded-md px-3 py-2 text-left text-sm text-slate-300 hover:bg-navy-800">Log out</button>
        </nav>
      </aside>
      <main className="min-w-0 flex-1 p-4 md:p-8"><Outlet /></main>
    </div>
  );
}
