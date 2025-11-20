import { create } from 'zustand'
import { AgentHierarchy, AgentModel, AgentTask, AgentStatus } from '../types/agent.types'
import { agentService } from '../services/agentService'

interface AgentState {
  configuration: AgentHierarchy | null
  availableModels: AgentModel[]
  availableTasks: AgentTask[]
  status: AgentStatus | null
  isLoading: boolean
  error: string | null
  fetchConfiguration: () => Promise<void>
  saveConfiguration: (config: Partial<AgentHierarchy>) => Promise<void>
  fetchAvailableModels: () => Promise<void>
  fetchAvailableTasks: () => Promise<void>
  fetchStatus: () => Promise<void>
}

export const useAgentStore = create<AgentState>((set) => ({
  configuration: null,
  availableModels: [],
  availableTasks: [],
  status: null,
  isLoading: false,
  error: null,

  fetchConfiguration: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await agentService.getConfiguration()
      set({ configuration: response.config, isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  },

  saveConfiguration: async (config: Partial<AgentHierarchy>) => {
    set({ isLoading: true, error: null })
    try {
      await agentService.configureAgents(config)
      // Fetch updated configuration
      const response = await agentService.getConfiguration()
      set({ configuration: response.config, isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
      throw error
    }
  },

  fetchAvailableModels: async () => {
    try {
      const response = await agentService.getAvailableModels()
      set({ availableModels: response.models })
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  fetchAvailableTasks: async () => {
    try {
      const response = await agentService.getAvailableTasks()
      set({ availableTasks: response.tasks })
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  fetchStatus: async () => {
    try {
      const status = await agentService.getAgentStatus()
      set({ status })
    } catch (error: any) {
      set({ error: error.message })
    }
  },
}))
