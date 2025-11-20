"""Utility Agent (Staff) - Executes specific tasks."""
from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from loguru import logger


class UtilityAgent(BaseAgent):
    """
    Utility Agent (Staff)
    - Executes specific tasks
    - Examples: Compare research, analyze vitals, check guidelines
    - Returns findings to super agent
    """

    VALID_TASKS = [
        "compare_external_research",
        "compare_internal_research",
        "study_patient_data",
        "study_individual_data",
        "study_medical_guidelines",
        "predict_deterioration"
    ]

    def __init__(
        self,
        agent_id: str = None,
        name: str = "UtilityAgent",
        model: str = "gemini-2.0-flash-exp",
        task: str = "study_patient_data",
        **kwargs
    ):
        """Initialize utility agent."""
        if task not in self.VALID_TASKS:
            logger.warning(f"Unknown task '{task}', defaulting to 'study_patient_data'")
            task = "study_patient_data"

        super().__init__(agent_id=agent_id, name=name, model=model, task=task, **kwargs)

    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute utility agent task based on assigned task type.
        """
        self.update_status("processing")
        self.log_activity("task_started", {"query": query, "task": self.task})

        try:
            # Route to specific task handler
            if self.task == "compare_external_research":
                result = await self._compare_external_research(query, context)
            elif self.task == "compare_internal_research":
                result = await self._compare_internal_research(query, context)
            elif self.task == "study_patient_data":
                result = await self._study_patient_data(query, context)
            elif self.task == "study_individual_data":
                result = await self._study_individual_data(query, context)
            elif self.task == "study_medical_guidelines":
                result = await self._study_medical_guidelines(query, context)
            elif self.task == "predict_deterioration":
                result = await self._predict_deterioration(query, context)
            else:
                result = {"error": f"Unknown task: {self.task}"}

            self.update_status("completed")
            self.log_activity("task_completed", {"query": query, "task": self.task})

            return {
                "status": "success",
                "utility_agent": self.name,
                "task": self.task,
                "result": result
            }

        except Exception as e:
            self.update_status("error")
            logger.error(f"Utility Agent {self.name} error: {e}")
            return {
                "status": "error",
                "utility_agent": self.name,
                "task": self.task,
                "error": str(e)
            }

    async def _compare_external_research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compare with external research papers."""
        from backend.agents.tasks.compare_external_research import compare_external_research
        return await compare_external_research(query, context, self.model)

    async def _compare_internal_research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compare with internal hospital research."""
        from backend.agents.tasks.compare_internal_research import compare_internal_research
        return await compare_internal_research(query, context, self.model)

    async def _study_patient_data(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Study batch patient data."""
        from backend.agents.tasks.study_patient_data import study_patient_data
        return await study_patient_data(query, context, self.model)

    async def _study_individual_data(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deep dive into individual patient data."""
        from backend.agents.tasks.study_individual_data import study_individual_data
        return await study_individual_data(query, context, self.model)

    async def _study_medical_guidelines(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Study and apply medical guidelines."""
        from backend.agents.tasks.study_medical_guidelines import study_medical_guidelines
        return await study_medical_guidelines(query, context, self.model)

    async def _predict_deterioration(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict patient deterioration."""
        from backend.agents.tasks.predict_deterioration import predict_deterioration
        return await predict_deterioration(query, context, self.model)
