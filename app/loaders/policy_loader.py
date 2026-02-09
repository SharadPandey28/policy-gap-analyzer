from pypdf import PdfReader


def load_policy_text(filepath):

    if filepath.lower().endswith(".txt"):
        return open(filepath, encoding="utf-8").read()

    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        text = ""
        for p in reader.pages:
            text += p.extract_text() + "\n"
        return text

    raise ValueError("Only .txt or .pdf supported")
