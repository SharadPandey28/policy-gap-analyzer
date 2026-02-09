from app.nlp.preprocessing import normalize_text


def preprocess_clauses(clauses):

    processed = []

    for c in clauses:

        # support multiple field names safely
        text = (
            c.get("requirement_text")
            or c.get("control")
            or c.get("description")
            or ""
        )

        processed.append({
            **c,
            "normalized_requirement": normalize_text(text),
            "normalized_keywords": [
                normalize_text(k) for k in c.get("keywords", [])
            ]
        })

    return processed
