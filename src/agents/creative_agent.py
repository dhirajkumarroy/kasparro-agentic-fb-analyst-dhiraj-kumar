# src/agents/creative_agent.py
from typing import List, Dict
import yaml
import os
import random

class CreativeAgent:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)
        random.seed(self.cfg.get("seed", 42))
        self.low_ctr_threshold = self.cfg.get("thresholds", {}).get("low_ctr", 0.02)

    def find_low_ctr(self, data_summary: dict):
        creative = data_summary["creative_summary"]
        low = creative[creative["ctr"] < self.low_ctr_threshold]
        items = []
        for _, row in low.iterrows():
            items.append({
                "campaign": row["campaign_name"],
                "adset": row["adset_name"],
                "creative_type": row["creative_type"],
                "creative_message": row["creative_message"],
                "ctr": float(row["ctr"]),
                "impressions": int(row["impressions"])
            })
        return items

    def generate_for_item(self, item: dict) -> Dict:
        """
        Rule-based lightweight creative generation.
        Produces headline, body, CTA.
        """
        orig = item.get("creative_message","")
        # simple transformations and variations
        suggestions = []
        ctype = item.get("creative_type","")
        # base patterns
        patterns = [
            ("Limited time: {orig}", "Hurry — only a few left", "Shop now"),
            ("New & Improved: {orig}", "See what customers love", "Learn more"),
            ("Just dropped — {orig}", "Don't miss the special price today", "Buy now"),
            ("Hot pick: {orig}", "Trending with buyers like you", "Shop deals"),
            ("Save more: {orig}", "Bundle & save — limited offer", "Get offer")
        ]
        # pick up to 4 suggestions
        for head_tpl, body_tpl, cta in random.sample(patterns, k=min(4, len(patterns))):
            headline = head_tpl.format(orig=orig if len(orig) < 60 else orig[:57] + "...")
            body = body_tpl
            suggestions.append({"headline": headline, "body": body, "cta": cta})
        return {
            "campaign": item["campaign"],
            "adset": item["adset"],
            "creative_type": ctype,
            "original": orig,
            "recommendations": suggestions,
            "ctr": item.get("ctr"),
            "impressions": item.get("impressions")
        }

    def generate(self, data_summary: dict) -> List[Dict]:
        items = self.find_low_ctr(data_summary)
        results = [self.generate_for_item(i) for i in items]
        return results
