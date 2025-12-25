#!/usr/bin/env python3
"""
CONFIGURATION MODULE
Centralized configuration management for the Cash Money Colors App
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class APIConfiguration:
    """API Keys and Configuration"""

    # AI API Keys
    grok_key: str = ""
    deepseek_key: str = ""
    blackbox_key: str = ""
    claude_key: str = ""

    # Service API Keys
    gmail_credentials: str = "credentials.json"
    stripe_key: str = ""
    paypal_key: str = ""

    # Payment Configuration
    stripe_webhook_secret: str = ""
    paypal_client_id: str = ""
    paypal_client_secret: str = ""

    # Database Configuration
    db_name: str = "nexus.db"
    backup_frequency: int = 300  # seconds

    # Gmail Configuration
    email_sender: str = "cashmoneycolors@gmail.com"

    # System Configuration
    max_threads: int = 10
    log_level: str = "INFO"
    health_check_interval: int = 300

    def __post_init__(self):
        """Load configuration from environment variables"""
        self.load_from_environment()

    def load_from_environment(self):
        """Load API keys from environment variables"""
        env_mapping = {
            'GROK_API_KEY': 'grok_key',
            'DEEPSEEK_API_KEY': 'deepseek_key',
            'BLACKBOX_API_KEY': 'blackbox_key',
            'ANTHROPIC_API_KEY': 'claude_key',
            'STRIPE_SECRET_KEY': 'stripe_key',
            'PAYPAL_CLIENT_ID': 'paypal_client_id',
            'PAYPAL_CLIENT_SECRET': 'paypal_client_secret',
            'STRIPE_WEBHOOK_SECRET': 'stripe_webhook_secret'
        }

        for env_var, config_attr in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                setattr(self, config_attr, value)

    def validate(self) -> bool:
        """Validate configuration has required keys"""
        required_keys = ['grok_key', 'deepseek_key', 'claude_key']

        for key in required_keys:
            if not getattr(self, key):
                print(f"Warning: {key} not configured")

        return any(getattr(self, key) for key in required_keys)

# Global configuration instance
API_CONFIG = APIConfiguration()

def create_config_structure():
    """Create necessary configuration files if they don't exist"""
    config_files = {
        'credentials.json': '''
{
  "web": {
    "client_id": "your_google_client_id.apps.googleusercontent.com",
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_client_secret",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
  }
}
''',

        '.env.example': '''
# AI API Keys
GROK_API_KEY=sk-or-v1-your_grok_key_here
DEEPSEEK_API_KEY=deepseek-your_deepseek_key_here
BLACKBOX_API_KEY=blackbox-your_blackbox_key_here
ANTHROPIC_API_KEY=sk-ant-api03-your_claude_key_here

# Payment API Keys
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key_here
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret

# Stripe Webhooks
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Gmail Configuration
GMAIL_EMAIL=cashmoneycolors@gmail.com
'''
    }

    for config_file, content in config_files.items():
        if not Path(config_file).exists():
            with open(config_file, 'w') as f:
                f.write(content.strip())

if __name__ == "__main__":
    # Create configuration files
    create_config_structure()

    # Validate configuration
    if API_CONFIG.validate():
        print("✅ Configuration loaded successfully")
    else:
        print("⚠️  Warning: Some API keys are missing")
        print("Please set your API keys in environment variables or create .env file")
