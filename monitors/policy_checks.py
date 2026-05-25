import re

SENSITIVE_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
}

BLOCKED_TOPICS = [
    "password dump",
    "bypass authentication",
    "steal credentials",
    "malware",
    "phishing kit",
]

def check_sensitive_data(output):
    findings = []

    for label, pattern in SENSITIVE_PATTERNS.items():
        if re.search(pattern, output):
            findings.append(f"Possible sensitive data detected: {label}")

    return findings

def check_blocked_topics(output):
    findings = []

    lowered = output.lower()
    for topic in BLOCKED_TOPICS:
        if topic in lowered:
            findings.append(f"Blocked topic detected: {topic}")

    return findings

def run_policy_checks(output):
    findings = []
    findings.extend(check_sensitive_data(output))
    findings.extend(check_blocked_topics(output))

    status = "PASS" if not findings else "FLAGGED"

    return {
        "status": status,
        "findings": findings
    }
