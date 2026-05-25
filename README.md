# Black Box AI Monitoring Lab

A cybersecurity and AI governance portfolio project demonstrating black-box AI monitoring, output policy scanning, audit logging, risk scoring, and ISO/IEC 42001-aligned governance concepts.

## Dashboard Preview

### Main Console
![Rogue AI Monitoring Console](docs/screenshots/dashboard-main.png)

### Governance Scan Results
![Governance Scan Results](docs/screenshots/dashboard-results.png)


## Project Overview

This lab simulates a monitored AI environment where user prompts are sent to a large language model and the generated output is scanned for governance and security risks.

The project is designed to show how organizations can monitor AI systems for unsafe outputs, sensitive data exposure, policy violations, and operational risk indicators.

## Key Features

- Real LLM API integration
- Streamlit-based rogue AI console interface
- Sensitive data detection
- Blocked-topic detection
- Risk scoring engine
- Audit logging
- ISO/IEC 42001 governance mapping
- ITIL AI governance concepts
- Secure local API key handling with `.env`

## Governance Concepts Demonstrated

### ISO/IEC 42001 Alignment

- AI risk management
- Accountability and traceability
- Continuous monitoring
- Human oversight support
- Information security and privacy controls
- Incident detection and response
- Continual improvement

### ITIL AI Concepts

- ETTC: Ethics, Transparency, Trust, Compliance
- AI lifecycle monitoring
- Auditability
- Governance adaptation
- Control boundaries

## Project Architecture

```text
black-box-ai-monitoring-lab/
├── app/
│   └── main.py
├── monitors/
│   ├── logger.py
│   ├── policy_checks.py
│   └── risk_scoring.py
├── requirements.txt
├── README.md
└── .gitignore
