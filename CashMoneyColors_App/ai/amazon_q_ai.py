#!/usr/bin/env python3

import os
import boto3
import json
from .base_ai import BaseAI

class AmazonQAI(BaseAI):
    """Amazon Q AI Integration via AWS Bedrock"""

    def __init__(self):
        super().__init__()
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        if self.access_key and self.secret_key:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=self.aws_region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
        else:
            self.client = None

    def generate_response(self, prompt, max_tokens=1000, temperature=0.7):
        if not self.client:
            raise Exception("AWS credentials not configured")

        # Using Amazon Q model (adjust model_id as needed)
        model_id = 'amazon.titan-text-lite-v1'
        # Or for Q: 'amazon.q-developer-v1' if available

        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    'inputText': prompt,
                    'textGenerationConfig': {
                        'maxTokenCount': max_tokens,
                        'temperature': temperature,
                        'topP': 0.9
                    }
                })
            )

            response_body = json.loads(response['body'].read())
            return response_body.get('results', [{}])[0].get('outputText', 'No response')

        except Exception as e:
            return f"Error with Amazon Q: {str(e)}"

    def is_available(self):
        return self.client is not None

    def get_model_name(self):
        return "Amazon Q"
