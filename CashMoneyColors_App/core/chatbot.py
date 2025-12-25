#!/usr/bin/env python3
"""
NEXUS CHATBOT MODULE
Intelligent conversation interface with multi-AI integration
Provides unified chat access to all AI capabilities
"""

try:
    from openai import OpenAI
    from anthropic import Anthropic
    import logging
    import time
    from datetime import datetime
    from .config import API_CONFIG
except ImportError as e:
    print(f"Import error in chatbot: {e}")
    # Mock implementations for missing imports
    class OpenAI:
        def __init__(self, *args, **kwargs):
            pass
        class Client:
            def __init__(self, *args, **kwargs):
                pass

    class Anthropic:
        def __init__(self, *args, **kwargs):
            pass

    API_CONFIG = type('obj', (object,), {})  # Mock config

class NexusChatbot:
    """Unified AI Chatbot Interface"""

    def __init__(self, database, api_config):
        self.db = database
        self.config = api_config
        self.conversation_history = []
        self.max_history = 50

        # Initialize AI clients (with error handling)
        self.clients = self._initialize_clients()

        # Track AI performance
        self.ai_performance = {
            'grok': {'calls': 0, 'success': 0, 'response_time': []},
            'claude': {'calls': 0, 'success': 0, 'response_time': []}
        }

    def _initialize_clients(self):
        """Initialize all AI clients"""
        clients = {}

        try:
            if hasattr(API_CONFIG, 'grok_key') and API_CONFIG.grok_key:
                clients['grok'] = OpenAI(
                    api_key=API_CONFIG.grok_key,
                    base_url="https://api.x.ai/v1"
                )
        except Exception as e:
            logging.warning(f"Failed to initialize Grok client: {e}")

        try:
            if hasattr(API_CONFIG, 'claude_key') and API_CONFIG.claude_key:
                clients['claude'] = Anthropic(api_key=API_CONFIG.claude_key)
        except Exception as e:
            logging.warning(f"Failed to initialize Claude client: {e}")

        return clients

    def process_query(self, user_query):
        """Process user query and return response"""
        try:
            start_time = time.time()

            # Get context from database
            context = self._get_context(user_query)

            # Determine which AI to use
            ai_choice = self._select_ai(user_query)

            # Get response from selected AI
            response = self._get_ai_response(ai_choice, user_query, context)

            # Optimize response with Claude if available
            if 'claude' in self.clients and ai_choice != 'claude':
                response = self._optimize_response(response, user_query)

            # Save conversation to history
            self._save_conversation(user_query, response)

            # Update database with new knowledge
            self._update_knowledge(user_query, response)

            # Track performance
            response_time = time.time() - start_time
            self.ai_performance[ai_choice]['calls'] += 1
            self.ai_performance[ai_choice]['response_time'].append(response_time)
            if len(self.ai_performance[ai_choice]['response_time']) > 10:
                self.ai_performance[ai_choice]['response_time'].pop(0)

            return response

        except Exception as e:
            logging.error(f"Error processing query: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."

    def _get_context(self, query):
        """Get relevant context from database"""
        if not self.db:
            return ""

        try:
            # Get relevant knowledge from database
            knowledge = self.db.search_knowledge(query.lower(), limit=5)
            context = "\n".join([f"- {k['content']}" for k in knowledge])

            return f"Context from Nexus:\n{context}\n\n"
        except Exception as e:
            logging.warning(f"Could not get context: {e}")
            return ""

    def _select_ai(self, query):
        """Select appropriate AI based on query characteristics"""
        query_lower = query.lower()

        # Analyze query to determine best AI
        if any(word in query_lower for word in ['code', 'programming', 'script', 'function']):
            return 'deepseek' if 'deepseek' in self.clients else 'grok'

        elif any(word in query_lower for word in ['analyze', 'optimize', 'improve', 'review']):
            return 'claude' if 'claude' in self.clients else 'grok'

        else:
            return 'grok' if 'grok' in self.clients else ('claude' if 'claude' in self.clients else None)

    def _get_ai_response(self, ai_choice, query, context):
        """Get response from selected AI"""
        if ai_choice == 'grok' and 'grok' in self.clients:
            prompt = f"{context}User question: {query}\n\nPlease provide a comprehensive and helpful response."
            return self._call_grok_api(prompt)

        elif ai_choice == 'claude' and 'claude' in self.clients:
            return self._call_claude_api(query, context)

        else:
            return "No available AI services at the moment."

    def _call_grok_api(self, prompt):
        """Call Grok API"""
        try:
            response = self.clients['grok'].chat.completions.create(
                model="grok-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Grok API call failed: {e}")
            return "I'm experiencing issues with my knowledge systems."

    def _call_claude_api(self, query, context):
        """Call Claude API"""
        try:
            full_prompt = f"{context}\n\nUser Query: {query}\n\nProvide a detailed and helpful response."

            response = self.clients['claude'].messages.create(
                model="claude-3.5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": full_prompt}]
            )

            return response.content[0].text
        except Exception as e:
            logging.error(f"Claude API call failed: {e}")
            return "I'm experiencing technical difficulties with analysis systems."

    def _optimize_response(self, response, original_query):
        """Optimize response using Claude for better quality"""
        try:
            optimization_prompt = f"""
Original Query: {original_query}

Current Response: {response}

Please optimize this response to be more helpful, accurate, and engaging.
Ensure it addresses the query directly and provides value.
"""

            optimized = self.clients['claude'].messages.create(
                model="claude-3-haiku-20240307",  # Faster for optimization
                max_tokens=1500,
                messages=[{"role": "user", "content": optimization_prompt}]
            )

            return optimized.content[0].text

        except Exception as e:
            # Return original response if optimization fails
            return response

    def _save_conversation(self, query, response):
        """Save conversation to history"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response[:500]  # Truncate long responses
        }

        self.conversation_history.append(conversation)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def _update_knowledge(self, query, response):
        """Update database with new knowledge"""
        if self.db:
            try:
                # Extract key concepts and save them
                key_concepts = self._extract_key_concepts(query, response)
                for concept, info in key_concepts.items():
                    self.db.add_knowledge(concept.lower(), info)
            except Exception as e:
                logging.warning(f"Could not update knowledge: {e}")

    def _extract_key_concepts(self, query, response):
        """Extract key concepts from conversation"""
        concepts = {}

        # Simple keyword extraction (could be enhanced with NLP)
        important_words = ['pricing', 'strategy', 'code', 'marketing', 'content', 'revenue', 'ai', 'optimization']

        for word in important_words:
            if word in query.lower() or word in response.lower():
                concepts[word] = f"Information about {word}: {response[:300]}..."

        return concepts

    def get_performance_stats(self):
        """Get AI performance statistics"""
        stats = {
            'total_conversations': len(self.conversation_history),
            'ai_performance': {},
            'available_clients': list(self.clients.keys())
        }

        for ai_name, perf_data in self.ai_performance.items():
            if perf_data['calls'] > 0:
                avg_response_time = sum(perf_data['response_time']) / len(perf_data['response_time'])
                stats['ai_performance'][ai_name] = {
                    'calls': perf_data['calls'],
                    'avg_response_time': round(avg_response_time, 2),
                    'success_rate': perf_data['success'] / perf_data['calls']
                }

        return stats

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logging.info("Conversation history cleared")
