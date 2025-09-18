import os
import boto3

# Read AWS credentials from env (via K8s Secret)
client = boto3.client(
    "bedrock",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
MODEL = os.getenv("BEDROCK_MODEL", "anthropic.claude-v3")

def query_llm(prompt: str) -> str:
    response = client.invoke_model(
        modelId=MODEL,
        body=prompt.encode("utf-8"),
        contentType="text/plain"
    )
    return response["body"].read().decode("utf-8")
