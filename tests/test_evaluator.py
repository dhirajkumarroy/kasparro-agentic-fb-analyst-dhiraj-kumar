# tests/test_evaluator.py
import pytest
import pandas as pd
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent

def test_roas_evaluation():
    da = DataAgent("config/config.yaml")
    df = da.load_data()
    summary = da.summarize(df)
    ia = InsightAgent({"roas_drop_pct": 0.05, "low_ctr": 0.02})
    hypotheses = ia.generate_hypotheses(summary)
    eva = EvaluatorAgent({"roas_drop_pct": 0.05, "low_ctr": 0.02})
    results = [eva.evaluate(h, summary) for h in hypotheses]
    assert isinstance(results, list)
    # at least one evaluation entry exists
    assert len(results) >= 1

if __name__ == "__main__":
    pytest.main([__file__])
