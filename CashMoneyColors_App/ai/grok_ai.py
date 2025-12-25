#!/usr/bin/env python3
"""
GROK AI AGENT MODULE
Specialized AI agent for strategic thinking and content generation using Grok
"""

import time
import logging
from openai import OpenAI
from typing import Dict, Any, Optional

from .base_ai import ContentGeneratorAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import safe_execute, measure_execution_time

class GrokAI(ContentGeneratorAI):
    """Grok AI Agent for content generation and strategic planning"""

    def __init__(self, db_manager, config: Dict[str, Any]):
        super().__init__(db_manager, config)
        self.name = "Grok"

        # Initialize Grok client
        try:
            self.client = OpenAI(
                api_key=config.get('GROK_API_KEY'),
                base_url="https://api.x.ai/v1"
            )
            self.default_model = "grok-4"
            logging.info("Grok AI client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Grok client: {e}")
            self.client = None

    def _generate_response(self, prompt: str, model: str = None, **kwargs) -> str:
        """Generate response using Grok AI"""
        if not self.client:
            return "Grok AI client not available. Please check API key configuration."

        try:
            # Prepare request
            request_params = {
                'model': model or self.default_model,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 1000,
                **kwargs
            }

            # Make API call with error handling
            response = safe_execute(
                self.client.chat.completions.create,
                **request_params
            )

            if response and hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            else:
                return "I apologize, but Grok couldn't generate a response at this time."

        except Exception as e:
            logging.error(f"Grok API error: {e}")
            return f"Error communicating with Grok AI: {str(e)}"

    @measure_execution_time
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a content generation or strategic task using Grok"""

        result = super().process_task(task)

        if result.get('success'):
            # Add Grok-specific enhancements
            content = result.get('content', '')

            # If task requires strategic thinking, add that context
            if task.get('type') == 'strategic_planning':
                enhanced_content = self._enhance_strategic_content(content)
                result['content'] = enhanced_content

            # If task is content generation, add viral optimization
            elif task.get('type') == 'content_generation':
                viral_content = self._optimize_for_virality(content)
                result['content'] = viral_content

        return result

    def _enhance_strategic_content(self, content: str) -> str:
        """Enhance content with strategic thinking"""
        strategic_prompt = f"""
As a strategic AI advisor, analyze and enhance the following plan:

{content}

Provide a more strategic version that includes:
- SWOT analysis
- Risk assessment
- Revenue projections
- Scalability considerations
- Exit strategy

Strategic Enhancement:"""

        strategic_enhancement = self._generate_response(strategic_prompt, max_tokens=1500)
        return f"{content}\n\n--- STRATEGIC ENHANCEMENT ---\n{strategic_enhancement}"

    def _optimize_for_virality(self, content: str) -> str:
        """Optimize content for maximum engagement and virality"""
        viral_prompt = f"""
Optimize the following content for maximum virality and engagement:

{content}

Make it more:
- Attention-grabbing (better hook)
- Shareable (emotional triggers)
- Valuable (unique insights)
- Action-oriented (clear CTAs)
- Platform-optimized (formatted for social media)

Viral-Optimized Version:"""

        viral_optimization = self._generate_response(viral_prompt, max_tokens=1200)
        return f"{viral_optimization}"

    def generate_marketing_copy(self, product: str, target_audience: str,
                              unique_selling_point: str) -> str:
        """Generate marketing copy for a product"""
        copy_prompt = f"""
Create compelling marketing copy for:

Product: {product}
Target Audience: {target_audience}
Unique Selling Point: {unique_selling_point}

Requirements:
- Attention-grabbing headline
- Problem-solution-benefit structure
- Social proof elements
- Clear call-to-action
- Under 1500 characters

Marketing Copy:"""

        return self._generate_response(copy_prompt, max_tokens=800)

    def analyze_market_trends(self, industry: str, timeframe: str = "6 months") -> str:
        """Analyze market trends in a specific industry"""
        analysis_prompt = f"""
As a market intelligence expert, analyze current and future trends in the {industry} industry for the next {timeframe}:

Cover:
1. Current market state
2. Emerging technologies
3. Consumer behavior changes
4. Competitive landscape
5. Growth opportunities
6. Potential disruptions
7. Investment recommendations

Industry Analysis:"""

        return self._generate_response(analysis_prompt, max_tokens=2000)

    def brainstorm_business_ideas(self, interests: str, budget: str, skills: str) -> str:
        """Brainstorm business ideas based on user's interests and resources"""
        brainstorm_prompt = f"""
Based on the following user profile, brainstorm 5 high-potential business ideas:

Interests: {interests}
Budget: {budget}
Skills: {skills}

For each idea provide:
- Business concept
- Target market
- Revenue model
- Competitive advantage
- Initial investment needed
- Growth potential
- Profit timeline

Business Ideas:"""

        return self._generate_response(brainstorm_prompt, max_tokens=1800)

    def optimize_social_content(self, platform: str, content: str, goal: str = "engagement") -> str:
        """Optimize content for specific social media platforms"""
        optimize_prompt = f"""
Optimize this content for {platform} to maximize {goal}:

{content}

Platform-Specific Optimizations for {platform}:
- Format best practices
- Hashtag strategy
- Timing recommendations
- Engagement hooks
- Platform-specific language
- Visual element suggestions

Optimized Content:"""

        return self._generate_response(optimize_prompt, max_tokens=1000)

    def _run_loop(self):
        """Main execution loop for Grok AI"""
        while self.running:
            try:
                # Look for pending tasks
                pending_tasks = self.db.get_pending_tasks(limit=3)

                for task in pending_tasks:
                    if task['type'] in ['content_generation', 'strategic_planning',
                                       'marketing', 'analysis', 'general_content']:

                        # Mark task as processing
                        self.db.update_task_status(task['id'], 'processing', assigned_agent=self.name)

                        # Process the task
                        result = self.process_task(task)

                        if result.get('success'):
                            self.db.update_task_status(
                                task['id'],
                                'completed',
                                assigned_agent=self.name,
                                result=result.get('content'),
                            )
                            logging.info(f"Grok completed task {task['id']}")
                        else:
                            self.db.update_task_status(
                                task['id'],
                                'failed',
                                assigned_agent=self.name,
                                error_message=result.get('error', 'Unknown error'),
                            )
                            logging.error(f"Grok failed task {task['id']}: {result.get('error')}")

            except Exception as e:
                logging.error(f"Grok AI run loop error: {e}")

            # Sleep between task checks (Grok is thoughtful and strategic)
            time.sleep(45)  # Longer pause for strategic thinking

    def get_status(self):
        """Get Grok AI status with additional metrics"""
        status = super().get_status()

        # Add Grok-specific status info
        status.update({
            'model': 'Grok-4 (xAI)',
            'specializations': ['Strategic Planning', 'Content Generation', 'Marketing', 'Analysis'],
            'thinking_style': 'Logical and strategic' if self.is_alive() else 'N/A',
            'knowledge_domains': ['Business Strategy', 'Marketing', 'AI Trends', 'Market Analysis']
        })

        return status

    # Specialized methods for different content types

    def create_thread_content(self, topic: str, audience: str, platform: str = "X") -> str:
        """Create viral thread content optimized for a specific platform"""
        thread_prompt = f"""
Create a compelling, viral-worthy thread about "{topic}" for {audience} on {platform}.

Requirements:
- 8-15 tweets total
- Strong hook to start
- Each tweet numbered correctly (1/14, 2/14, etc.)
- Build curiosity and value throughout
- End with strong call-to-action
- Include emojis appropriately for {platform}
- Platform-optimized formatting

Thread Content:"""

        return self._generate_response(thread_prompt, max_tokens=3000)

    def analyze_competitor_strategy(self, competitor: str, industry: str) -> str:
        """Analyze competitor's business strategy"""
        analysis_prompt = f"""
Perform a strategic analysis of {competitor} in the {industry} industry:

Analyze:
1. Business Model & Revenue Streams
2. Target Market & Positioning
3. Marketing Strategy & Branding
4. Competitive Advantages
5. Potential Weaknesses
6. Growth Strategy
7. Lessons for competitors

Strategic Analysis:"""

        return self._generate_response(analysis_prompt, max_tokens=2000)

    def forecast_trends(self, topic: str, horizon: str = "2026") -> str:
        """Forecast future trends in a topic or industry"""
        forecast_prompt = f"""
Forecast trends and developments in {topic} through {horizon}:

Include:
1. Technology advancements
2. Consumer behavior changes
3. Market dynamics shifts
4. Competitive landscape evolution
5. Regulatory changes
6. Opportunities and threats
7. Recommendations for preparation

Trend Forecast:"""

        return self._generate_response(forecast_prompt, max_tokens=2500)

    # Integration with the AI system

    def collaborate_with_agents(self, task_description: str) -> Dict[str, Any]:
        """Plan how to collaborate with other AI agents on a complex task"""
        collaboration_prompt = f"""
For this complex task: "{task_description}"

Design a collaboration strategy with other AI agents:
1. Task breakdown into subtasks
2. Agent assignments (DeepSeek for code, Blackbox for prototyping, Claude for analysis)
3. Sequential or parallel execution plan
4. Integration points
5. Quality assurance steps

Collaboration Plan:"""

        plan = self._generate_response(collaboration_prompt, max_tokens=1200)

        return {
            'task': task_description,
            'collaboration_plan': plan,
            'assigned_by': 'Grok',
            'timestamp': time.time()
        }
