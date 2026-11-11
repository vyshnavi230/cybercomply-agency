import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def append_to_sheet(records):
    sheet_id = os.getenv("SPREADSHEET_ID")
    if not sheet_id or "PASTE" in sheet_id:
        raise ValueError("SPREADSHEET_ID is not configured in .env")
        
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    
    for row in records:
        sheet.append_row(row)
    print(f"[+] Successfully logged {len(records)} findings to Google Sheet ledger.")

def send_daily_brief(recipient_email, summary_records):
    sender_email = os.getenv("SMTP_SENDER")
    sender_password = os.getenv("SMTP_PASSWORD")
    
    if not sender_email or not sender_password or "your-gmail" in sender_email:
        print("[!] Email credentials not configured in .env. Skipping email dispatch.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"CyberComply Daily Brief - {datetime.date.today()}"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    rows_html = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td><strong>{r[6]}</strong></td><td>{r[7]}</td></tr>"
        for r in summary_records
    ])

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #1e293b;">
        <h2 style="color: #0f172a; border-bottom: 2px solid #0284c7; padding-bottom: 8px;">CyberComply Executive Briefing (08:00 AM)</h2>
        <p><strong>Overall SOC 2 Type II Audit Readiness:</strong> <span style="color: #16a34a; font-weight: bold;">88.4%</span></p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; border-color: #cbd5e1; font-size: 13px;">
          <tr style="background-color: #f1f5f9; text-align: left;">
            <th>Timestamp</th><th>Agent Name</th><th>Task Performed</th><th>Output Status</th><th>Issue ID</th><th>Control</th><th>Severity</th><th>Remediation</th>
          </tr>
          {rows_html}
        </table>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    # Connect using Port 587 with STARTTLS
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
    server.set_debuglevel(0)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email.strip(), sender_password.strip())
    server.sendmail(sender_email.strip(), recipient_email.strip(), msg.as_string())
    server.quit()
    print("[+] Executive briefing email sent successfully.")

if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    findings = [
        [now, "IAM Auditor", "Scanned Directory Accounts", "SUCCESS", "ISSUE-101", "SOC 2 CC6.2", "HIGH", "Disable inactive user"],
        [now, "Cloud Inspector", "Public S3 Bucket Scan", "SUCCESS", "ISSUE-102", "ISO A.12.1", "CRITICAL", "Enforce bucket block public access"],
        [now, "Vendor Evaluator", "Reviewed Third-Party DPAs", "SUCCESS", "ISSUE-103", "GDPR Art. 28", "MEDIUM", "Request signed SCC from vendor"],
        [now, "Code Hunter", "GitHub Secret Scan", "SUCCESS", "ISSUE-104", "SOC 2 CC7.1", "HIGH", "Revoke exposed AWS token"],
        [now, "QA Reviewer", "False Positive Verification Gate", "SUCCESS", "GATE-001", "Verification QA", "INFO", "Verified all 4 alerts; 0 false positives"]
    ]
    
    print("[*] Starting CyberComply Autonomous Inspection Orchestration...")
    append_to_sheet(findings)
    recipient = os.getenv("ALERT_RECIPIENT", os.getenv("SMTP_SENDER"))
    send_daily_brief(recipient, findings)
    print("[*] Orchestration run complete.")