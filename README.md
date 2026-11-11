# CyberComply Autonomous Inspection Orchestrator

An autonomous compliance orchestration system that runs simulated security and compliance findings across multiple frameworks (SOC 2, ISO 27001, GDPR), logs audit trails to a Google Sheet ledger, and delivers daily executive briefing emails.

## Features
- **Autonomous Inspection Orchestration**: Aggregates findings across multiple compliance agents (IAM Auditor, Cloud Inspector, Vendor Evaluator, Code Hunter, and QA Reviewer).
- **Google Sheets Integration**: Authenticates via a Google Cloud Service Account and appends findings to a live compliance ledger.
- **Executive Briefing Email**: Dispatches automated HTML summaries with audit readiness scores via Gmail SMTP (TLS/SSL).

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- A Google Cloud Service Account key file named `service_account.json` in the root folder with permissions on the target Google Sheet.
- A Gmail account with an active 16-character Google App Password.

### 2. Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# Install dependencies:
pip install -r requirements.txt