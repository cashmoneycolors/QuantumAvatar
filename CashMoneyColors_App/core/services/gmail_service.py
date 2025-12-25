#!/usr/bin/env python3
"""
GMAIL SERVICE MODULE
Email communication interface for autonomous operations
Handles sending notifications, reports, and coordinating with external services
"""

import os
import json
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logging.warning("Google API client not available - Gmail functionality disabled")

class GmailService:
    """Gmail service for autonomous email operations"""

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.service = None
        self.scopes = ['https://www.googleapis.com/auth/gmail.modify']

        if GOOGLE_API_AVAILABLE:
            self.initialize_gmail()
        else:
            logging.warning("Gmail service unavailable due to missing dependencies")

    def initialize_gmail(self):
        """Initialize Gmail API service"""
        try:
            creds = self._get_credentials()
            if creds:
                self.service = build('gmail', 'v1', credentials=creds)
                logging.info("Gmail service initialized successfully")
            else:
                logging.error("Could not initialize Gmail credentials")
        except Exception as e:
            logging.error(f"Failed to initialize Gmail service: {e}")

    def _get_credentials(self):
        """Get or refresh OAuth credentials"""
        creds = None

        # Token file path
        token_path = Path("token_gmail.json")

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logging.warning(f"Token refresh failed: {e}")
                    creds = None
            else:
                creds = None

            if not creds and Path(self.credentials_file).exists():
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.scopes
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    logging.error(f"OAuth flow failed: {e}")
                    return None

            if creds:
                with open(token_path, 'w') as token_file:
                    token_file.write(creds.to_json())

        return creds

    def send_email(self, to: str, subject: str, body: str, html_body: str = None) -> bool:
        """Send email autonomously"""
        if not self.service:
            logging.warning("Gmail service not available - skipping email send")
            return False

        try:
            message = self._create_message(to, subject, body, html_body)
            sent_message = self.service.users().messages().send(
                userId="me", body=message
            ).execute()

            logging.info(f"Email sent successfully to {to}: {subject}")
            return True

        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False

    def _create_message(self, to: str, subject: str, body: str, html_body: str = None):
        """Create MIME message for Gmail API"""
        message = MIMEMultipart("alternative")

        message['to'] = to
        message['from'] = "me"
        message['subject'] = subject

        # Plain text version
        text_part = MIMEText(body, "plain")
        message.attach(text_part)

        # HTML version if provided
        if html_body:
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)

        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw.decode()}

    def send_notification(self, subject: str, details: dict) -> bool:
        """Send notification email about system events"""
        to = "cashmoneycolors@gmail.com"  # Configurable recipient
        body = f"System Notification: {subject}\n\nDetails:\n{json.dumps(details, indent=2)}"
        html_body = f"""
        <h2>System Notification</h2>
        <h3>{subject}</h3>
        <pre>{json.dumps(details, indent=2)}</pre>
        <p>Sent by Cash Money Colors Autonomous System</p>
        """

        return self.send_email(to, f"SYSTEM: {subject}", body, html_body)

    def send_revenue_report(self, revenue_data: dict) -> bool:
        """Send revenue report via email"""
        total_revenue = revenue_data.get('total_revenue', 0)
        subject = f"Revenue Report: €{total_revenue:,.2f}"

        body = f"""
Today's Revenue Report
Total Revenue: €{total_revenue:,.2f}

Revenue Breakdown:
{json.dumps(revenue_data.get('breakdown', {}), indent=2)}

Generated by: Cash Money Colors AI System
        """

        html_body = f"""
        <h2>Today's Revenue Report</h2>
        <h1>€{total_revenue:,.2f}</h1>
        <h3>Revenue Breakdown:</h3>
        <pre>{json.dumps(revenue_data.get('breakdown', {}), indent=2)}</pre>
        <p><small>Generated by Cash Money Colors AI System</small></p>
        """

        return self.send_email("cashmoneycolors@gmail.com", subject, body, html_body)

    def send_ai_content(self, content_type: str, content: str, recipient: str = None) -> bool:
        """Send AI-generated content via email"""
        if not recipient:
            recipient = "cashmoneycolors@gmail.com"

        subject = f"AI Generated Content: {content_type}"
        body = f"""
AI Generated Content: {content_type}

Generated automated content:

{content}

This content was generated by the Cash Money Colors AI swarm.
        """

        return self.send_email(recipient, subject, body)

    def check_service_status(self) -> bool:
        """Check if Gmail service is operational"""
        return self.service is not None

    def get_service_status(self) -> dict:
        """Get service status information"""
        return {
            'service_available': self.service is not None,
            'google_api_available': GOOGLE_API_AVAILABLE,
            'credentials_file_exists': Path(self.credentials_file).exists(),
            'token_file_exists': Path("token_gmail.json").exists()
        }
