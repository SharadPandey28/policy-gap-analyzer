import re

MIN_SEGMENT_LENGTH = 25


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def segment_policy(text):

    parts = re.split(r"[.!?]\s+", text)

    segments = []

    for i, seg in enumerate(parts):
        if len(seg) < MIN_SEGMENT_LENGTH:
            continue

        segments.append({
            "id": i,
            "text": seg,
            "normalized": normalize_text(seg)
        })

    return segments
