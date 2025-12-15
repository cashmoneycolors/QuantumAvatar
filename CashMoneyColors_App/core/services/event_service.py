#!/usr/bin/env python3
"""
EVENT SERVICE MODULE
Event-driven communication system for AI agents coordination
Allows AIs to communicate and trigger actions based on events
"""

import logging
from queue import Queue
from threading import Thread, Lock
from typing import Callable, Dict, List, Any
import time

class EventService:
    """Event-driven service for AI coordination"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_queue = Queue()
        self.lock = Lock()
        self.running = True

        # Start event processing thread
        self.processor_thread = Thread(target=self._process_events, daemon=True)
        self.processor_thread.start()

        # Event history for debugging
        self.event_history: List[Dict[str, Any]] = []
        self.max_history = 100

    def on(self, event_name: str, callback: Callable):
        """Register an event listener"""
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)
            logging.debug(f"Registered listener for event: {event_name}")

    def trigger(self, event_name: str, data: Any = None):
        """Trigger an event with optional data"""
        event = {
            'name': event_name,
            'data': data,
            'timestamp': time.time()
        }

        self.event_queue.put(event)

        # Keep event history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

    def _process_events(self):
        """Process events in background"""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self._handle_event(event)
                self.event_queue.task_done()
            except:
                # Timeout or empty queue, continue
                pass

    def _handle_event(self, event):
        """Handle individual event"""
        event_name = event['name']
        data = event.get('data')

        logging.debug(f"Processing event: {event_name}")

        with self.lock:
            if event_name in self.listeners:
                for callback in self.listeners[event_name]:
                    try:
                        Thread(target=callback, args=(data,), daemon=True).start()
                    except Exception as e:
                        logging.error(f"Error calling event callback: {e}")

    def get_event_history(self, limit: int = 10):
        """Get recent event history"""
        return self.event_history[-limit:]

    def clear_event_history(self):
        """Clear event history"""
        self.event_history = []

    def shutdown(self):
        """Shutdown event service"""
        self.running = False
        if self.processor_thread.is_alive():
            self.processor_thread.join(timeout=2)
