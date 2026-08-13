"""
auth/email_utils.py
---------------------
<<<<<<< HEAD
Sends the signup verification code by email, via Brevo's HTTPS API.

CONFIGURING REAL EMAIL DELIVERY:
Add these to Render's Environment tab (or backend/.env for local dev):
    BREVO_API_KEY=your-brevo-api-key
    BREVO_SENDER_EMAIL=your-verified-sender@email.com

WITHOUT BREVO_API_KEY CONFIGURED (local dev default):
The code is printed to the backend console and written to audit.log
=======
Sends the signup verification code (and password reset link) by email.

WHY BREVO (HTTP API):
- Render's free tier blocks outbound raw SMTP connections (ports
  587/465), so smtplib.SMTP(...) fails there with
  "OSError: [Errno 101] Network is unreachable" even though it works
  fine locally. Brevo sends email over a normal HTTPS API call
  (port 443), which Render does NOT block.
- Unlike Resend's free tier (which requires verifying a whole domain
  via DNS before you can email anyone other than your own account
  email), Brevo only requires verifying a single SENDER email address
  (a one-click email confirmation, no domain/DNS needed). Once that
  sender is verified, you can send to ANY recipient email — up to
  300 emails/day on the free plan.

SETUP (one-time):
1. Sign up for a free account at https://www.brevo.com
2. Verify a sender email: Dashboard -> Settings -> Senders, Domains
   & Dedicated IPs -> "Add a Sender" -> enter any email you control
   (e.g. your Gmail) -> click the confirmation link Brevo emails you.
3. Create an API key: Dashboard -> Settings -> API Keys -> "Generate
   a new API key".
4. Add these to backend/.env (and to Render's Environment tab for
   production):
    BREVO_API_KEY=xkeysib-your-key-here
    EMAIL_FROM=the-sender-email-you-verified@example.com
    EMAIL_FROM_NAME=GitLab AI Content Engine   (optional, defaults below)

WITHOUT BREVO_API_KEY CONFIGURED (local dev default):
The code is printed to the backend console and logged to audit.log
>>>>>>> 0ffb3b780a93f9b649d3858d1b6326198f1aa6e1
instead of emailed, so you can still test the signup flow without
setting up email. Look for a line like:
    [DEV EMAIL] To: someone@example.com | Subject: Your verification code
"""

import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from database.audit_log import log_event

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
<<<<<<< HEAD
EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@example.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "GitLab AI Content Engine")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _send_email(to_email: str, subject: str, body_text: str) -> None:
    """
    Shared helper: sends a plain-text email via the Brevo HTTP API.
    Falls back to console/log output if BREVO_API_KEY isn't configured,
    so local development still works without any email setup.
    """
    if not BREVO_API_KEY:
        # Dev fallback: no email service configured, so just log it.
        print(f"[DEV EMAIL] To: {to_email} | Subject: {subject}\n{body_text}")
        log_event("email_logged_dev_mode", job_id=None, email=to_email)
        return

    try:
        response = requests.post(
            BREVO_API_URL,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "sender": {"name": EMAIL_FROM_NAME, "email": EMAIL_FROM},
                "to": [{"email": to_email}],
                "subject": subject,
                "textContent": body_text,
            },
            timeout=10,
        )
        response.raise_for_status()
        print(f"[EMAIL SENT] {subject} -> {to_email}")
    except requests.RequestException as exc:
        # Surface Brevo's actual error body (e.g. unverified sender,
        # bad API key) in the logs instead of just the status code.
        detail = getattr(exc, "response", None)
        detail_text = detail.text if detail is not None else str(exc)
        print(f"[EMAIL FAILED] {subject} -> {to_email}: {detail_text}")
        log_event("email_send_failed", job_id=None, email=to_email, error=detail_text)
        raise
=======
EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@example.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "GitLab AI Content Engine")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _send_email(to_email: str, subject: str, body_text: str) -> None:
    """
    Shared helper: sends a plain-text email via the Brevo HTTP API.
    Falls back to console/log output if BREVO_API_KEY isn't configured,
    so local development still works without any email setup.
    """
    if not BREVO_API_KEY:
        # Dev fallback: no email service configured, so just log it.
        print(f"[DEV EMAIL] To: {to_email} | Subject: {subject}\n{body_text}")
        log_event("email_logged_dev_mode", job_id=None, email=to_email)
        return

    try:
        response = requests.post(
            BREVO_API_URL,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "sender": {"name": EMAIL_FROM_NAME, "email": EMAIL_FROM},
                "to": [{"email": to_email}],
                "subject": subject,
                "textContent": body_text,
            },
            timeout=10,
        )
        response.raise_for_status()
        print(f"[EMAIL SENT] {subject} -> {to_email}")
    except requests.RequestException as exc:
        # Surface Brevo's actual error body (e.g. unverified sender,
        # bad API key) in the logs instead of just the status code.
        detail = getattr(exc, "response", None)
        detail_text = detail.text if detail is not None else str(exc)
        print(f"[EMAIL FAILED] {subject} -> {to_email}: {detail_text}")
        log_event("email_send_failed", job_id=None, email=to_email, error=detail_text)
        raise
>>>>>>> 0ffb3b780a93f9b649d3858d1b6326198f1aa6e1


def send_verification_code(email: str, code: str) -> None:
    if not (BREVO_API_KEY and BREVO_SENDER_EMAIL):
        # Dev fallback: no mail service configured, so just log it.
        print(f"[DEV EMAIL] Verification code for {email}: {code}")
        log_event("verification_code_logged_dev_mode", job_id=None, email=email)
        return

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"email": BREVO_SENDER_EMAIL},
        subject="Your verification code",
        text_content=f"Your verification code is: {code}\n\nThis code expires in 15 minutes.",
    )

<<<<<<< HEAD
    try:
        api_instance.send_transac_email(send_email)
        print(f"SUCCESS: Verification code sent to {email}")
    except ApiException as e:
        print(f"FAILED to send email: {e}")
=======
def send_reset_email(email: str, reset_link: str) -> None:
    _send_email(
        to_email=email,
        subject="Reset Your Password",
        body_text=(
            "Please click this link to reset your password:\n\n"
            f"{reset_link}\n\n"
            "This link expires in 15 minutes."
        ),
    )
>>>>>>> 0ffb3b780a93f9b649d3858d1b6326198f1aa6e1
