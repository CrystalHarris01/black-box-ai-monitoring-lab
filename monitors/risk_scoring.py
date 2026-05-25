def calculate_risk_score(findings):

    score = 0

    for finding in findings:

        if "sensitive data" in finding.lower():
            score += 40

        elif "blocked topic" in finding.lower():
            score += 30

        else:
            score += 10

    if score == 0:
        risk_level = "LOW"

    elif score <= 40:
        risk_level = "MEDIUM"

    elif score <= 70:
        risk_level = "HIGH"

    else:
        risk_level = "CRITICAL"

    return {
        "score": score,
        "risk_level": risk_level
    }
