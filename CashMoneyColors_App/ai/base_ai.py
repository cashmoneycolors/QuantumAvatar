#!/usr/bin/env python3
"""
BASE AI MODULE
Base class for all AI agents in the autonomous system
"""

import time
import logging
import threading
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import safe_execute

class BaseAI(ABC):
    """Base class for all AI agents"""

    def __init__(self, db_manager, config: Dict[str, Any]):
        self.db = db_manager
        self.config = config
        self.running = False
        self.thread = None
        self.name = self.__class__.__name__

        # Initialize AI client (subclass must override if needed)
        self.client = None

        # Performance tracking
        self.tasks_processed = 0
        self.last_activity = time.time()

    def start(self):
        """Start the AI agent"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            logging.info(f"{self.name} AI agent started")

    def stop(self):
        """Stop the AI agent"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logging.info(f"{self.name} AI agent stopped")

    def is_alive(self) -> bool:
        """Check if agent is alive"""
        return self.running and (self.thread is None or self.thread.is_alive())

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'name': self.name,
            'running': self.running,
            'alive': self.is_alive(),
            'tasks_processed': self.tasks_processed,
            'last_activity': time.time() - self.last_activity
        }

    @abstractmethod
    def _run_loop(self):
        """Main execution loop (subclass must implement)"""
        pass

    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task (subclass must implement)"""
        pass

    def _generate_response(self, prompt: str, model: str = None, **kwargs) -> str:
        """Generate response using AI (generic method)"""
        try:
            if not self.client:
                raise ValueError("AI client not initialized")

            # Default parameters
            request_params = {
                'model': model or getattr(self, 'default_model', 'gpt-3.5-turbo'),
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 1000,
                **kwargs
            }

            response = safe_execute(self.client.chat.completions.create, **request_params)
            if response and response.choices:
                return response.choices[0].message.content
            else:
                return "I apologize, but I couldn't generate a response at this time."

        except Exception as e:
            logging.error(f"{self.name} response generation failed: {e}")
            return f"Error generating response: {str(e)}"

    def _log_activity(self):
        """Update last activity timestamp"""
        self.last_activity = time.time()

    def _health_check(self) -> bool:
        """Perform basic health check"""
        # Basic checks that can be overridden by subclasses
        return self.is_alive()

class ContentGeneratorAI(BaseAI):
    """Base class for content generation AIs"""

    def __init__(self, db_manager, config):
        super().__init__(db_manager, config)
        self.content_type = "general_content"

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process content generation task"""
        try:
            prompt = task.get('content', '')
            if not prompt:
                return {'error': 'No content provided for task'}

            # Add context from knowledge base
            context = self._get_relevant_context(prompt)
            enhanced_prompt = f"Context: {context}\n\nTask: {prompt}"

            response = self._generate_response(enhanced_prompt)
            if response:
                # Save to knowledge base
                self.db.add_knowledge(prompt, response)
                self.tasks_processed += 1
                self._log_activity()

                return {
                    'success': True,
                    'content': response,
                    'type': self.content_type,
                    'task_id': task.get('id')
                }
            else:
                return {'error': 'Failed to generate content'}

        except Exception as e:
            logging.error(f"{self.name} task processing failed: {e}")
            return {'error': str(e)}

    def _get_relevant_context(self, query: str) -> str:
        """Get relevant context from knowledge base"""
        relevant = self.db.get_knowledge(query, limit=2)
        if relevant:
            context = "Relevant information:\n"
            for item in relevant:
                context += f"- {item['query']}: {item['content'][:200]}...\n"
            return context
        return "No relevant context found."

    def _run_loop(self):
        """Main execution loop for content generation"""
        while self.running:
            try:
                # Look for content generation tasks
                pending_tasks = self.db.get_pending_tasks(limit=5)

                for task in pending_tasks:
                    if task['type'] == self.content_type or task['type'] == 'general':
                        result = self.process_task(task)
                        if result.get('success'):
                            self.db.update_task_status(task['id'], 'completed')
                            logging.info(f"{self.name} completed task {task['id']}")
                        else:
                            self.db.update_task_status(task['id'], 'failed')
                            logging.warning(f"{self.name} failed task {task['id']}: {result.get('error')}")

                # Health check every minute
                if not self._health_check():
                    logging.warning(f"{self.name} health check failed")

            except Exception as e:
                logging.error(f"{self.name} run loop error: {e}")

            time.sleep(30)  # Check every 30 seconds

class CodeGeneratorAI(BaseAI):
    """Base class for code generation AIs"""

    def __init__(self, db_manager, config):
        super().__init__(db_manager, config)
        self.content_type = "code_generation"

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process code generation task"""
        try:
            prompt = task.get('content', '')
            if not prompt:
                return {'error': 'No code specification provided'}

            # Enhance prompt for code generation
            code_prompt = f"""You are an expert software developer. Generate high-quality, well-documented code based on this requirement:

{prompt}

Requirements:
- Use modern best practices
- Include comments and docstrings
- Handle edge cases and errors
- Follow clean code principles
- Make it production-ready

Generate only the code without any explanatory text around it:"""

            code = self._generate_response(code_prompt, max_tokens=2000)
            if code:
                # Save to knowledge base
                self.db.add_knowledge(prompt, f"```python\n{code}\n```")
                self.tasks_processed += 1
                self._log_activity()

                return {
                    'success': True,
                    'code': code,
                    'task_id': task.get('id')
                }
            else:
                return {'error': 'Failed to generate code'}

        except Exception as e:
            logging.error(f"{self.name} code generation failed: {e}")
            return {'error': str(e)}

    def _run_loop(self):
        """Main execution loop for code generation"""
        while self.running:
            try:
                # Look for code generation tasks
                pending_tasks = self.db.get_pending_tasks(limit=3)

                for task in pending_tasks:
                    if task['type'] == 'code_generation':
                        result = self.process_task(task)
                        if result.get('success'):
                            self.db.update_task_status(task['id'], 'completed')
                            logging.info(f"{self.name} completed code task {task['id']}")
                        else:
                            self.db.update_task_status(task['id'], 'failed')
                            logging.warning(f"{self.name} failed code task {task['id']}: {result.get('error')}")

            except Exception as e:
                logging.error(f"{self.name} code run loop error: {e}")

            time.sleep(45)  # Code generation is more intensive, so less frequent checks

class AnalysisAI(BaseAI):
    """Base class for analysis and optimization AIs"""

    def __init__(self, db_manager, config):
        super().__init__(db_manager, config)
        self.content_type = "analysis"

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis task"""
        try:
            content = task.get('content', '')
            if not content:
                return {'error': 'No content to analyze'}

            analysis_prompt = f"""Analyze this content and provide insights, improvements, and optimization suggestions:

{content}

Provide your analysis in the following format:
1. Summary (2-3 sentences)
2. Strengths
3. Areas for improvement
4. Actionable recommendations
5. Optimized version:"""

            analysis = self._generate_response(analysis_prompt, max_tokens=1500)
            if analysis:
                # Save analysis to knowledge base
                self.db.add_knowledge(f"Analysis of: {content[:100]}...", analysis)
                self.tasks_processed += 1
                self._log_activity()

                return {
                    'success': True,
                    'analysis': analysis,
                    'task_id': task.get('id')
                }
            else:
                return {'error': 'Analysis failed'}

        except Exception as e:
            logging.error(f"{self.name} analysis failed: {e}")
            return {'error': str(e)}

    def _run_loop(self):
        """Main execution loop for analysis"""
        while self.running:
            try:
                pending_tasks = self.db.get_pending_tasks(limit=5)

                for task in pending_tasks:
                    if task['type'] == 'analysis':
                        result = self.process_task(task)
                        if result.get('success'):
                            self.db.update_task_status(task['id'], 'completed')
                            logging.info(f"{self.name} completed analysis task {task['id']}")
                        else:
                            self.db.update_task_status(task['id'], 'failed')
                            logging.warning(f"{self.name} failed analysis task {task['id']}: {result.get('error')}")

            except Exception as e:
                logging.error(f"{self.name} analysis run loop error: {e}")

            time.sleep(60)  # Analysis is thoughtful work, check less frequently
