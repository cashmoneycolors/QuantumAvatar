#!/usr/bin/env python3
"""
LOGGING UTILITIES MODULE
Provides comprehensive logging functionality for the autonomous AI system
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

class QuantumLogger:
    """Enhanced logging system for quantum AI operations"""

    def __init__(self, log_directory: str = 'logs', log_level: str = 'INFO'):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)

        # Create formatters
        self.standard_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Configure log level
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        logging.getLogger().setLevel(numeric_level)

        # Create specialized loggers
        self.quantum_logger = logging.getLogger('quantum')
        self.ai_logger = logging.getLogger('ai')
        self.system_logger = logging.getLogger('system')

        # Setup handlers (after loggers are created)
        self.setup_handlers()

    def setup_handlers(self):
        """Setup logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.standard_formatter)
        logging.getLogger().addHandler(console_handler)

        # File handler for general logs
        general_log = self.log_directory / 'cashmoneycolors.log'
        file_handler = logging.handlers.RotatingFileHandler(
            general_log, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.detailed_formatter)
        logging.getLogger().addHandler(file_handler)

        # Error log handler
        error_log = self.log_directory / 'errors.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_log, maxBytes=5*1024*1024, backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self.detailed_formatter)
        logging.getLogger().addHandler(error_handler)

        # AI operations log
        ai_log = self.log_directory / 'ai_operations.log'
        ai_handler = logging.handlers.RotatingFileHandler(
            ai_log, maxBytes=20*1024*1024, backupCount=10
        )
        ai_handler.setLevel(logging.DEBUG)
        ai_handler.setFormatter(self.detailed_formatter)

        # Add to specific loggers
        self.ai_logger.addHandler(ai_handler)
        self.ai_logger.setLevel(logging.DEBUG)

    def quantum_operation(self, operation: str, agent: str = "", duration: float = 0,
                         success: bool = True, details: Optional[Dict[str, Any]] = None):
        """Log quantum AI operations"""
        message = f"OPERATION: {operation} | AGENT: {agent} | DURATION: {duration:.2f}s | SUCCESS: {success}"
        if details:
            message += f" | DETAILS: {details}"

        if success:
            self.quantum_logger.info(message)
        else:
            self.quantum_logger.error(message)

    def ai_interaction(self, agent: str, operation: str, input_data: Any,
                      output_data: Optional[Any] = None, tokens_used: Optional[int] = None,
                      cost: Optional[float] = None):
        """Log AI agent interactions"""
        message = f"AGENT: {agent} | OPERATION: {operation}"
        if tokens_used:
            message += f" | TOKENS: {tokens_used}"
        if cost:
            message += ".4f"

        # Truncate long inputs/outputs for logging
        input_str = str(input_data)[:500] + "..." if len(str(input_data)) > 500 else str(input_data)
        message += f" | INPUT: {input_str}"

        if output_data is not None:
            output_str = str(output_data)[:500] + "..." if len(str(output_data)) > 500 else str(output_data)
            message += f" | OUTPUT: {output_str}"

        self.ai_logger.info(message)

    def revenue_event(self, amount: float, source: str, description: str = ""):
        """Log revenue generation events"""
        message = f"REVENUE: €{amount:.2f} | SOURCE: {source}"
        if description:
            message += f" | DESCRIPTION: {description}"

        self.system_logger.info(message)

    def system_health(self, component: str, status: str, metrics: Optional[Dict[str, Any]] = None):
        """Log system health metrics"""
        message = f"HEALTH: {component} | STATUS: {status}"
        if metrics:
            message += f" | METRICS: {metrics}"

        if status.upper() == 'HEALTHY':
            self.system_logger.info(message)
        elif status.upper() == 'WARNING':
            self.system_logger.warning(message)
        else:
            self.system_logger.error(message)

    def task_lifecycle(self, task_id: int, task_type: str, status: str,
                      agent: Optional[str] = None, duration: Optional[float] = None):
        """Log task lifecycle events"""
        message = f"TASK: {task_id} | TYPE: {task_type} | STATUS: {status}"
        if agent:
            message += f" | AGENT: {agent}"
        if duration:
            message += ".2f"

        self.system_logger.info(message)

    def knowledge_update(self, query: str, category: str, operation: str):
        """Log knowledge base updates"""
        message = f"KNOWLEDGE: {operation} | CATEGORY: {category} | QUERY: {query[:100]}{'...' if len(query) > 100 else ''}"
        self.system_logger.info(message)

    def security_event(self, event: str, user: Optional[str] = None,
                      ip: Optional[str] = None, details: Optional[str] = None):
        """Log security-related events"""
        message = f"SECURITY: {event}"
        if user:
            message += f" | USER: {user}"
        if ip:
            message += f" | IP: {ip}"
        if details:
            message += f" | DETAILS: {details}"

        self.system_logger.warning(message)

    def performance_metric(self, component: str, metric: str, value: Any):
        """Log performance metrics"""
        message = f"PERFORMANCE: {component} | METRIC: {metric} | VALUE: {value}"
        self.system_logger.debug(message)

    def error_recovery(self, component: str, error: Exception, recovery_action: str,
                      success: bool = True):
        """Log error recovery attempts"""
        message = f"RECOVERY: {component} | ERROR: {str(error)} | ACTION: {recovery_action} | SUCCESS: {success}"
        if success:
            self.system_logger.info(message)
        else:
            self.system_logger.error(message)

class AICallTracker:
    """Track API calls and usage for different AI services"""

    def __init__(self, logger: QuantumLogger):
        self.logger = logger
        self.call_counts = {}
        self.token_usage = {}
        self.cost_tracking = {}

    def track_call(self, service: str, operation: str, tokens: Optional[int] = None,
                  cost: Optional[float] = None, success: bool = True):
        """Track an API call"""
        # Update call counts
        key = f"{service}:{operation}"
        self.call_counts[key] = self.call_counts.get(key, 0) + 1

        # Update token usage
        if tokens:
            self.token_usage[service] = self.token_usage.get(service, 0) + tokens

        # Update cost tracking
        if cost:
            self.cost_tracking[service] = self.cost_tracking.get(service, 0.0) + cost

        # Log the call
        self.logger.ai_interaction(
            agent=service,
            operation=operation,
            input_data={"call_count": self.call_counts[key]},
            tokens_used=tokens,
            cost=cost
        )

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            'call_counts': self.call_counts.copy(),
            'token_usage': self.token_usage.copy(),
            'cost_tracking': self.cost_tracking.copy(),
            'total_calls': sum(self.call_counts.values()),
            'total_tokens': sum(self.token_usage.values()),
            'total_cost': sum(self.cost_tracking.values())
        }

    def reset_tracking(self):
        """Reset all tracking counters"""
        self.call_counts.clear()
        self.token_usage.clear()
        self.cost_tracking.clear()
        self.logger.system_logger.info("API call tracking reset")

# Global logger instances
quantum_logger = QuantumLogger()
ai_call_tracker = AICallTracker(quantum_logger)

# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Get a named logger"""
    return logging.getLogger(name)

def log_quantum_operation(operation: str, **details):
    """Log a quantum operation"""
    quantum_logger.quantum_operation(operation, **details)

def log_ai_interaction(agent: str, operation: str, **details):
    """Log an AI interaction"""
    quantum_logger.ai_interaction(agent, operation, **details)

def log_revenue(amount: float, source: str, description: str = ""):
    """Log revenue"""
    quantum_logger.revenue_event(amount, source, description)

def log_system_health(component: str, status: str, **metrics):
    """Log system health"""
    quantum_logger.system_health(component, status, metrics)

def get_logger_instance(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return logging.getLogger(name)

def setup_logging(log_directory: str = 'logs', log_level: str = 'INFO'):
    """Setup logging system"""
    return QuantumLogger(log_directory, log_level)
