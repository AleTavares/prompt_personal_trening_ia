import re
import json
import boto3
import requests
from botocore.config import Config

config = Config(
    retries = dict(
        max_attempts = 10
    )
)

AWS_REGION = 'us-east-1' # Região onde o Modelo Base foi liberado
MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0' # Id do Modelo a ser utilizado
MODEL_TEMPERATURE = 0.0
SEC_COMPANY = 'my-company'
SEC_EMAIL = 'my-email@my-company.com'
REPORTS_DIR = 'reports'

aws_access_key_id = "Coloque aqui sua ACCESS KY"
aws_secret_access_key = "Coloque aqui sua SECRET ACCESS KEY"


session = boto3.Session(
     region_name=AWS_REGION, 
     aws_access_key_id=aws_access_key_id, 
     aws_secret_access_key=aws_secret_access_key,
)

bedrock = session.client(
    service_name='bedrock-runtime'
    )


def call_bedrock(prompt):
    with open('../Prompt/prompt.md', 'rb') as input_file:
        input_file_bytes = input_file.read()
        message = {
            'role': 'user',
            'content': [
                {'text': prompt},
                {
                    'document': {
                        'name': 'Financial results report',
                        'format': 'md',
                        'source': {
                            'bytes': input_file_bytes
                        }
                    }
                },
            ]
        }
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[message],
            inferenceConfig={
                'temperature': MODEL_TEMPERATURE,
                'maxTokens': 1000
            },
        )
    content = response['output']['message']['content'][0]['text']
    print(content)
    return content, response['usage']['inputTokens'], response['usage']['outputTokens']

def geraTreino(biotipo, periodização, tipo):
    prompt = f'''
    Variaveis:\n
    biotipo = {biotipo}\n
    periodização = {periodização}\n
    tipo = {tipo}
    '''
    response, input_tokens, output_tokens = call_bedrock(prompt)
    bullet_points = '\n'.join([f'- {bullet}' for bullet in json.loads(response)['summary']])
    bullet_points = bullet_points.replace("$", "\\$")
    token_info = f'Input tokens: {input_tokens}, Output tokens: {output_tokens}'
    return bullet_points, token_info
