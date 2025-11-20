"""Agent configuration data models."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AgentConfigModel(BaseModel):
    """Configuration for a single agent."""
    agent_id: str
    name: str
    agent_type: str  # "orchestrator", "super", "utility"
    model: str = "gemini-2.0-flash-exp"
    task: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentHierarchyConfig(BaseModel):
    """Complete agent hierarchy configuration."""
    config_id: str
    name: str = "Default Configuration"
    orchestrator: AgentConfigModel
    super_agents: List[AgentConfigModel]
    utility_agents: List[AgentConfigModel]
    connections: Dict[str, List[str]]  # Maps super_agent_id -> [utility_agent_ids]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def validate_hierarchy(self) -> tuple[bool, str]:
        """
        Validate agent hierarchy rules:
        - Must have exactly 1 orchestrator
        - Each super agent must have at least 2 utility agents
        - All utility agents must be assigned to a super agent
        """
        # Check orchestrator
        if self.orchestrator.agent_type != "orchestrator":
            return False, "Orchestrator must have agent_type='orchestrator'"

        # Check super agents
        for sa in self.super_agents:
            if sa.agent_type != "super":
                return False, f"Super agent {sa.name} must have agent_type='super'"

            # Check connections
            utility_count = len(self.connections.get(sa.agent_id, []))
            if utility_count < 2:
                return False, f"Super agent {sa.name} must have at least 2 utility agents (has {utility_count})"

        # Check all utility agents are assigned
        assigned_utilities = set()
        for utilities in self.connections.values():
            assigned_utilities.update(utilities)

        all_utility_ids = {ua.agent_id for ua in self.utility_agents}
        unassigned = all_utility_ids - assigned_utilities

        if unassigned:
            return False, f"Some utility agents are not assigned: {unassigned}"

        return True, "Hierarchy is valid"


class AgentResponse(BaseModel):
    """Standard response from an agent."""
    agent_id: str
    agent_name: str
    agent_type: str
    status: str  # "success", "error", "processing"
    result: Dict[str, Any]
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
