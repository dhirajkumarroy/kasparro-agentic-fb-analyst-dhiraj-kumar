Insight Agent Prompt (structured):

Input: data_summary.json (aggregated metrics)
Task: Generate hypotheses explaining ROAS / CTR changes.
Output JSON:
{
  "hypotheses": [
    {"id":"h1","text":"...","confidence_prior":0.5,"evidence_summary":"..."}
  ],
  "next_steps": ["run_evaluator:h1", ...]
}
