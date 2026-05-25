from reviewer.dataset_reviewer import (find_similar_question)

def review_response(query, response):

    dangerous_keywords = [
        "bomb",
        "explosive",
        "poison",
        "weapon",
        "kill",
        "hack",
        "malware"
    ]

    combined_text = (query + " " + response).lower()

    issues = []

    # Safety check
    for keyword in dangerous_keywords:

        if keyword in combined_text:

            issues.append(f"Dangerous keyword: {keyword}")

    # Dataset similarity check
    match = find_similar_question(query)

    if match["score"] >= 0.60:

        decision = "APPROVE"

    else:

        decision = "ESCALATE"

        issues.append("No reliable historical match found")

    # Dangerous content overrides approval
    if len(issues) > 0:

        decision = "ESCALATE"

    matched_question = None
    matched_answer = None

    if decision == "APPROVE":

        matched_question = match["question"]
        matched_answer = match["answer"]

    return {
        "decision": decision,
        "confidence": round(match["score"],2),
        "issues": issues,
        "matched_question": matched_question,
        "matched_answer": matched_answer
    }