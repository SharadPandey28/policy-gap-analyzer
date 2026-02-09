from app.nlp.matching import score, classify


def generate_gap_report(clauses, segments):

    report = []

    for c in clauses:

        best_score = 0
        best_text = ""

        for seg in segments:
            s = score(c, seg["normalized"])

            if s > best_score:
                best_score = s
                best_text = seg["text"]

        report.append({
            "clause_id": c.get("clause_id") or c.get("id"),
            "title": c.get("title") or c.get("control"),
            "coverage": classify(best_score),
            "score": round(best_score, 2),
            "matched_text": best_text
        })

    return report
