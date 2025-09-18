from pydantic import BaseModel

class K8sQueryRequest(BaseModel):
    query: str
    namespace: str = "default"

class K8sQueryResponse(BaseModel):
    explanation: str
    result: str
