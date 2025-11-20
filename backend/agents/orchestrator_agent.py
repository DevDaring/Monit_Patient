"""Orchestrator Agent (Manager) - Top-level coordinator."""
from typing import Dict, Any, List, Optional
from backend.agents.base_agent import BaseAgent
from backend.agents.super_agent import SuperAgent
from loguru import logger


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent (Manager)
    - Receives user queries
    - Delegates to super agents
    - Aggregates responses
    - Makes final decisions
    """

    def __init__(
        self,
        agent_id: str = None,
        name: str = "Orchestrator",
        model: str = "gemini-2.0-flash-exp",
        **kwargs
    ):
        """Initialize orchestrator agent."""
        super().__init__(agent_id=agent_id, name=name, model=model, **kwargs)
        self.super_agents: List[SuperAgent] = []

    def add_super_agent(self, super_agent: SuperAgent):
        """Add a super agent to manage."""
        self.super_agents.append(super_agent)
        logger.info(f"Orchestrator {self.name} added Super Agent {super_agent.name}")

    def remove_super_agent(self, agent_id: str):
        """Remove a super agent."""
        self.super_agents = [sa for sa in self.super_agents if sa.agent_id != agent_id]

    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute orchestrator task:
        1. Analyze query
        2. Delegate to super agents
        3. Aggregate responses
        4. Formulate final response
        """
        self.update_status("processing")
        self.log_activity("query_received", {"query": query})

        try:
            # Import gemini service here to avoid circular imports
            from backend.services.gemini_service import GeminiService
            gemini_service = GeminiService()

            # Step 1: Analyze query and plan delegation
            delegation_prompt = f"""
            You are an Orchestrator Agent managing a team of Super Agents for hospital patient monitoring.

            Query: {query}

            Context: {context}

            Available Super Agents: {len(self.super_agents)}

            Analyze this query and determine:
            1. What type of analysis is needed?
            2. Which super agents should handle this?
            3. What specific questions should each super agent answer?

            Provide a clear delegation plan.
            """

            delegation_plan = await gemini_service.generate_response(
                prompt=delegation_prompt,
                model=self.model,
                context=context
            )

            # Step 2: Delegate to super agents
            super_agent_responses = []
            for super_agent in self.super_agents:
                try:
                    response = await super_agent.execute(query, context)
                    super_agent_responses.append({
                        "agent_id": super_agent.agent_id,
                        "agent_name": super_agent.name,
                        "response": response
                    })
                except Exception as e:
                    logger.error(f"Error from Super Agent {super_agent.name}: {e}")
                    super_agent_responses.append({
                        "agent_id": super_agent.agent_id,
                        "agent_name": super_agent.name,
                        "error": str(e)
                    })

            # Step 3: Aggregate responses and formulate final decision
            aggregation_prompt = f"""
            You are an Orchestrator Agent synthesizing findings from Super Agents.

            Original Query: {query}

            Delegation Plan: {delegation_plan}

            Super Agent Responses:
            {super_agent_responses}

            Synthesize these findings into a comprehensive response:
            1. Summary of key findings
            2. Risk assessment (if applicable)
            3. Recommendations
            4. Confidence level

            Provide a clear, actionable response.
            """

            final_response = await gemini_service.generate_response(
                prompt=aggregation_prompt,
                model=self.model,
                context=context
            )

            self.update_status("completed")
            self.log_activity("query_completed", {
                "query": query,
                "super_agents_involved": len(super_agent_responses)
            })

            return {
                "status": "success",
                "orchestrator": self.name,
                "delegation_plan": delegation_plan,
                "super_agent_responses": super_agent_responses,
                "final_response": final_response,
                "confidence": "high"  # Could be calculated based on agent agreement
            }

        except Exception as e:
            self.update_status("error")
            logger.error(f"Orchestrator error: {e}")
            return {
                "status": "error",
                "orchestrator": self.name,
                "error": str(e)
            }
