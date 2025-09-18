from kubernetes import client, config

# Use in-cluster ServiceAccount token
config.load_incluster_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def list_pods(namespace="default"):
    pods = v1.list_namespaced_pod(namespace)
    return [{"name": p.metadata.name, "status": p.status.phase} for p in pods]

def list_services(namespace="default"):
    svcs = v1.list_namespaced_service(namespace)
    return [{"name": s.metadata.name, "type": s.spec.type} for s in svcs]

def describe_pod(pod_name, namespace="default"):
    pods = v1.list_namespaced_pod(namespace)
    pod = next((p for p in pods.items if pod_name in p.metadata.name), None)
    if not pod:
        return f"Pod '{pod_name}' not found in {namespace}"
    return {
        "name": pod.metadata.name,
        "status": pod.status.phase,
        "containers": [c.name for c in pod.spec.containers]
    }

def get_pod_logs(pod_name, namespace="default"):
    try:
        return v1.read_namespaced_pod_log(pod_name, namespace)
    except Exception as e:
        return str(e)
