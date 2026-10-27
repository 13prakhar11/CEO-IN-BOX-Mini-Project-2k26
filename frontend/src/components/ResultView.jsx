import AgentCard from "./AgentCard";
import StatusBadge from "./StatusBadge";
import ScoreGauge from "./ScoreGauge";
import JsonTrace from "./JsonTrace";

export default function ResultView({ data }) {
  const { market: m, finance: f, operations: o, risk: r, executive_decision: ex, evaluation_report: au } = data;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <AgentCard title="Market" role="Market analyst"
          badges={m && <><StatusBadge label="Demand" value={m.demand_direction} demand /><StatusBadge label="Confidence" value={m.confidence} /></>}
          text={m ? [{ label: "Trends", value: m.trend_summary }, { label: "Recommendation", value: m.recommendation }] : []} />
        <AgentCard title="Finance" role="Chief Financial Officer"
          badges={f && <><StatusBadge label="Health" value={f.financial_health} /><StatusBadge label="Safe budget" value={f.safe_budget_range} /></>}
          lists={f ? [{ label: "Budget flags", items: f.budget_flags }] : []}
          text={f ? [{ label: "Recommendation", value: f.recommendation }] : []} />
        <AgentCard title="Operations" role="Chief Operating Officer"
          badges={o && <StatusBadge label="Capacity" value={o.capacity_status} />}
          text={o ? [{ label: "Supply chain impact", value: o.supply_chain_impact }] : []}
          lists={o ? [{ label: "Operational risks", items: o.operational_risks }] : []} />
        <AgentCard title="Risk and compliance" role="Chief Compliance Officer"
          badges={r && <StatusBadge label="Risk level" value={r.overall_risk_level} />}
          lists={r ? [{ label: "Rule violations", items: r.rule_violations }] : []}
          text={r ? [{ label: "Mitigation", value: r.mitigation_strategy }, { label: "Recommendation", value: r.recommendation }] : []} />
      </div>

      {ex && (
        <section className="rounded-lg bg-navy-800 p-6 text-slate-100">
          <h2 className="font-serif text-2xl">Board resolution</h2>
          <p className="mt-3 text-sm leading-relaxed text-slate-300">{ex.strategic_synthesis}</p>
          <p className="mt-4 text-lg leading-snug">{ex.final_board_resolution}</p>
          <h3 className="mt-5 text-sm font-semibold text-slate-300">Critical actions</h3>
          <ol className="mt-2 list-decimal space-y-1.5 pl-5 text-sm">{ex.critical_actions?.map((a, i) => <li key={i}>{a}</li>)}</ol>
        </section>
      )}

      {au && (
        <section className="rounded-lg border border-slate-200 bg-white p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="font-serif text-xl text-navy-900">Auditor review</h2>
            <StatusBadge value={au.verdict} />
          </div>
          <div className="mt-4 flex flex-wrap gap-8">
            <ScoreGauge label="Faithfulness" value={au.faithfulness_score} />
            <ScoreGauge label="Conflict resolution" value={au.conflict_resolution_score} />
          </div>
          <p className="mt-4 text-sm leading-relaxed text-slate-600">{au.evaluation_summary}</p>
        </section>
      )}

      <div>
        <h2 className="mb-2 font-serif text-xl text-navy-900">Explainability trace</h2>
        <JsonTrace items={[
          { name: "Market agent", data: m }, { name: "Finance agent", data: f },
          { name: "Operations agent", data: o }, { name: "Risk agent", data: r },
          { name: "Executive agent", data: ex }, { name: "Auditor agent", data: au },
        ]} />
      </div>
    </div>
  );
}
