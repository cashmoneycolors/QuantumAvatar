#!/usr/bin/env python3
"""
HELPERS UTILITIES MODULE
Provides utility functions for the autonomous AI system
"""

import os
import time
import traceback
import functools
from typing import Any, Callable, Optional, List, Dict
from pathlib import Path
import json

def safe_execute(func: Callable, *args, **kwargs) -> Optional[Any]:
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Safe execute failed for {func.__name__}: {e}")
        traceback.print_exc()
        return None

def create_directories(dirs: List[str]):
    """Create directories if they don't exist"""
    for dir_path in dirs:
        Path(dir_path).mkdir(exist_ok=True, parents=True)

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration dictionary"""
    required_keys = ['GROK_API_KEY']

    missing_keys = []
    for key in required_keys:
        if key not in config or not config[key]:
            missing_keys.append(key)

    if missing_keys:
        print(f"Missing configuration keys: {missing_keys}")
        return False

    return True

def format_currency(amount: float, currency: str = 'EUR') -> str:
    """Format currency amount"""
    return ".2f"

def generate_timestamp() -> str:
    """Generate ISO timestamp string"""
    from datetime import datetime
    return datetime.now().isoformat()

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        text = str(text)
    return text.strip()[:max_length]

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Failed to load JSON file {file_path}: {e}")
        return None

def save_json_file(file_path: str, data: Dict[str, Any]):
    """Save JSON file safely"""
    try:
        Path(file_path).parent.mkdir(exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save JSON file {file_path}: {e}")

def measure_execution_time(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            print(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            print(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    return wrapper

class ErrorHandler:
    """Central error handling class"""

    @staticmethod
    def handle_error(error: Exception, context: str = ""):
        """Handle and log errors"""
        error_msg = f"Error in {context}: {error}" if context else f"Error: {error}"
        print(error_msg)
        traceback.print_exc()

    @staticmethod
    def handle_ai_error(error: Exception, agent_name: str):
        """Handle AI-specific errors"""
        print(f"AI Agent {agent_name} error: {error}")
        traceback.print_exc()

class PerformanceMonitor:
    """Monitor performance of operations"""

    def __init__(self):
        self.operations = {}

    def start_operation(self, name: str):
        """Start timing an operation"""
        self.operations[name] = time.perf_counter()

    def end_operation(self, name: str) -> float:
        """End timing and return duration"""
        if name in self.operations:
            duration = time.perf_counter() - self.operations[name]
            del self.operations[name]
            return duration
        return 0.0

    def get_operation_time(self, name: str) -> float:
        """Get current operation time without ending it"""
        if name in self.operations:
            return time.perf_counter() - self.operations[name]
        return 0.0

# Global performance monitor
performance_monitor = PerformanceMonitor()

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retry functionality"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        print(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def chunk_text(text: str, chunk_size: int = 4000) -> List[str]:
    """Split text into chunks for API processing"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end

    return chunks

def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix

def clean_response_text(text: str) -> str:
    """Clean AI response text"""
    # Remove excessive whitespace
    text = ' '.join(text.split())

    # Remove common AI artifacts
    artifacts = [
        "As an AI",
        "I am an AI",
        "As Grok",
        "Here's the information",
        "Let me help you"
    ]

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        if any(artifact.lower() in line.lower() for artifact in artifacts) and len(line.strip()) < 100:
            continue  # Skip introductory lines
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate basic similarity between two texts"""
    # Simple Jaccard similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 and not words2:
        return 1.0

    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    return intersection / union if union > 0 else 0.0

class RateLimiter:
    """Rate limiting utility"""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.minute_window = 60

    def can_make_call(self) -> bool:
        """Check if a call can be made"""
        now = time.time()

        # Remove calls outside the window
        self.calls = [call_time for call_time in self.calls
                     if now - call_time < self.minute_window]

        return len(self.calls) < self.calls_per_minute

    def record_call(self):
        """Record a call"""
        self.calls.append(time.time())

    def get_remaining_calls(self) -> int:
        """Get remaining calls in current window"""
        now = time.time()
        self.calls = [call_time for call_time in self.calls
                     if now - call_time < self.minute_window]

        return self.calls_per_minute - len(self.calls)

    def wait_for_call(self):
        """Wait until a call can be made"""
        if not self.can_make_call():
            now = time.time()
            oldest_call = min(self.calls) if self.calls else now
            wait_time = self.minute_window - (now - oldest_call)
            if wait_time > 0:
                time.sleep(min(wait_time, 10))  # Max wait 10 seconds

# Global rate limiter for API calls
api_rate_limiter = RateLimiter(calls_per_minute=60)

def safe_api_call(func: Callable, *args, **kwargs):
    """Make a rate-limited API call"""
    if not api_rate_limiter.can_make_call():
        api_rate_limiter.wait_for_call()

    try:
        result = func(*args, **kwargs)
        api_rate_limiter.record_call()
        return result
    except Exception as e:
        print(f"API call failed: {e}")
        return None

class ConfigManager:
    """Manage application configuration"""

    def __init__(self, config_file: str = 'config.json', default_config: Optional[Dict] = None):
        self.config_file = config_file

        self.default_config = default_config or {
            'GROK_API_KEY': '',
            'DEEPSEEK_API_KEY': '',
            'BLACKBOX_API_KEY': '',
            'CLAUDE_API_KEY': '',
            'STRIPE_API_KEY': '',
            'GMAIL_CREDENTIALS': 'credentials.json',
            'LOG_LEVEL': 'INFO',
            'DB_PATH': 'data/nexus.db',
            'AUTO_START_AGENTS': True,
            'RATE_LIMIT_CALLS_PER_MINUTE': 60
        }

        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        config_data = load_json_file(self.config_file)

        if config_data:
            # Merge with defaults
            merged_config = self.default_config.copy()
            merged_config.update(config_data)
            return merged_config

        return self.default_config.copy()

    def save_config(self):
        """Save current configuration to file"""
        save_json_file(self.config_file, self.config)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

    def validate(self) -> bool:
        """Validate configuration"""
        return validate_config(self.config)

# Global configuration manager
config_manager = ConfigManager()
