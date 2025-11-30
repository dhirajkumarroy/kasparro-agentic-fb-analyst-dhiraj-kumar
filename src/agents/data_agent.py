# src/agents/data_agent.py
import pandas as pd
import numpy as np
from datetime import timedelta
import yaml
import os

class DataAgent:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)
        self.data_path = self.cfg["data_path"]
        np.random.seed(self.cfg.get("seed", 42))

    def load_data(self):
        df = pd.read_csv(self.data_path, parse_dates=["date"])
        # Basic cleaning
        df["ctr"] = pd.to_numeric(df["ctr"], errors="coerce")
        df["spend"] = pd.to_numeric(df["spend"], errors="coerce")
        df["impressions"] = pd.to_numeric(df["impressions"], errors="coerce").fillna(0).astype(int)
        df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce").fillna(0).astype(int)
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
        df["purchases"] = pd.to_numeric(df["purchases"], errors="coerce").fillna(0).astype(int)
        df["roas"] = pd.to_numeric(df["roas"], errors="coerce").fillna(0.0)
        return df

    def summarize(self, df):
        # Global time series aggregation
        ts = df.groupby("date").agg({
            "spend": "sum",
            "impressions": "sum",
            "clicks": "sum",
            "revenue": "sum",
            "purchases": "sum"
        }).reset_index()
        ts["ctr"] = ts["clicks"] / ts["impressions"].replace(0, pd.NA)
        ts["roas"] = ts["revenue"] / ts["spend"].replace(0, pd.NA)

        # Creative-level summary
        creative = df.groupby(["campaign_name", "adset_name", "creative_type", "creative_message"]).agg({
            "spend":"sum","impressions":"sum","clicks":"sum","revenue":"sum","purchases":"sum"
        }).reset_index()
        creative["ctr"] = creative["clicks"] / creative["impressions"].replace(0, pd.NA)
        creative["roas"] = creative["revenue"] / creative["spend"].replace(0, pd.NA)

        # Audience summary
        audience = df.groupby(["audience_type"]).agg({
            "spend":"sum","impressions":"sum","clicks":"sum","revenue":"sum","purchases":"sum"
        }).reset_index()
        audience["ctr"] = audience["clicks"] / audience["impressions"].replace(0, pd.NA)
        audience["roas"] = audience["revenue"] / audience["spend"].replace(0, pd.NA)

        return {
            "timeseries": ts,
            "creative_summary": creative,
            "audience_summary": audience,
            "raw": df
        }
