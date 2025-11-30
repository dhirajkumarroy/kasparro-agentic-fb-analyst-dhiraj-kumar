# src/agents/planner.py
import json
from typing import List
from pathlib import Path

class PlannerAgent:
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = Path(prompts_dir)

    def plan(self, query: str):
        """
        Break user query into tasks. Return a JSON-like plan.
        """
        plan = {
            "query": query,
            "tasks": [
                {"id": "load_data", "desc": "Load & clean dataset", "priority": 1},
                {"id": "summarize", "desc": "Aggregate time series & creative summaries", "priority": 2},
                {"id": "generate_insights", "desc": "Create hypotheses explaining changes", "priority": 3},
                {"id": "validate_insights", "desc": "Quantitatively validate hypotheses", "priority": 4},
                {"id": "generate_creatives", "desc": "Produce creatives for low CTR ads", "priority": 5},
                {"id": "compile_report", "desc": "Write marketer-friendly report and persist outputs", "priority": 6}
            ],
            "retry": {"max_attempts":2}
        }
        return plan
