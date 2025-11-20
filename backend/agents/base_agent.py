"""Base agent class for all agent types."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        agent_id: str = None,
        name: str = "",
        model: str = "gemini-2.0-flash-exp",
        task: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize base agent."""
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name
        self.model = model
        self.task = task
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.status = "initialized"

    @abstractmethod
    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task - must be implemented by subclasses."""
        pass

    def log_activity(self, activity: str, details: Dict[str, Any]):
        """Log agent activity."""
        log_entry = {
            "agent_id": self.agent_id,
            "name": self.name,
            "activity": activity,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        # This will be sent to Kafka topic for agent logs
        return log_entry

    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "model": self.model,
            "task": self.task,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }

    def update_status(self, status: str):
        """Update agent status."""
        self.status = status
        self.log_activity("status_change", {"new_status": status})
