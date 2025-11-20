import { useEffect } from 'react'
import { useAgentStore } from '../store/agentStore'

export function useAgentConfig() {
  const {
    configuration,
    availableModels,
    availableTasks,
    status,
    isLoading,
    error,
    fetchConfiguration,
    saveConfiguration,
    fetchAvailableModels,
    fetchAvailableTasks,
    fetchStatus,
  } = useAgentStore()

  useEffect(() => {
    fetchConfiguration()
    fetchAvailableModels()
    fetchAvailableTasks()
    fetchStatus()
  }, [fetchConfiguration, fetchAvailableModels, fetchAvailableTasks, fetchStatus])

  return {
    configuration,
    availableModels,
    availableTasks,
    status,
    isLoading,
    error,
    saveConfiguration,
    refreshConfiguration: fetchConfiguration,
    refreshStatus: fetchStatus,
  }
}
