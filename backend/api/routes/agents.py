"""Agent configuration and management endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.schemas.agent_schema import (
    AgentHierarchyRequest,
    AgentQueryRequest,
    AgentQueryResponse
)
from backend.services.agent_service import AgentService
from backend.agents.models.agent_config import AgentHierarchyConfig, AgentConfigModel
from loguru import logger
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/agents", tags=["agents"])
agent_service = AgentService()


@router.post("/configure", response_model=Dict[str, Any])
async def configure_agents(config_request: AgentHierarchyRequest):
    """
    Configure agent hierarchy.

    This endpoint allows admins to set up the agent system:
    - Define orchestrator (Manager)
    - Add super agents (Team Leads)
    - Add utility agents (Staff) with specific tasks
    - Define connections between super agents and utility agents
    """
    try:
        # Convert request to AgentHierarchyConfig
        config = AgentHierarchyConfig(
            config_id=str(uuid.uuid4()),
            name=config_request.config_name,
            orchestrator=AgentConfigModel(**config_request.orchestrator.model_dump()),
            super_agents=[AgentConfigModel(**sa.model_dump()) for sa in config_request.super_agents],
            utility_agents=[AgentConfigModel(**ua.model_dump()) for ua in config_request.utility_agents],
            connections=config_request.connections,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Validate configuration
        is_valid, message = config.validate_hierarchy()
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        # Save configuration
        success = agent_service.save_configuration(config)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save configuration")

        # Initialize agents with new configuration
        agent_service.initialize_agents(config)

        return {
            "status": "success",
            "message": "Agent configuration saved and initialized",
            "config_id": config.config_id,
            "validation": message
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error configuring agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/configuration")
async def get_configuration():
    """Get current agent configuration."""
    try:
        if agent_service.current_config:
            return {
                "status": "success",
                "config": agent_service.current_config.model_dump()
            }
        else:
            # Load default configuration
            config = agent_service.load_configuration()
            if config:
                agent_service.initialize_agents(config)
                return {
                    "status": "success",
                    "config": config.model_dump()
                }
            else:
                raise HTTPException(status_code=404, detail="No configuration found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=AgentQueryResponse)
async def query_agents(query_request: AgentQueryRequest):
    """
    Send query to agent system for analysis.

    This endpoint processes medical queries through the multi-agent system.
    """
    try:
        context = query_request.context or {}
        if query_request.patient_id:
            context['patient_id'] = query_request.patient_id

        result = await agent_service.process_query(
            query=query_request.query,
            context=context
        )

        return AgentQueryResponse(
            status=result.get('status', 'unknown'),
            final_response=result.get('final_response'),
            super_agent_responses=result.get('super_agent_responses'),
            error=result.get('error')
        )

    except Exception as e:
        logger.error(f"Error processing agent query: {e}")
        return AgentQueryResponse(
            status="error",
            error=str(e)
        )


@router.get("/available-models")
async def get_available_models():
    """Get list of available Gemini models."""
    return {
        "models": [
            {"id": "gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash (Experimental)", "type": "fast"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "type": "standard"},
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "type": "fast"},
        ]
    }


@router.get("/available-tasks")
async def get_available_tasks():
    """Get list of available utility agent tasks."""
    from backend.agents.utility_agent import UtilityAgent

    return {
        "tasks": [
            {
                "id": "compare_external_research",
                "name": "Compare with External Research",
                "description": "Search and compare with medical research papers using Google grounding"
            },
            {
                "id": "compare_internal_research",
                "name": "Compare with Internal Research",
                "description": "Compare with hospital's internal case studies and treatment outcomes"
            },
            {
                "id": "study_patient_data",
                "name": "Study Internal Patient Data",
                "description": "Analyze patterns across multiple patients in the database"
            },
            {
                "id": "study_individual_data",
                "name": "Study Individual Data for Personal Care",
                "description": "Deep dive analysis of a single patient's complete history"
            },
            {
                "id": "study_medical_guidelines",
                "name": "Study Medical Guidelines",
                "description": "Reference clinical practice guidelines and protocols"
            },
            {
                "id": "predict_deterioration",
                "name": "Predict Patient Deterioration",
                "description": "Predictive analytics for patient deterioration risk"
            }
        ]
    }


@router.get("/status")
async def get_agent_status():
    """Get current status of agent system."""
    try:
        if agent_service.active_orchestrator:
            orchestrator_info = agent_service.active_orchestrator.get_info()
            super_agents_info = [sa.get_info() for sa in agent_service.active_orchestrator.super_agents]

            return {
                "status": "active",
                "orchestrator": orchestrator_info,
                "super_agents": super_agents_info,
                "total_super_agents": len(super_agents_info)
            }
        else:
            return {
                "status": "not_initialized",
                "message": "Agent system not initialized. Please configure agents first."
            }

    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
