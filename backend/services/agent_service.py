"""Agent orchestration service."""
from typing import Dict, Any, List, Optional
from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.agents.super_agent import SuperAgent
from backend.agents.utility_agent import UtilityAgent
from backend.agents.models.agent_config import AgentHierarchyConfig, AgentConfigModel
from backend.core.database import db
from loguru import logger
import uuid
import json


class AgentService:
    """Service for managing agent system."""

    def __init__(self):
        """Initialize agent service."""
        self.config_file = "agents/agent_configurations.csv"
        self.active_orchestrator: Optional[OrchestratorAgent] = None
        self.current_config: Optional[AgentHierarchyConfig] = None

    def load_configuration(self, config_id: Optional[str] = None) -> Optional[AgentHierarchyConfig]:
        """
        Load agent configuration from CSV.

        Args:
            config_id: Specific config ID to load, or None for latest

        Returns:
            AgentHierarchyConfig or None
        """
        try:
            configs_df = db.read_csv(self.config_file)
            if configs_df.empty:
                logger.warning("No agent configurations found")
                return self._create_default_configuration()

            # Get specific or latest config
            if config_id and 'config_id' in configs_df.columns:
                config_row = configs_df[configs_df['config_id'] == config_id]
            else:
                # Get most recent
                if 'created_at' in configs_df.columns:
                    configs_df = configs_df.sort_values('created_at', ascending=False)
                config_row = configs_df.head(1)

            if config_row.empty:
                return self._create_default_configuration()

            # Parse config (stored as JSON in CSV)
            config_data = config_row.iloc[0].to_dict()

            # Reconstruct hierarchy config
            # Note: In production, you'd want a more robust serialization
            return self._parse_config_from_dict(config_data)

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self._create_default_configuration()

    def _create_default_configuration(self) -> AgentHierarchyConfig:
        """Create default agent configuration."""
        config_id = str(uuid.uuid4())

        # Create orchestrator
        orchestrator = AgentConfigModel(
            agent_id=str(uuid.uuid4()),
            name="Main Orchestrator",
            agent_type="orchestrator",
            model="gemini-2.0-flash-exp"
        )

        # Create 2 super agents
        super_agents = [
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="Medical Analysis Team",
                agent_type="super",
                model="gemini-2.0-flash-exp"
            ),
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="Research Team",
                agent_type="super",
                model="gemini-2.0-flash-exp"
            )
        ]

        # Create 4 utility agents
        utility_agents = [
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="Patient Data Analyst",
                agent_type="utility",
                model="gemini-2.0-flash-exp",
                task="study_patient_data"
            ),
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="Individual Care Specialist",
                agent_type="utility",
                model="gemini-2.0-flash-exp",
                task="study_individual_data"
            ),
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="External Research Analyst",
                agent_type="utility",
                model="gemini-2.0-flash-exp",
                task="compare_external_research"
            ),
            AgentConfigModel(
                agent_id=str(uuid.uuid4()),
                name="Guidelines Specialist",
                agent_type="utility",
                model="gemini-2.0-flash-exp",
                task="study_medical_guidelines"
            )
        ]

        # Create connections: First super agent gets first 2 utilities, second gets last 2
        connections = {
            super_agents[0].agent_id: [utility_agents[0].agent_id, utility_agents[1].agent_id],
            super_agents[1].agent_id: [utility_agents[2].agent_id, utility_agents[3].agent_id]
        }

        config = AgentHierarchyConfig(
            config_id=config_id,
            name="Default Configuration",
            orchestrator=orchestrator,
            super_agents=super_agents,
            utility_agents=utility_agents,
            connections=connections
        )

        # Validate
        is_valid, message = config.validate_hierarchy()
        if is_valid:
            logger.info(f"Created default configuration: {config_id}")
            return config
        else:
            logger.error(f"Invalid default configuration: {message}")
            raise ValueError(f"Invalid configuration: {message}")

    def _parse_config_from_dict(self, config_data: Dict[str, Any]) -> AgentHierarchyConfig:
        """Parse configuration from dictionary."""
        # This is a simplified parser - in production you'd want more robust handling
        # For now, return default config
        return self._create_default_configuration()

    def initialize_agents(self, config: AgentHierarchyConfig):
        """Initialize agent instances from configuration."""
        try:
            # Create orchestrator
            orchestrator = OrchestratorAgent(
                agent_id=config.orchestrator.agent_id,
                name=config.orchestrator.name,
                model=config.orchestrator.model
            )

            # Create super agents and their utility agents
            for super_config in config.super_agents:
                super_agent = SuperAgent(
                    agent_id=super_config.agent_id,
                    name=super_config.name,
                    model=super_config.model
                )

                # Add utility agents for this super agent
                utility_ids = config.connections.get(super_config.agent_id, [])
                for utility_id in utility_ids:
                    # Find utility config
                    utility_config = next(
                        (u for u in config.utility_agents if u.agent_id == utility_id),
                        None
                    )
                    if utility_config:
                        utility_agent = UtilityAgent(
                            agent_id=utility_config.agent_id,
                            name=utility_config.name,
                            model=utility_config.model,
                            task=utility_config.task
                        )
                        super_agent.add_utility_agent(utility_agent)

                orchestrator.add_super_agent(super_agent)

            self.active_orchestrator = orchestrator
            self.current_config = config

            logger.info(f"Initialized agent system with config: {config.config_id}")

        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            raise

    async def process_query(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a query through the agent system.

        Args:
            query: User query
            context: Context data (patient info, etc.)

        Returns:
            Agent system response
        """
        try:
            # Ensure agents are initialized
            if not self.active_orchestrator:
                config = self.load_configuration()
                if config:
                    self.initialize_agents(config)
                else:
                    raise ValueError("No agent configuration available")

            # Execute through orchestrator
            result = await self.active_orchestrator.execute(query, context)

            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def save_configuration(self, config: AgentHierarchyConfig) -> bool:
        """Save agent configuration to CSV."""
        try:
            # Validate first
            is_valid, message = config.validate_hierarchy()
            if not is_valid:
                logger.error(f"Invalid configuration: {message}")
                return False

            # Serialize config to dict
            config_row = {
                "config_id": config.config_id,
                "name": config.name,
                "config_json": json.dumps(config.model_dump()),
                "created_at": config.created_at.isoformat()
            }

            # Save to CSV
            db.append_row(self.config_file, config_row)

            logger.info(f"Saved configuration: {config.config_id}")
            return True

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
