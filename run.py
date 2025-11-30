# run.py
import sys
from src.orchestrator.orchestrator import Orchestrator

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py 'Analyze ROAS drop'")
        sys.exit(1)
    query = sys.argv[1]
    orchestrator = Orchestrator()
    report = orchestrator.run(query)
    print("Report generated. Check reports/insights.json, creatives.json, report.md and logs/")

if __name__ == "__main__":
    main()
