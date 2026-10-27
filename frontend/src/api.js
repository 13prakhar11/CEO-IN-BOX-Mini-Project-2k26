async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.error || `Request failed (${res.status})`);
    err.status = res.status;
    throw err;
  }
  return data;
}

export const api = {
  me: () => request("/me"),
  login: (username, password) => request("/login", { method: "POST", body: JSON.stringify({ username, password }) }),
  logout: () => request("/logout", { method: "POST" }),
  run: (payload) => request("/run", { method: "POST", body: JSON.stringify(payload) }),
  sessions: () => request("/sessions"),
  session: (id) => request(`/sessions/${encodeURIComponent(id)}`),
};
