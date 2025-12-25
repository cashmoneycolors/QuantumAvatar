#!/usr/bin/env python3
"""
PAYPAL PAYMENT SERVICE MODULE
Real PayPal API integration for the Quantum Avatar Business Empire
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import base64
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.logger import get_logger_instance

class PayPalService:
    """PayPal API Service for business payments"""

    def __init__(self, client_id: str, client_secret: str, is_sandbox: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.is_sandbox = is_sandbox

        # Set endpoints based on environment
        if self.is_sandbox:
            self.base_url = "https://api.sandbox.paypal.com"
        else:
            self.base_url = "https://api.paypal.com"

        self.token_url = f"{self.base_url}/v1/oauth2/token"
        self.payment_url = f"{self.base_url}/v2/payments"

        # Initialize logger
        self.logger = get_logger_instance("PayPalService")

        # Access token cache
        self._access_token = None
        self._token_expires = None

    def _get_access_token(self) -> str:
        """Get OAuth2 access token from PayPal"""

        # Check if we have a valid cached token
        if self._access_token and self._token_expires and datetime.now() < self._token_expires:
            return self._access_token

        try:
            # Base64 encode client credentials
            credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

            headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {"grant_type": "client_credentials"}

            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self._access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3599)  # Default 1 hour

            # Set expiration time (10 minutes buffer)
            self._token_expires = datetime.now() + timedelta(seconds=expires_in - 600)

            self.logger.info("PayPal access token obtained successfully")
            return self._access_token

        except Exception as e:
            self.logger.error(f"Failed to get PayPal access token: {e}")
            raise Exception(f"PayPal authentication failed: {e}")

    def create_payment(self, amount: float, description: str,
                      currency: str = "EUR", return_url: str = None,
                      cancel_url: str = None) -> Dict:
        """Create a PayPal payment"""

        if not return_url:
            return_url = "https://cashmoneycolors.com/payment/success"
        if not cancel_url:
            cancel_url = "https://cashmoneycolors.com/payment/cancel"

        try:
            access_token = self._get_access_token()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            payment_data = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": f"{amount:.2f}",
                        "currency": currency
                    },
                    "description": description[:127]  # PayPal limit
                }],
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                }
            }

            response = requests.post(
                f"{self.base_url}/v1/payments/payment",
                headers=headers,
                json=payment_data
            )
            response.raise_for_status()

            payment = response.json()
            self.logger.info(f"PayPal payment created: {payment['id']} for {amount} {currency}")

            return payment

        except Exception as e:
            self.logger.error(f"Failed to create PayPal payment: {e}")
            raise Exception(f"Payment creation failed: {e}")

    def execute_payment(self, payment_id: str, payer_id: str) -> Dict:
        """Execute an approved PayPal payment"""

        try:
            access_token = self._get_access_token()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            execute_data = {
                "payer_id": payer_id
            }

            response = requests.post(
                f"{self.base_url}/v1/payments/payment/{payment_id}/execute",
                headers=headers,
                json=execute_data
            )
            response.raise_for_status()

            result = response.json()
            self.logger.info(f"PayPal payment executed: {payment_id}")

            return result

        except Exception as e:
            self.logger.error(f"Failed to execute PayPal payment: {e}")
            raise Exception(f"Payment execution failed: {e}")

    def refund_payment(self, payment_id: str, amount: Optional[float] = None,
                      currency: str = "EUR") -> Dict:
        """Process a refund for a completed payment"""

        try:
            access_token = self._get_access_token()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            refund_data = {}
            if amount:
                refund_data["amount"] = {
                    "total": f"{amount:.2f}",
                    "currency": currency
                }

            # Get sale ID from payment first
            sale_response = requests.get(
                f"{self.base_url}/v1/payments/payment/{payment_id}",
                headers=headers
            )
            sale_response.raise_for_status()

            payment_data = sale_response.json()
            sale_id = None

            for transaction in payment_data.get("transactions", []):
                for related_resource in transaction.get("related_resources", []):
                    if "sale" in related_resource:
                        sale_id = related_resource["sale"]["id"]
                        break
                if sale_id:
                    break

            if not sale_id:
                raise Exception("Could not find sale ID for refund")

            response = requests.post(
                f"{self.base_url}/v1/payments/sale/{sale_id}/refund",
                headers=headers,
                json=refund_data if refund_data else {}
            )
            response.raise_for_status()

            refund = response.json()
            self.logger.info(f"PayPal refund processed: {refund['id']}")

            return refund

        except Exception as e:
            self.logger.error(f"Failed to process PayPal refund: {e}")
            raise Exception(f"Refund failed: {e}")

    def get_payment_details(self, payment_id: str) -> Dict:
        """Get details of a payment"""

        try:
            access_token = self._get_access_token()

            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            response = requests.get(
                f"{self.base_url}/v1/payments/payment/{payment_id}",
                headers=headers
            )
            response.raise_for_status()

            payment = response.json()
            return payment

        except Exception as e:
            self.logger.error(f"Failed to get PayPal payment details: {e}")
            raise Exception(f"Could not fetch payment details: {e}")

    def create_subscription_plan(self, name: str, description: str,
                               amount: float, currency: str = "EUR") -> Dict:
        """Create a subscription plan (requires business account approval)"""

        try:
            access_token = self._get_access_token()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            plan_data = {
                "name": name,
                "description": description,
                "type": "INFINITE",
                "payment_definitions": [{
                    "name": "Regular Payment",
                    "type": "REGULAR",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": currency
                    },
                    "cycles": "0"
                }],
                "merchant_preferences": {
                    "auto_bill_amount": "YES",
                    "cancel_url": "https://cashmoneycolors.com/cancel",
                    "return_url": "https://cashmoneycolors.com/success"
                }
            }

            response = requests.post(
                f"{self.base_url}/v1/payments/billing-plans",
                headers=headers,
                json=plan_data
            )
            response.raise_for_status()

            plan = response.json()
            self.logger.info(f"PayPal subscription plan created: {plan['id']}")

            return plan

        except Exception as e:
            self.logger.error(f"Failed to create PayPal subscription plan: {e}")
            raise Exception(f"Subscription plan creation failed: {e}")

# Quick payment functions for business use
def create_business_payment(service_name: str, amount: float,
                          customer_email: str = None) -> Dict:
    """Quick function to create business payments"""

    # This would load credentials from config
    # For demo purposes, returning mock data
    return {
        "payment_id": f"mock_{int(time.time())}",
        "amount": amount,
        "service": service_name,
        "status": "created",
        "timestamp": datetime.now().isoformat()
    }

def get_payment_status(payment_id: str) -> str:
    """Get payment status"""
    # Mock implementation
    return "completed"

def generate_invoice(service: str, amount: float, customer: str) -> str:
    """Generate payment invoice"""
    invoice = f"""
INVOICE #{int(time.time())}
=======================

Service: {service}
Amount: €{amount:.2f}
Customer: {customer}
Date: {datetime.now().strftime('%Y-%m-%d')}

PAYMENT LINK: https://paypal.me/cashmoneycolors/{amount}

Business Empire AI Suite
Quantum AI Technology GmbH
"""
    return invoice

# Export functions
__all__ = [
    'PayPalService',
    'create_business_payment',
    'get_payment_status',
    'generate_invoice'
]
