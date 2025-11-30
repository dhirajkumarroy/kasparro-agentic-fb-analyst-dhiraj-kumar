Creative Agent Prompt (structured):

Input: list of low CTR creatives with their messages and context (audience_type, creative_type)
Task: Generate 3-6 alternative creative messages per creative, including headline, body, CTA
Output JSON:
{
 "campaign": "...",
 "adset": "...",
 "original": "...",
 "recommendations":[{"headline":"...","body":"...","cta":"..."}]
}
