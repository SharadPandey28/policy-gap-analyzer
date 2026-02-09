import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def keyword_score(clause, segment):

    keywords = clause["normalized_keywords"]

    if not keywords:
        return 0

    matched = 0

    for kw in keywords:
        if re.search(rf"\b{kw}\b", segment):
            matched += 1

    return matched / len(keywords)



def tfidf_score(text1, text2):

    vec = TfidfVectorizer(stop_words="english")
    tfidf = vec.fit_transform([text1, text2])

    return cosine_similarity(tfidf[0], tfidf[1])[0][0]



def score(clause, segment):

    kw = keyword_score(clause, segment)


    if kw >= 0.5:
        return 0.8

    sim = tfidf_score(
        clause["normalized_requirement"],
        segment
    )

    return 0.5 * kw + 0.5 * sim



def classify(score):

    if score >= 0.6:
        return "Covered"
    elif score >= 0.25:
        return "Partial"
    return "Missing"
