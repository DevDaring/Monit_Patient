"""Super Agent (Team Lead) - Manages utility agents."""
from typing import Dict, Any, List, Optional
from backend.agents.base_agent import BaseAgent
from loguru import logger


class SuperAgent(BaseAgent):
    """
    Super Agent (Team Lead)
    - Manages 2+ utility agents
    - Assigns subtasks
    - Ensures task completion
    - Reports to orchestrator
    """

    def __init__(
        self,
        agent_id: str = None,
        name: str = "SuperAgent",
        model: str = "gemini-2.0-flash-exp",
        **kwargs
    ):
        """Initialize super agent."""
        super().__init__(agent_id=agent_id, name=name, model=model, **kwargs)
        self.utility_agents: List['UtilityAgent'] = []

    def add_utility_agent(self, utility_agent: 'UtilityAgent'):
        """Add a utility agent to manage."""
        self.utility_agents.append(utility_agent)
        logger.info(f"Super Agent {self.name} added Utility Agent {utility_agent.name}")

    def remove_utility_agent(self, agent_id: str):
        """Remove a utility agent."""
        self.utility_agents = [ua for ua in self.utility_agents if ua.agent_id != agent_id]

    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute super agent task:
        1. Break down task into subtasks
        2. Assign to utility agents
        3. Monitor progress
        4. Synthesize results
        """
        self.update_status("processing")
        self.log_activity("task_received", {"query": query})

        try:
            # Import gemini service
            from backend.services.gemini_service import GeminiService
            gemini_service = GeminiService()

            # Step 1: Plan subtask distribution
            planning_prompt = f"""
            You are a Super Agent (Team Lead) managing {len(self.utility_agents)} Utility Agents.

            Task: {query}

            Context: {context}

            Available Utility Agents and their tasks:
            {[{"name": ua.name, "task": ua.task} for ua in self.utility_agents]}

            Create a plan to distribute this work among your utility agents:
            1. What should each utility agent do?
            2. In what order should tasks be executed?
            3. What dependencies exist?

            Provide a clear task distribution plan.
            """

            task_plan = await gemini_service.generate_response(
                prompt=planning_prompt,
                model=self.model,
                context=context
            )

            # Step 2: Execute utility agents
            utility_agent_results = []
            for utility_agent in self.utility_agents:
                try:
                    result = await utility_agent.execute(query, context)
                    utility_agent_results.append({
                        "agent_id": utility_agent.agent_id,
                        "agent_name": utility_agent.name,
                        "task": utility_agent.task,
                        "result": result
                    })
                except Exception as e:
                    logger.error(f"Error from Utility Agent {utility_agent.name}: {e}")
                    utility_agent_results.append({
                        "agent_id": utility_agent.agent_id,
                        "agent_name": utility_agent.name,
                        "task": utility_agent.task,
                        "error": str(e)
                    })

            # Step 3: Synthesize utility agent results
            synthesis_prompt = f"""
            You are a Super Agent synthesizing findings from Utility Agents.

            Original Task: {query}

            Task Plan: {task_plan}

            Utility Agent Results:
            {utility_agent_results}

            Synthesize these findings:
            1. What are the key insights?
            2. Are there any conflicts or agreements?
            3. What is the overall assessment?
            4. What recommendations emerge?

            Provide a comprehensive synthesis.
            """

            synthesis = await gemini_service.generate_response(
                prompt=synthesis_prompt,
                model=self.model,
                context=context
            )

            self.update_status("completed")
            self.log_activity("task_completed", {
                "query": query,
                "utility_agents_involved": len(utility_agent_results)
            })

            return {
                "status": "success",
                "super_agent": self.name,
                "task_plan": task_plan,
                "utility_agent_results": utility_agent_results,
                "synthesis": synthesis
            }

        except Exception as e:
            self.update_status("error")
            logger.error(f"Super Agent error: {e}")
            return {
                "status": "error",
                "super_agent": self.name,
                "error": str(e)
            }
