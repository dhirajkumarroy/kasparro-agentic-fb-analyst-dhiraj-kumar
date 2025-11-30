# 🧠 Kasparro Agentic Facebook Analyst — Dhiraj Kumar

** A fully functional, multi-agent system that diagnoses Facebook Ads performance, explains ROAS fluctuations, validates insights quantitatively, and generates improved creative directions — completely autonomous and reproducible. ** 

This project follows Kasparro’s required structure, prompt design, reasoning workflow, and output standards.

---

### 🚀 Quick Start

1️⃣ Create virtual environment
-> python -m venv .venv
-> source .venv/bin/activate

2️⃣ Install dependencies
-> pip install -r requirements.txt

3️⃣ Run the Agentic System
-> python run.py "Analyze ROAS drop"

### 4️⃣ View results
Outputs are generated automatically in the `reports/` folder:

* **reports/insights.json** (Generated hypotheses)
* **reports/evaluations.json** (Confidence scores)
* **reports/creatives.json** (New ad copy)
* **reports/report.md** (Final summary)

Logs are available at:
* **logs/run_log.json**

## 📁 Project Structure

```
* ** kasparro-agentic-fb-analyst-dhiraj/**
├── README.md
├── requirements.txt
├── run.py
├── config/
│   └── config.yaml
├── data/
│   ├── sample_ads.csv
│   └── data_README.md
├── prompts/
│   ├── planner_prompt.md
│   ├── insight_prompt.md
│   ├── evaluator_prompt.md
│   └── creative_prompt.md
├── src/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator_agent.py
│   │   └── creative_agent.py
│   ├── orchestrator/
│   │   └── orchestrator.py
│   └── utils/
│       ├── logger.py
│       └── schemas.py
├── reports/
│   ├── insights.json
│   ├── evaluations.json
│   ├── creatives.json
│   └── report.md
├── logs/
│   └── run_log.json
└── tests/
    └── test_evaluator.py

```
## 🧩 Architecture Overview

```
Agent Flow Diagram (Mermaid)
flowchart TD

A[User Query] --> B[Planner Agent]
B --> C[Data Agent]
C --> D[Insight Agent]
D --> E[Evaluator Agent]
C --> F[Creative Agent]
E --> G[Final Report]
F --> G

```
## 🧠 Agent Responsibilities

1. Planner Agent
Breaks user query into structured tasks

  . Defines retry logic

  . Orchestrates agent order

2. Data Agent
  . Loads + cleans dataset

  . Produces:

    . Time series summary

    . Creative-level summary

    . Audience performance summary

  . Returns structured Python dicts

3. Insight Agent
  . Creates hypotheses using:

    . ROAS trends

    . CTR shifts

    . Weak creatives

    . Audience fatigue

  . Outputs structured hypothesis JSON

4. Evaluator Agent
  . Quantitatively tests hypotheses

  . Uses thresholds & simple statistical checks

  Outputs:

    . validated = True/False

    . confidence = 0–1

    . evidence struct

5. Creative Improvement Agent
  . Identifies low CTR creatives

  . Generates 3–5 alternative headlines, bodies, CTAs

  . Mirrors messaging tone & audience targeting context

## 📊 Example Output Files
✔ insights.json
Generated hypotheses:
[
  {
    "id": "h_roas_drop",
    "text": "ROAS dropped by 25%...",
    "confidence_prior": 0.75
  }
]

✔ evaluations.json
Evaluator confidence scores:
[
  {
    "hypothesis_id": "h_roas_drop",
    "validated": true,
    "confidence": 0.78,
    "evidence": { "drop_pct": 0.25 }
  }
]

✔ creatives.json
Generated improved creatives:
[
  {
    "campaign": "Holiday Sale - Global",
    "original": "Save 30% on everything",
    "recommendations": [
      { "headline": "Limited time: Save 30% on everything", "cta": "Shop now" }
    ]
  }
]

✔ report.md
Human-friendly summary:

# Kasparro Agentic FB Analyst — Report

Query: Analyze ROAS drop
Hypothesis: ROAS declined due to creative fatigue...
Validated with 82% confidence.
Creative Ideas Generated...


⚙️ Configuration
All settings live in config/config.yaml:
seed: 42
thresholds:
  low_ctr: 0.02
  roas_drop_pct: 0.10
output:
  reports_dir: "reports"
  logs_dir: "logs"

🔬 Testing
Run the included evaluator test:
-> pytest -q


## 📝 Design Decisions & Reasoning
Reproducibility
  . All agents rule-based → deterministic

  . Randomness seeded in config

Separation of Concerns
Each agent handles one responsibility for clarity & debugging.

Reflective & Structured Prompts
All prompts are stored in /prompts/ following Kasparro’s guidelines:

  . JSON schemas

  . Think → Analyze → Conclude steps

  . Retry logic built in

Observability
  . Every agent step is logged in run_log.json

  . Traces map exactly to planner’s task order


## 🙌 Author
Dhiraj Kumar
Applied AI Engineer — Agentic Analytics