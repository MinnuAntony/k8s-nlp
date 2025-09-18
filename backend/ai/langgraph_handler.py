
# from ..k8s_client.client import list_pods, list_services, describe_pod, get_pod_logs
# from .bedrock_client import query_llm

# def ai_parse_and_execute(query, namespace="default"):
#     prompt = f"""
#     You are a Kubernetes assistant.
#     User query: '{query}'
#     Allowed actions: list_pods, list_services, describe_pod, get_pod_logs
#     Return structured output: action_name, resource_name (optional)
#     """
#     llm_output = query_llm(prompt).lower()

#     if "list pods" in llm_output:
#         result = list_pods(namespace)
#         explanation = f"Listing pods in namespace '{namespace}'"
#     elif "list services" in llm_output:
#         result = list_services(namespace)
#         explanation = f"Listing services in namespace '{namespace}'"
#     elif "describe pod" in llm_output:
#         pod_name = llm_output.split("pod_name:")[1].strip()
#         result = describe_pod(pod_name, namespace)
#         explanation = f"Description of pod '{pod_name}'"
#     elif "logs" in llm_output:
#         pod_name = llm_output.split("pod_name:")[1].strip()
#         result = get_pod_logs(pod_name, namespace)
#         explanation = f"Logs of pod '{pod_name}'"
#     else:
#         result = "Could not understand query"
#         explanation = "No action matched"

#     return explanation, result

from ..k8s_client.client import list_pods, list_services, describe_pod, get_pod_logs
from .bedrock_client import query_llm

def ai_parse_and_execute(query, namespace="default"):
    prompt = f"""
    You are a Kubernetes assistant.
    User query: '{query}'
    Allowed actions: list_pods, list_services, describe_pod, get_pod_logs
    Return structured output: action_name, resource_name (optional)
    """
    
    llm_output = query_llm(prompt)           # raw Claude output
    llm_output_lower = llm_output.lower()    # for parsing only

    if "list pods" in llm_output_lower:
        result = list_pods(namespace)
    elif "list services" in llm_output_lower:
        result = list_services(namespace)
    elif "describe pod" in llm_output_lower:
        pod_name = llm_output_lower.split("pod_name:")[1].strip()
        result = describe_pod(pod_name, namespace)
    elif "logs" in llm_output_lower:
        pod_name = llm_output_lower.split("pod_name:")[1].strip()
        result = get_pod_logs(pod_name, namespace)
    else:
        result = None  # or "No action matched"

    # ✅ return raw Claude text in explanation, and kubectl result if any
    return llm_output, result
