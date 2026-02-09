import json
from app.loaders.policy_loader import load_policy_text
from app.llm.ollama_client import get_llm
from app.nlp.preprocessing import segment_policy
from app.nlp.clause_preprocessing import preprocess_clauses
from app.reporting.gap_report import generate_gap_report
from app.remediation.reviser import revise_policy


def analyze_policy(policy_path):

    llm = get_llm()

    with open("data/policy_clauses.json") as f:
        clauses = preprocess_clauses(json.load(f))

    policy_text = load_policy_text(policy_path)

    segments = segment_policy(policy_text)

    gap_report = generate_gap_report(clauses, segments)

    revised, roadmap = revise_policy(llm, policy_text, gap_report)

    return {
        "gap_report": gap_report,
        "gaps": [g for g in gap_report if g["coverage"] != "Covered"],
        "revised_policy": revised,
        "roadmap": roadmap
    }
