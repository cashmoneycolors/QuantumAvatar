#!/usr/bin/env python3
"""
AI MANAGER MODULE
Manages and orchestrates all AI agents in the autonomous system
"""

import threading
import time
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from .base_ai import BaseAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import safe_execute

class AIManager:
    """Unified AI Manager for coordinating multiple AI agents"""

    def __init__(self, database):
        self.db = database
        self.agents = {}
        self.active_agents = []
        self.coordination_interval = 60  # seconds
        self.running = False

        # Initialize coordination thread
        self.coordinator_thread = threading.Thread(
            target=self._coordinate_agents,
            daemon=True
        )

    def register_agent(self, agent_name: str, agent_class: type, config: Dict[str, Any]):
        """Register a new AI agent"""
        try:
            agent_instance = safe_execute(agent_class, self.db, config)
            if agent_instance:
                self.agents[agent_name] = {
                    'instance': agent_instance,
                    'config': config,
                    'status': 'stopped'
                }
                logging.info(f"Registered AI agent: {agent_name}")
            else:
                logging.error(f"Failed to register AI agent: {agent_name}")
        except Exception as e:
            logging.error(f"Error registering agent {agent_name}: {e}")

    def start_agent(self, agent_config: dict):
        """Start a specific AI agent"""
        # Extract agent name from config
        agent_name = agent_config.get('agent_name') or agent_config.get('name', 'unknown')

        if agent_name in self.agents:
            agent_data = self.agents[agent_name]
            if agent_data['status'] != 'running':
                try:
                    agent_data['instance'].start()
                    agent_data['status'] = 'running'
                    self.active_agents.append(agent_name)
                    logging.info(f"Started AI agent: {agent_name}")
                except Exception as e:
                    logging.error(f"Failed to start agent {agent_name}: {e}")
            return

        # If agent not registered yet, try to register and start it
        try:
            agent_type = agent_config.get('type', 'unknown')
            api_key = agent_config.get('api_key', '')

            if not api_key:
                logging.error(f"No API key provided for agent {agent_name}")
                return

            # Dynamic import and registration based on type
            if agent_type == 'grok':
                from ai.grok_ai import GrokAI
                agent_class = GrokAI
            elif agent_type == 'claude':
                try:
                    from anthropic import Anthropic
                    from ai.claude_ai import ClaudeAI
                    agent_class = ClaudeAI
                except ImportError:
                    logging.warning("Claude not available, using fallback")
                    from ai.base_ai import BaseAI
                    agent_class = BaseAI
            else:
                logging.warning(f"Unknown agent type: {agent_type}, using base")
                from ai.base_ai import BaseAI
                agent_class = BaseAI

            # Register the agent
            agent_instance = agent_class(self.db, api_key)
            self.agents[agent_name] = {
                'instance': agent_instance,
                'config': agent_config,
                'status': 'stopped'
            }

            # Now start it
            self.start_agent(agent_config)  # Recursive call

        except Exception as e:
            logging.error(f"Failed to register/start agent {agent_name}: {e}")
            logging.error(f"Agent config: {agent_config}")

    def stop_agent(self, agent_name: str):
        """Stop a specific AI agent"""
        if agent_name in self.agents:
            agent_data = self.agents[agent_name]
            if agent_data['status'] == 'running':
                try:
                    agent_data['instance'].stop()
                    agent_data['status'] = 'stopped'
                    if agent_name in self.active_agents:
                        self.active_agents.remove(agent_name)
                    logging.info(f"Stopped AI agent: {agent_name}")
                except Exception as e:
                    logging.error(f"Failed to stop agent {agent_name}: {e}")

    def start_all_agents(self):
        """Start all registered agents"""
        for agent_name in self.agents:
            self.start_agent(agent_name)

        self.running = True
        self.coordinator_thread.start()
        logging.info("All AI agents started")

    def stop_all_agents(self):
        """Stop all running agents"""
        self.running = False
        for agent_name in self.active_agents[:]:  # Copy list to avoid modification during iteration
            self.stop_agent(agent_name)
        logging.info("All AI agents stopped")

    def get_agent_status(self, agent_name: str = None) -> Dict[str, Any]:
        """Get status of agents"""
        if agent_name:
            if agent_name in self.agents:
                return {
                    'name': agent_name,
                    'status': self.agents[agent_name]['status'],
                    'config': self.agents[agent_name]['config']
                }
            return {}
        else:
            return {
                'total_agents': len(self.agents),
                'active_agents': len(self.active_agents),
                'agents': [{
                    'name': name,
                    'status': data['status']
                } for name, data in self.agents.items()]
            }

    def send_task_to_agent(self, agent_name: str, task: Dict[str, Any]):
        """Send a task to a specific agent"""
        if agent_name in self.agents and self.agents[agent_name]['status'] == 'running':
            try:
                agent = self.agents[agent_name]['instance']
                if hasattr(agent, 'process_task'):
                    threading.Thread(
                        target=agent.process_task,
                        args=(task,),
                        daemon=True
                    ).start()
                    logging.info(f"Sent task to agent {agent_name}")
                else:
                    logging.warning(f"Agent {agent_name} does not support task processing")
            except Exception as e:
                logging.error(f"Failed to send task to agent {agent_name}: {e}")

    def broadcast_task(self, task: Dict[str, Any]):
        """Send task to all active agents"""
        for agent_name in self.active_agents:
            self.send_task_to_agent(agent_name, task)

    def _coordinate_agents(self):
        """Coordinate agents autonomously"""
        while self.running:
            try:
                # Check for pending tasks from database
                pending_tasks = self.db.get_pending_tasks()

                if pending_tasks:
                    for task in pending_tasks:
                        # Distribute tasks based on type
                        if task['type'] == 'content_generation':
                            self.send_task_to_agent('grok_ai', task)
                        elif task['type'] == 'code_generation':
                            self.send_task_to_agent('deepseek_ai', task)
                        elif task['type'] == 'prototyping':
                            self.send_task_to_agent('blackbox_ai', task)
                        elif task['type'] == 'analysis':
                            self.send_task_to_agent('claude_ai', task)
                        else:
                            # Send to all agents
                            self.broadcast_task(task)

                # Health check and auto-restart failed agents
                self._health_check_agents()

            except Exception as e:
                logging.error(f"Error in agent coordination: {e}")

            time.sleep(self.coordination_interval)

    def _health_check_agents(self):
        """Perform health checks on agents and restart if necessary"""
        for agent_name in self.agents:
            agent_data = self.agents[agent_name]
            if agent_data['status'] == 'running':
                agent = agent_data['instance']
                try:
                    # Check if agent is responsive
                    if hasattr(agent, 'is_alive'):
                        if not agent.is_alive():
                            logging.warning(f"Agent {agent_name} appears dead, restarting...")
                            self.stop_agent(agent_name)
                            self.start_agent(agent_name)

                    # Could add more sophisticated health checks here

                except Exception as e:
                    logging.error(f"Health check failed for agent {agent_name}: {e}")

    def shutdown(self):
        """Shutdown the AI manager"""
        logging.info("Shutting down AI Manager...")
        self.stop_all_agents()
        self.running = False

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
