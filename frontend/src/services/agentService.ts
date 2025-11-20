import api from './api'
import {
  AgentHierarchy,
  AgentQueryRequest,
  AgentQueryResponse,
  AgentModel,
  AgentTask,
  AgentStatus,
} from '../types/agent.types'

export const agentService = {
  // Configure agent hierarchy
  async configureAgents(hierarchy: Partial<AgentHierarchy>): Promise<any> {
    const response = await api.post('/api/agents/configure', {
      config_name: hierarchy.name,
      orchestrator: hierarchy.orchestrator,
      super_agents: hierarchy.super_agents,
      utility_agents: hierarchy.utility_agents,
      connections: hierarchy.connections,
    })
    return response.data
  },

  // Get current configuration
  async getConfiguration(): Promise<{ status: string; config: AgentHierarchy }> {
    const response = await api.get('/api/agents/configuration')
    return response.data
  },

  // Query agent system
  async queryAgents(request: AgentQueryRequest): Promise<AgentQueryResponse> {
    const response = await api.post('/api/agents/query', request)
    return response.data
  },

  // Get available models
  async getAvailableModels(): Promise<{ models: AgentModel[] }> {
    const response = await api.get('/api/agents/available-models')
    return response.data
  },

  // Get available tasks
  async getAvailableTasks(): Promise<{ tasks: AgentTask[] }> {
    const response = await api.get('/api/agents/available-tasks')
    return response.data
  },

  // Get agent status
  async getAgentStatus(): Promise<AgentStatus> {
    const response = await api.get('/api/agents/status')
    return response.data
  },
}
