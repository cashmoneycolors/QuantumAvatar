#!/usr/bin/env python3

import os
import requests
from .base_ai import BaseAI

class DeepSeekAI(BaseAI):
    """DeepSeek AI Integration"""

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def generate_response(self, prompt, max_tokens=1000, temperature=0.7):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': temperature
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']

    def is_available(self):
        return self.api_key is not None

    def get_model_name(self):
        return "DeepSeek"
