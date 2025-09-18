from fastapi import APIRouter
from ..models.query_models import K8sQueryRequest, K8sQueryResponse
from ..ai.langgraph_handler import ai_parse_and_execute

router = APIRouter()

@router.post("/query", response_model=K8sQueryResponse)
def query_k8s(req: K8sQueryRequest):
    explanation, result = ai_parse_and_execute(req.query, req.namespace)
    return K8sQueryResponse(explanation=explanation, result=str(result))
