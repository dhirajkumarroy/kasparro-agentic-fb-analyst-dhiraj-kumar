# src/utils/schemas.py
# JSON schemas (simple python dicts) used for guidance; not enforced
INSIGHT_SCHEMA = {
    "hypotheses": [
        {"id": "h1", "text": "", "confidence_prior": 0.5, "evidence_summary": ""}
    ],
    "next_steps": []
}

EVALUATION_SCHEMA = {
    "hypothesis_id": "",
    "validated": False,
    "confidence": 0.0,
    "evidence": {}
}

CREATIVE_SCHEMA = {
    "campaign": "",
    "adset": "",
    "original": "",
    "recommendations": [
        {"headline": "", "body": "", "cta": ""}
    ]
}
