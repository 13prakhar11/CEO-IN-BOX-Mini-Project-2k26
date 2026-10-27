import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { api } from "./api";
import Layout from "./components/Layout";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import History from "./components/History";

export default function App() {
  const [auth, setAuth] = useState(null); // null = checking

  useEffect(() => { api.me().then(() => setAuth(true)).catch(() => setAuth(false)); }, []);

  if (auth === null) return <p className="p-8 text-sm text-slate-500">Loading...</p>;

  return (
    <Routes>
      <Route path="/login" element={auth ? <Navigate to="/" /> : <Login onLogin={() => setAuth(true)} />} />
      <Route element={auth ? <Layout onLogout={() => setAuth(false)} /> : <Navigate to="/login" />}>
        <Route path="/" element={<Dashboard onUnauth={() => setAuth(false)} />} />
        <Route path="/history" element={<History onUnauth={() => setAuth(false)} />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
