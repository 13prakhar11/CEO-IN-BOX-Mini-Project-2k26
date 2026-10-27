const GOOD = ["stable", "optimal", "low", "passed"];
const WARN = ["at risk", "strained", "medium"];
const BAD = ["critical", "severe", "high", "needs_revision"];

const TONES = {
  good: "bg-emerald-50 text-emerald-800 ring-emerald-600/30",
  warn: "bg-amber-50 text-amber-800 ring-amber-600/30",
  bad: "bg-red-50 text-red-800 ring-red-600/30",
  neutral: "bg-slate-100 text-slate-700 ring-slate-500/20",
};

// demand=true flips the scale: High demand is good news, Low is bad.
export default function StatusBadge({ label, value, demand = false }) {
  const v = String(value ?? "").toLowerCase();
  let tone = "neutral";
  if (demand) tone = v === "high" ? "good" : v === "medium" ? "warn" : v === "low" ? "bad" : "neutral";
  else if (GOOD.includes(v)) tone = "good";
  else if (WARN.includes(v)) tone = "warn";
  else if (BAD.includes(v)) tone = "bad";
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${TONES[tone]}`}>
      {label && <span className="text-slate-500">{label}:</span>}
      {value ?? "n/a"}
    </span>
  );
}
