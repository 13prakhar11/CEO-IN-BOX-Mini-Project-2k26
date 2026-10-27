export default function ScoreGauge({ label, value = 0 }) {
  const pct = Math.max(0, Math.min(1, Number(value) || 0));
  const r = 34, c = 2 * Math.PI * r;
  const color = pct >= 0.8 ? "#059669" : pct >= 0.6 ? "#d97706" : "#dc2626";
  return (
    <div className="flex items-center gap-3" role="img" aria-label={`${label}: ${pct.toFixed(2)} out of 1`}>
      <svg width="84" height="84" viewBox="0 0 84 84">
        <circle cx="42" cy="42" r={r} fill="none" stroke="#e2e8f0" strokeWidth="8" />
        <circle cx="42" cy="42" r={r} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
          strokeDasharray={c} strokeDashoffset={c * (1 - pct)} transform="rotate(-90 42 42)"
          style={{ transition: "stroke-dashoffset .8s ease" }} />
        <text x="42" y="47" textAnchor="middle" className="fill-navy-900 text-[17px] font-semibold">{pct.toFixed(2)}</text>
      </svg>
      <span className="text-sm text-slate-600">{label}</span>
    </div>
  );
}
