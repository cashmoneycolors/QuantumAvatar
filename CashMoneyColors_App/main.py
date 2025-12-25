#!/usr/bin/env python3
"""
CASHMONEY COLORS AUTONOMOUS DESKTOP APP
Professional Native Windows Application
Full Quantum Avatar Integration, Autonomic AI Swarm, Payment Processing
"""

import sys
import os
from pathlib import Path

# Ensure proper imports work
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
from datetime import datetime

# Custom imports
from core.config import API_CONFIG
from core.chatbot import NexusChatbot
from core.services.gmail_service import GmailService
from core.services.event_service import EventService
from ai.manager import AIManager
from ai.grok_ai import GrokAI
from db.manager import get_database, NexusDatabase
from ui.main_window import MainWindow
from utils.logger import setup_logging
from utils.helpers import safe_execute, create_directories, config_manager

# Setup logging
setup_logging('logs/app.log')

class CashMoneyColorsApp:
    """Main Application Class"""

    def __init__(self):
        self.app = None
        self.db = None
        self.event_service = None
        self.ai_manager = None
        self.chatbot = None
        self.gmail_service = None

    def setup_bootstrap(self):
        """Setup the application bootstrap components"""
        logging.info("Bootstrapping CashMoney Colors App...")

        # Create all necessary directories
        create_directories([
            'logs',
            'data',
            'backups',
            'config'
        ])

        # Initialize core components
        self.db = safe_execute(NexusDatabase, 'data/nexus.db')
        if not self.db:
            logging.error("Failed to initialize database")
            return False

        self.event_service = safe_execute(EventService)
        self.gmail_service = safe_execute(GmailService, API_CONFIG.gmail_credentials)

        # Setup AI Manager
        self.ai_manager = safe_execute(AIManager, self.db)
        if not self.ai_manager:
            logging.error("Failed to initialize AI Manager")
            return False

        # Initialize AI Agents
        threading.Thread(target=self._initialize_ai_agents, daemon=True).start()

        # Setup Chatbot
        self.chatbot = safe_execute(NexusChatbot, self.db, API_CONFIG)

        logging.info("Bootstrap complete")
        return True

    def _initialize_ai_agents(self):
        """Initialize AI agents in background"""
        agents_config = [
            {
                'agent_name': 'grok_ai',
                'type': 'grok',
                'api_key': API_CONFIG.grok_key,
                'capabilities': ['content_generation', 'strategy'],
                'auto_start': True
            },
            {
                'agent_name': 'deepseek_ai',
                'type': 'deepseek',
                'api_key': API_CONFIG.deepseek_key,
                'capabilities': ['code_generation', 'bug_fixing'],
                'auto_start': True
            },
            {
                'agent_name': 'blackbox_ai',
                'type': 'blackbox',
                'api_key': API_CONFIG.blackbox_key,
                'capabilities': ['prototyping', 'video_editing'],
                'auto_start': True
            },
            {
                'agent_name': 'claude_ai',
                'type': 'claude',
                'api_key': API_CONFIG.claude_key,
                'capabilities': ['analysis', 'optimization'],
                'auto_start': True
            }
        ]

        for agent_config in agents_config:
            if agent_config['auto_start']:
                try:
                    # Pass the full config dict as expected by start_agent
                    self.ai_manager.start_agent(agent_config)
                    logging.info(f"Started {agent_config['agent_name']} agent")
                except Exception as e:
                    logging.error(f"Failed to start {agent_config['agent_name']}: {e}")

    def run(self):
        """Run the main application"""
        try:
            # Initialize app
            self.app = tk.Tk()

            # Bootstrap components
            if not self.setup_bootstrap():
                messagebox.showerror("Error", "Failed to initialize application")
                return

            # Create main window
            self.main_window = MainWindow(
                self.app,
                self.db,
                self.chatbot,
                self.ai_manager,
                self.event_service
            )

            # Start background services
            self._start_background_services()

            # Run event loop
            self.app.protocol("WM_DELETE_WINDOW", self._on_closing)
            self.app.mainloop()

        except Exception as e:
            try:
                import traceback
                logging.error(f"Application error: {e}")
                logging.error(f"Traceback: {traceback.format_exc()}")
                messagebox.showerror("Error", f"Application error: {e}")
            except:
                print(f"Application error: {e}")

    def _start_background_services(self):
        """Start background monitoring services"""
        # Revenue monitoring
        threading.Thread(target=self._revenue_monitor, daemon=True).start()

        # System health check
        threading.Thread(target=self._health_monitor, daemon=True).start()

        # AI coordination
        threading.Thread(target=self._ai_coordination, daemon=True).start()

    def _revenue_monitor(self):
        """Monitor revenue in background"""
        while True:
            try:
                # Implement revenue monitoring logic here
                time.sleep(60)  # Monitor every minute
            except Exception as e:
                logging.error(f"Revenue monitor error: {e}")

    def _health_monitor(self):
        """Monitor system health"""
        while True:
            try:
                # Implement health monitoring logic here
                time.sleep(300)  # Health check every 5 minutes
            except Exception as e:
                logging.error(f"Health monitor error: {e}")

    def _ai_coordination(self):
        """Coordinate AI agents"""
        while True:
            try:
                # Implement AI coordination logic here
                time.sleep(120)  # Coordinate every 2 minutes
            except Exception as e:
                logging.error(f"AI coordination error: {e}")

    def _on_closing(self):
        """Handle application close"""
        logging.info("Application closing...")
        try:
            if self.ai_manager:
                self.ai_manager.shutdown()
            if self.db:
                self.db.close()
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")

        self.app.destroy()

def main():
    """Entry point"""
    print("*** CASH MONEY COLORS AUTONOMOUS DESKTOP APP STARTING ***")
    print("Quantum Avatar AI Swarm | Professional Windows Native App")
    print("="*60)

    app = CashMoneyColorsApp()
    app.run()

if __name__ == "__main__":
    main()
