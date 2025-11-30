# src/agents/evaluator_agent.py
import numpy as np
from typing import Dict, Any
from scipy.stats import ttest_ind

class EvaluatorAgent:
    def __init__(self, cfg=None):
        self.cfg = cfg or {}

    def evaluate(self, hypothesis: Dict[str, Any], data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single hypothesis using numeric checks.
        Returns an evaluation dict with confidence and evidence.
        """
        hid = hypothesis.get("id")
        result = {
            "hypothesis_id": hid,
            "validated": False,
            "confidence": 0.0,
            "evidence": {}
        }

        # Simple validators based on hypothesis id patterns
        if hid == "h_roas_drop":
            ts = data_summary["timeseries"]
            if len(ts) >= 2:
                prev = ts.iloc[-2]
                last = ts.iloc[-1]
                prev_roas = prev["roas"] if prev["roas"] and not np.isnan(prev["roas"]) else 1e-9
                drop = (prev_roas - last["roas"]) / prev_roas
                conf = min(1.0, float(max(0.0, drop)))
                result["validated"] = drop > self.cfg.get("roas_drop_pct", 0.1)
                result["confidence"] = conf
                result["evidence"] = {"roas_prev": float(prev["roas"]), "roas_last": float(last["roas"]), "drop_pct": float(drop)}
            else:
                result["confidence"] = 0.1
                result["evidence"] = {"reason": "insufficient timepoints"}

        elif str(hid).startswith("h_lowctr"):
            # parse creative_summary, check CTR
            creative = data_summary["creative_summary"]
            # find creative message fragment in text
            text = hypothesis.get("text","")
            # attempt to extract the creative fragment from the text
            # fallback: validate by checking min ctr
            if "low CTR" in hypothesis.get("text","").lower() or "lowctr" in hid:
                # use heuristic: if any creative has ctr < threshold then validate
                low_ctr_threshold = self.cfg.get("low_ctr", 0.02)
                low = creative[creative["ctr"] < low_ctr_threshold]
                validated = not low.empty
                # confidence scaled by relative drop
                if validated:
                    # compute average ctr of low creatives
                    avg_low = low["ctr"].mean()
                    conf = min(1.0, (low_ctr_threshold - avg_low) / (low_ctr_threshold + 1e-9) + 0.5)
                else:
                    conf = 0.2
                result["validated"] = validated
                result["confidence"] = float(conf)
                result["evidence"] = {
                    "low_count": int(len(low)),
                    "threshold": low_ctr_threshold,
                    "examples": low.head(3).to_dict(orient="records")
                }

        elif hid == "h_audience_underperform":
            aud = data_summary["audience_summary"]
            # check worst audience vs median
            if not aud.empty:
                median_ctr = aud["ctr"].median()
                worst = aud.sort_values("ctr").iloc[0]
                validated = (worst["ctr"] < 0.6 * median_ctr) if (median_ctr and not np.isnan(median_ctr)) else False
                conf = 0.5 + max(0, (median_ctr - worst["ctr"]) / (median_ctr + 1e-9)) * 0.5
                result["validated"] = validated
                result["confidence"] = float(min(1.0, conf))
                result["evidence"] = {"worst_audience": worst["audience_type"], "worst_ctr": float(worst["ctr"]), "median_ctr": float(median_ctr)}
            else:
                result["confidence"] = 0.1
                result["evidence"] = {"reason":"no audience data"}

        else:
            result["validated"] = False
            result["confidence"] = 0.2
            result["evidence"] = {"reason":"no validator matched"}

        return result
