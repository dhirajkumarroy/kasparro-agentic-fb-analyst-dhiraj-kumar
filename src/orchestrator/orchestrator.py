# src/orchestrator/orchestrator.py
import json
import os
from pathlib import Path
import yaml

from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.utils.logger import SimpleLogger

class Orchestrator:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)
        outdir = self.cfg["output"]["reports_dir"]
        logfile = os.path.join(self.cfg["output"]["logs_dir"], "run_log.json")
        Path(self.cfg["output"]["reports_dir"]).mkdir(parents=True, exist_ok=True)
        Path(self.cfg["output"]["logs_dir"]).mkdir(parents=True, exist_ok=True)

        self.logger = SimpleLogger(logfile)
        self.planner = PlannerAgent()
        self.data_agent = DataAgent(config_path)
        self.insight_agent = InsightAgent(self.cfg.get("thresholds", {}))
        self.evaluator = EvaluatorAgent(self.cfg.get("thresholds", {}))
        self.creative_agent = CreativeAgent(config_path)
        self.reports_dir = outdir

    def run(self, query: str):
        plan = self.planner.plan(query)
        self.logger.log("planner", plan)

        # load data
        df = self.data_agent.load_data()
        summary = self.data_agent.summarize(df)
        # persist a small summary (not full CSV)
        self.logger.log("data_summary_keys", list(summary.keys()))

        # generate insights (hypotheses)
        hypotheses = self.insight_agent.generate_hypotheses(summary)
        self.logger.log("hypotheses_raw", hypotheses)

        # evaluate each hypothesis
        evaluations = []
        validated = []
        for h in hypotheses:
            ev = self.evaluator.evaluate(h, summary)
            evaluations.append(ev)
            # add to validated list if validated
            if ev.get("validated"):
                validated.append(ev)
            self.logger.log("evaluation", ev)

        # generate creatives for low CTR
        creatives = self.creative_agent.generate(summary)
        self.logger.log("creatives", creatives)

        # compile report
        report = {
            "query": query,
            "hypotheses": hypotheses,
            "evaluations": evaluations,
            "validated": validated,
            "creatives": creatives
        }

        # write outputs
        reports_dir = self.reports_dir
        with open(os.path.join(reports_dir, "insights.json"), "w") as f:
            json.dump(hypotheses, f, indent=2)
        with open(os.path.join(reports_dir, "evaluations.json"), "w") as f:
            json.dump(evaluations, f, indent=2)
        with open(os.path.join(reports_dir, "creatives.json"), "w") as f:
            json.dump(creatives, f, indent=2)
        # human readable report
        report_md = self._render_markdown(report)
        with open(os.path.join(reports_dir, "report.md"), "w") as f:
            f.write(report_md)

        self.logger.log("final_report_written", {"reports_dir": reports_dir})
        return report

    def _render_markdown(self, report: dict) -> str:
        md = ["# Kasparro Agentic FB Analyst — Report\n"]
        md.append(f"**Query:** {report.get('query')}\n\n")
        md.append("## Hypotheses\n")
        for h in report["hypotheses"]:
            md.append(f"- **{h['id']}**: {h['text']} (prior={h.get('confidence_prior',0):.2f})\n")
            md.append(f"  - Evidence: {h.get('evidence_summary')}\n")
        md.append("\n## Evaluations\n")
        for e in report["evaluations"]:
            md.append(f"- **{e['hypothesis_id']}** — validated: {e['validated']}, confidence: {e['confidence']:.2f}\n")
            md.append(f"  - Evidence: {e['evidence']}\n")
        md.append("\n## Creative Suggestions\n")
        for c in report["creatives"]:
            md.append(f"### Campaign: {c['campaign']} | Adset: {c['adset']}\n")
            md.append(f"- Original: {c['original']}\n")
            for r in c["recommendations"]:
                md.append(f"  - Headline: {r['headline']}\n")
                md.append(f"    Body: {r['body']}\n")
                md.append(f"    CTA: {r['cta']}\n")
            md.append("\n")
        return "\n".join(md)
