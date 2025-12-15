#!/usr/bin/env python3
"""
DATABASE MANAGER MODULE
Manages SQLite database operations for the autonomous AI system
"""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

class NexusDatabase:
    """Advanced database for the AI Nexus system"""

    def __init__(self, db_path: str = 'data/nexus.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = None
        self.initialize_database()

    def initialize_database(self):
        """Initialize database with all required tables"""
        try:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.cursor = self.conn.cursor()

            # Create all tables
            self.cursor.executescript('''
                -- Knowledge base for AI learning
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(query, category)
                );

                -- Conversation history
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    response_time REAL,
                    satisfaction_rating INTEGER CHECK(satisfaction_rating >= 1 AND satisfaction_rating <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Task queue for AI agents
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'completed', 'failed')),
                    assigned_agent TEXT,
                    result TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Revenue tracking
                CREATE TABLE IF NOT EXISTS revenue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'EUR',
                    source TEXT NOT NULL,
                    description TEXT,
                    transaction_id TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- AI agent performance metrics
                CREATE TABLE IF NOT EXISTS agent_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    duration REAL,
                    success BOOLEAN DEFAULT TRUE,
                    tokens_used INTEGER,
                    cost REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_knowledge_query ON knowledge(query);
                CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge(category);
                CREATE INDEX IF NOT EXISTS idx_tasks_status_priority ON tasks(status, priority DESC);
                CREATE INDEX IF NOT EXISTS idx_conversations_created ON conversations(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_revenue_created ON revenue(created_at DESC);
            ''')

            self.conn.commit()
            logging.info(f"Nexus database initialized at {self.db_path}")

        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            raise

    # Knowledge Management Methods
    def add_knowledge(self, query: str, response: str, category: str = 'general',
                     confidence: float = 1.0) -> int:
        """Add knowledge entry to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO knowledge
                (query, response, category, confidence, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (query.lower().strip(), response.strip(), category.lower(), confidence))

            self.conn.commit()
            knowledge_id = self.cursor.lastrowid
            logging.debug(f"Added knowledge: {query[:50]}...")
            return knowledge_id

        except Exception as e:
            logging.error(f"Failed to add knowledge: {e}")
            self.conn.rollback()
            return -1

    def get_knowledge(self, query: str, limit: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant knowledge from database"""
        try:
            if category:
                self.cursor.execute('''
                    SELECT id, query, response, category, confidence, created_at
                    FROM knowledge
                    WHERE category = ? AND query LIKE ?
                    ORDER BY confidence DESC, created_at DESC
                    LIMIT ?
                ''', (category, f'%{query.lower()}%', limit))
            else:
                self.cursor.execute('''
                    SELECT id, query, response, category, confidence, created_at
                    FROM knowledge
                    WHERE query LIKE ?
                    ORDER BY confidence DESC, created_at DESC
                    LIMIT ?
                ''', (f'%{query.lower()}%', limit))

            results = self.cursor.fetchall()
            return [{
                'id': row[0],
                'query': row[1],
                'content': row[2],
                'category': row[3],
                'confidence': row[4],
                'created_at': row[5]
            } for row in results]

        except Exception as e:
            logging.error(f"Failed to retrieve knowledge: {e}")
            return []

    def update_knowledge_confidence(self, knowledge_id: int, new_confidence: float):
        """Update confidence score of knowledge entry"""
        try:
            self.cursor.execute(
                'UPDATE knowledge SET confidence = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (new_confidence, knowledge_id)
            )
            self.conn.commit()
        except Exception as e:
            logging.error(f"Failed to update knowledge confidence: {e}")

    # Task Management Methods
    def create_task(self, task_type: str, content: str, priority: int = 1) -> int:
        """Create a new task for AI agents"""
        try:
            self.cursor.execute(
                'INSERT INTO tasks (task_type, content, priority) VALUES (?, ?, ?)',
                (task_type, content, priority)
            )
            self.conn.commit()
            task_id = self.cursor.lastrowid
            logging.info(f"Created task {task_id}: {task_type}")
            return task_id
        except Exception as e:
            logging.error(f"Failed to create task: {e}")
            return -1

    def get_pending_tasks(self, limit: int = 10, task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get pending tasks ordered by priority"""
        try:
            if task_type:
                self.cursor.execute('''
                    SELECT id, task_type, content, priority, created_at
                    FROM tasks
                    WHERE status = 'pending' AND task_type = ?
                    ORDER BY priority DESC, created_at ASC
                    LIMIT ?
                ''', (task_type, limit))
            else:
                self.cursor.execute('''
                    SELECT id, task_type, content, priority, created_at
                    FROM tasks
                    WHERE status = 'pending'
                    ORDER BY priority DESC, created_at ASC
                    LIMIT ?
                ''', (limit,))

            results = self.cursor.fetchall()
            return [{
                'id': row[0],
                'type': row[1],
                'content': row[2],
                'priority': row[3],
                'created_at': row[4]
            } for row in results]

        except Exception as e:
            logging.error(f"Failed to get pending tasks: {e}")
            return []

    def update_task_status(self, task_id: int, status: str,
                          assigned_agent: Optional[str] = None,
                          result: Optional[str] = None,
                          error_message: Optional[str] = None):
        """Update task status and related information"""
        try:
            self.cursor.execute('''
                UPDATE tasks
                SET status = ?, assigned_agent = ?, result = ?,
                    error_message = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, assigned_agent, result, error_message, task_id))
            self.conn.commit()
            logging.debug(f"Updated task {task_id} to status: {status}")
        except Exception as e:
            logging.error(f"Failed to update task status: {e}")

    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get specific task by ID"""
        try:
            self.cursor.execute('''
                SELECT id, task_type, content, priority, status,
                       assigned_agent, result, error_message, created_at, updated_at
                FROM tasks WHERE id = ?
            ''', (task_id,))

            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'type': row[1],
                    'content': row[2],
                    'priority': row[3],
                    'status': row[4],
                    'assigned_agent': row[5],
                    'result': row[6],
                    'error_message': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                }
        except Exception as e:
            logging.error(f"Failed to get task {task_id}: {e}")
        return None

    # Conversation Management
    def save_conversation(self, user_query: str, ai_response: str,
                         response_time: float = 0.0, satisfaction: Optional[int] = None):
        """Save conversation to history"""
        try:
            self.cursor.execute(
                'INSERT INTO conversations (user_query, ai_response, response_time, satisfaction_rating) VALUES (?, ?, ?, ?)',
                (user_query, ai_response, response_time, satisfaction)
            )
            self.conn.commit()
        except Exception as e:
            logging.error(f"Failed to save conversation: {e}")

    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        try:
            self.cursor.execute('''
                SELECT id, user_query, ai_response, response_time, satisfaction_rating, created_at
                FROM conversations
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            results = self.cursor.fetchall()
            return [{
                'id': row[0],
                'user_query': row[1][:100] + '...' if len(row[1]) > 100 else row[1],
                'ai_response': row[2][:100] + '...' if len(row[2]) > 100 else row[2],
                'response_time': row[3],
                'satisfaction': row[4],
                'created_at': row[5]
            } for row in results]

        except Exception as e:
            logging.error(f"Failed to get conversation history: {e}")
            return []

    # Revenue and Analytics
    def log_revenue(self, amount: float, source: str, description: str = "",
                   currency: str = 'EUR', transaction_id: Optional[str] = None) -> int:
        """Log revenue transaction"""
        try:
            self.cursor.execute(
                'INSERT INTO revenue (amount, currency, source, description, transaction_id) VALUES (?, ?, ?, ?, ?)',
                (amount, currency, source, description, transaction_id)
            )
            self.conn.commit()
            revenue_id = self.cursor.lastrowid
            logging.info(f"Logged revenue: {amount} {currency} from {source}")
            return revenue_id
        except Exception as e:
            logging.error(f"Failed to log revenue: {e}")
            return -1

    def get_revenue_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue statistics"""
        try:
            # Total revenue
            self.cursor.execute('SELECT SUM(amount) FROM revenue')
            total_revenue = self.cursor.fetchone()[0] or 0.0

            # Revenue by source
            self.cursor.execute('SELECT source, SUM(amount) FROM revenue GROUP BY source')
            revenue_by_source = dict(self.cursor.fetchall())

            # Recent revenue (last N days)
            self.cursor.execute('''
                SELECT SUM(amount) FROM revenue
                WHERE created_at >= datetime('now', '-{} days')
            '''.format(days))
            recent_revenue = self.cursor.fetchone()[0] or 0.0

            return {
                'total_revenue': total_revenue,
                'revenue_by_source': revenue_by_source,
                'recent_revenue_days': days,
                'recent_revenue': recent_revenue
            }

        except Exception as e:
            logging.error(f"Failed to get revenue stats: {e}")
            return {'total_revenue': 0, 'revenue_by_source': {}, 'recent_revenue': 0}

    # AI Metrics
    def log_agent_metric(self, agent_name: str, operation: str, duration: float,
                        success: bool = True, tokens_used: Optional[int] = None,
                        cost: Optional[float] = None):
        """Log AI agent performance metrics"""
        try:
            self.cursor.execute(
                'INSERT INTO agent_metrics (agent_name, operation, duration, success, tokens_used, cost) VALUES (?, ?, ?, ?, ?, ?)',
                (agent_name, operation, duration, success, tokens_used, cost)
            )
            self.conn.commit()
        except Exception as e:
            logging.error(f"Failed to log agent metric: {e}")

    def get_agent_performance(self, agent_name: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
        """Get AI agent performance statistics"""
        try:
            if agent_name:
                self.cursor.execute('''
                    SELECT
                        COUNT(*) as total_operations,
                        AVG(duration) as avg_duration,
                        SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
                        SUM(tokens_used) as total_tokens,
                        SUM(cost) as total_cost
                    FROM agent_metrics
                    WHERE agent_name = ? AND created_at >= datetime('now', '-{} days')
                '''.format(days), (agent_name,))
            else:
                self.cursor.execute('''
                    SELECT
                        agent_name,
                        COUNT(*) as total_operations,
                        AVG(duration) as avg_duration,
                        SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
                        SUM(tokens_used) as total_tokens,
                        SUM(cost) as total_cost
                    FROM agent_metrics
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY agent_name
                '''.format(days))

            results = self.cursor.fetchall()
            if not results:
                return {}

            if agent_name:
                row = results[0]
                return {
                    'agent_name': agent_name,
                    'total_operations': row[0],
                    'avg_duration': row[1],
                    'success_rate': row[2],
                    'total_tokens': row[3] or 0,
                    'total_cost': row[4] or 0
                }
            else:
                return {
                    agent_row[0]: {
                        'total_operations': agent_row[1],
                        'avg_duration': agent_row[2],
                        'success_rate': agent_row[3],
                        'total_tokens': agent_row[4] or 0,
                        'total_cost': agent_row[5] or 0
                    }
                    for agent_row in results
                }

        except Exception as e:
            logging.error(f"Failed to get agent performance: {e}")
            return {}

    # System Statistics
    def get_stats(self) -> Dict[str, Any]:
        """Get overall system statistics (Aliased for compatibility)"""
        return self.get_system_stats()

    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search knowledge base (for UI compatibility)"""
        return self.get_knowledge(query, limit)

    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        try:
            stats = {}

            # Knowledge stats
            self.cursor.execute('SELECT COUNT(*), COUNT(DISTINCT category) FROM knowledge')
            knowledge_count, category_count = self.cursor.fetchone()
            stats['knowledge_entries'] = knowledge_count
            stats['knowledge_categories'] = category_count

            # Task stats
            self.cursor.execute('''
                SELECT
                    COUNT(*),
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)
                FROM tasks
            ''')
            total_tasks, pending, completed, failed = self.cursor.fetchone()
            stats['total_tasks'] = total_tasks
            stats['pending_tasks'] = pending
            stats['completed_tasks'] = completed
            stats['failed_tasks'] = failed

            # Conversation stats
            self.cursor.execute('SELECT COUNT(*), AVG(response_time), AVG(satisfaction_rating) FROM conversations')
            conv_count, avg_response_time, avg_satisfaction = self.cursor.fetchone()
            stats['total_conversations'] = conv_count
            stats['avg_response_time'] = avg_response_time or 0
            stats['avg_satisfaction'] = avg_satisfaction or 0

            # Revenue stats
            revenue_stats = self.get_revenue_stats()
            stats.update(revenue_stats)

            return stats

        except Exception as e:
            logging.error(f"Failed to get system stats: {e}")
            return {}

    # Maintenance Methods
    def cleanup_old_entries(self, days: int = 90):
        """Clean up old entries to maintain database size"""
        try:
            cutoff_date = f"datetime('now', '-{days} days')"

            # Clean old conversations (keep last 1000)
            self.cursor.execute('DELETE FROM conversations WHERE id NOT IN (SELECT id FROM conversations ORDER BY created_at DESC LIMIT 1000)')

            # Clean old task results but keep metadata
            self.cursor.execute(f'UPDATE tasks SET result = NULL WHERE status IN ("completed", "failed") AND updated_at < {cutoff_date}')

            self.conn.commit()
            logging.info(f"Cleaned up entries older than {days} days")

        except Exception as e:
            logging.error(f"Failed to cleanup old entries: {e}")

    def backup_database(self, backup_path: str):
        """Create database backup"""
        try:
            backup_conn = sqlite3.connect(backup_path)
            self.conn.backup(backup_conn)
            backup_conn.close()
            logging.info(f"Database backup created: {backup_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to create backup: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Global database instance for easy access
database_manager = NexusDatabase()

def get_database() -> NexusDatabase:
    """Get the global database manager instance"""
    return database_manager
