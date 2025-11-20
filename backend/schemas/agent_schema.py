"""Agent schemas for API."""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AgentConfigRequest(BaseModel):
    """Schema for agent configuration request."""
    agent_id: str
    name: str
    agent_type: str  # orchestrator, super, utility
    model: str
    task: Optional[str] = None


class AgentHierarchyRequest(BaseModel):
    """Schema for complete agent hierarchy configuration."""
    config_name: str
    orchestrator: AgentConfigRequest
    super_agents: List[AgentConfigRequest]
    utility_agents: List[AgentConfigRequest]
    connections: Dict[str, List[str]]  # super_agent_id -> [utility_agent_ids]


class AgentQueryRequest(BaseModel):
    """Schema for agent query request."""
    query: str
    patient_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AgentQueryResponse(BaseModel):
    """Schema for agent query response."""
    status: str
    final_response: Optional[str] = None
    super_agent_responses: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
