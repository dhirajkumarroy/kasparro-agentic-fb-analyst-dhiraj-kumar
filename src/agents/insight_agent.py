# src/agents/insight_agent.py
import numpy as np
import pandas as pd
from typing import List, Dict
from scipy.stats import ttest_ind

class InsightAgent:
    def __init__(self, cfg=None):
        self.cfg = cfg or {}

    def generate_hypotheses(self, data_summary: dict) -> List[Dict]:
        """
        Simple rule-based hypothesis generation using the provided summaries.
        Returns a list of hypothesis dicts with a prior confidence and text.
        """
        ts = data_summary["timeseries"]
        creative = data_summary["creative_summary"]
        audience = data_summary["audience_summary"]

        hypotheses = []

        # 1) Check for ROAS drop over last two available dates
        if len(ts) >= 2:
            last = ts.iloc[-1]
            prev = ts.iloc[-2]
            # avoid division by zero
            prev_roas = prev["roas"] if prev["roas"] and not np.isnan(prev["roas"]) else 1e-9
            if prev_roas > 0:
                roas_drop = (prev["roas"] - last["roas"]) / prev_roas
                if roas_drop > self.cfg.get("roas_drop_pct", 0.1):
                    hypotheses.append({
                        "id": "h_roas_drop",
                        "text": f"ROAS dropped by {roas_drop:.2%} from {prev['roas']:.2f} to {last['roas']:.2f}. Possible causes: creative performance or audience fatigue.",
                        "confidence_prior": min(0.9, roas_drop),
                        "evidence_summary": f"roas_prev={prev['roas']:.2f}, roas_last={last['roas']:.2f}, drop={roas_drop:.2f}"
                    })

        # 2) Low CTR creatives
        low_ctr_threshold = self.cfg.get("low_ctr", 0.02)
        low_ctr = creative[creative["ctr"] < low_ctr_threshold]
        for _, row in low_ctr.iterrows():
            hypotheses.append({
                "id": f"h_lowctr_{_}",
                "text": f"Creative '{row['creative_message'][:60]}' (type={row['creative_type']}) has low CTR={row['ctr']:.4f}. This may explain lower conversions.",
                "confidence_prior": 0.6,
                "evidence_summary": f"creative_ctr={row['ctr']:.4f}, impressions={int(row['impressions'])}"
            })

        # 3) Audience shift: significant reduction in clicks for specific audience
        # simple rule: audience CTR decreased
        aud = audience.copy()
        aud = aud.sort_values("ctr")
        if len(aud) >= 2:
            # if worst audience ctr is below median by sizable margin
            median_ctr = aud["ctr"].median()
            worst = aud.iloc[0]
            if not np.isnan(median_ctr) and not np.isnan(worst["ctr"]) and worst["ctr"] < 0.6 * median_ctr:
                hypotheses.append({
                    "id": "h_audience_underperform",
                    "text": f"Audience '{worst['audience_type']}' underperforms (ctr={worst['ctr']:.4f}) vs median {median_ctr:.4f}.",
                    "confidence_prior": 0.5,
                    "evidence_summary": f"audience_ctr={worst['ctr']:.4f}, median_ctr={median_ctr:.4f}"
                })

        if not hypotheses:
            hypotheses.append({
                "id": "h_none",
                "text": "No obvious signal from quick heuristics. Recommend deeper analysis.",
                "confidence_prior": 0.3,
                "evidence_summary": "no heuristics triggered"
            })

        return hypotheses
