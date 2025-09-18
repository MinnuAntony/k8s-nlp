import os
import json
import boto3

# Bedrock runtime client
client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

MODEL = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-haiku-20240307-v1:0")

def query_llm(prompt: str) -> str:
    """
    Query AWS Bedrock Claude model and return string output.
    """
    body = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
        "max_tokens": 512
    }

    response = client.invoke_model(
        modelId=MODEL,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())

    # Claude responses are inside "content"
    if "output" in result:
        return result["output"]
    elif "content" in result:
        return result["content"][0]["text"]
    else:
        return json.dumps(result)
