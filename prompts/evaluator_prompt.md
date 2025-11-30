Evaluator Agent Prompt (structured):

Input: hypothesis + data_summary
Task: Quantitatively validate hypothesis using statistical checks or simple thresholds.
Output JSON:
{
 "hypothesis_id":"h1",
 "validated": true/false,
 "confidence": 0.0-1.0,
 "evidence": {"metric": "CTR", "before":x, "after":y, "delta_pct":z}
}
