import { useState, useEffect } from 'react'
import { useAgentConfig } from '../../hooks/useAgentConfig'
import { AgentConfig, AgentType, UtilityAgentTask } from '../../types/agent.types'
import { Plus, Trash2, Link as LinkIcon } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AgentConfigPanel() {
  const { configuration, availableModels, availableTasks, saveConfiguration, isLoading } =
    useAgentConfig()

  const [orchestrator, setOrchestrator] = useState<AgentConfig | null>(null)
  const [superAgents, setSuperAgents] = useState<AgentConfig[]>([])
  const [utilityAgents, setUtilityAgents] = useState<AgentConfig[]>([])
  const [connections, setConnections] = useState<Record<string, string[]>>({})

  // Load configuration when available
  useEffect(() => {
    if (configuration) {
      setOrchestrator(configuration.orchestrator)
      setSuperAgents(configuration.super_agents || [])
      setUtilityAgents(configuration.utility_agents || [])
      setConnections(configuration.connections || {})
    }
  }, [configuration])

  // Add Super Agent
  const addSuperAgent = () => {
    const newAgent: AgentConfig = {
      agent_id: `super-${Date.now()}`,
      name: `Team Lead ${superAgents.length + 1}`,
      agent_type: 'super',
      model: 'gemini-2.0-flash-exp',
    }
    setSuperAgents([...superAgents, newAgent])
    setConnections({ ...connections, [newAgent.agent_id]: [] })
  }

  // Add Utility Agent
  const addUtilityAgent = () => {
    const newAgent: AgentConfig = {
      agent_id: `util-${Date.now()}`,
      name: `Staff ${utilityAgents.length + 1}`,
      agent_type: 'utility',
      model: 'gemini-2.0-flash-exp',
      task: 'study_patient_data',
    }
    setUtilityAgents([...utilityAgents, newAgent])
  }

  // Remove Super Agent
  const removeSuperAgent = (agentId: string) => {
    setSuperAgents(superAgents.filter((a) => a.agent_id !== agentId))
    const newConnections = { ...connections }
    delete newConnections[agentId]
    setConnections(newConnections)
  }

  // Remove Utility Agent
  const removeUtilityAgent = (agentId: string) => {
    setUtilityAgents(utilityAgents.filter((a) => a.agent_id !== agentId))
    // Remove from all connections
    const newConnections = { ...connections }
    Object.keys(newConnections).forEach((superAgentId) => {
      newConnections[superAgentId] = newConnections[superAgentId].filter((id) => id !== agentId)
    })
    setConnections(newConnections)
  }

  // Toggle connection between super agent and utility agent
  const toggleConnection = (superAgentId: string, utilityAgentId: string) => {
    const newConnections = { ...connections }
    if (!newConnections[superAgentId]) {
      newConnections[superAgentId] = []
    }

    if (newConnections[superAgentId].includes(utilityAgentId)) {
      newConnections[superAgentId] = newConnections[superAgentId].filter(
        (id) => id !== utilityAgentId
      )
    } else {
      newConnections[superAgentId].push(utilityAgentId)
    }

    setConnections(newConnections)
  }

  // Save configuration
  const handleSave = async () => {
    // Validation
    for (const superAgent of superAgents) {
      const connectedUtilities = connections[superAgent.agent_id] || []
      if (connectedUtilities.length < 2) {
        toast.error(`${superAgent.name} must have at least 2 staff members`)
        return
      }
    }

    if (!orchestrator) {
      toast.error('Orchestrator configuration is missing')
      return
    }

    try {
      await saveConfiguration({
        name: 'Current Configuration',
        orchestrator,
        super_agents: superAgents,
        utility_agents: utilityAgents,
        connections,
      })
      toast.success('Configuration saved successfully!')
    } catch (error) {
      toast.error('Failed to save configuration')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Agent Configuration</h2>
          <p className="text-gray-600 mt-1">
            Configure your multi-agent system hierarchy
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={isLoading}
          className="px-6 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors disabled:opacity-50"
        >
          {isLoading ? 'Saving...' : 'Save Configuration'}
        </button>
      </div>

      {/* Row 1: Orchestrator (Manager) */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Orchestrator (Manager) - 1 Required
        </h3>
        {orchestrator && (
          <AgentCard
            agent={orchestrator}
            availableModels={availableModels}
            availableTasks={availableTasks}
            onChange={(updated) => setOrchestrator(updated)}
          />
        )}
      </div>

      {/* Row 2: Super Agents (Team Leads) */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Super Agents (Team Leads) - {superAgents.length} Created
          </h3>
          <button
            onClick={addSuperAgent}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Team Lead
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {superAgents.map((agent) => (
            <AgentCard
              key={agent.agent_id}
              agent={agent}
              availableModels={availableModels}
              availableTasks={availableTasks}
              onChange={(updated) => {
                setSuperAgents(
                  superAgents.map((a) => (a.agent_id === agent.agent_id ? updated : a))
                )
              }}
              onRemove={() => removeSuperAgent(agent.agent_id)}
              showRemove
            />
          ))}
        </div>
      </div>

      {/* Row 3: Utility Agents (Staff) */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Utility Agents (Staff) - {utilityAgents.length} Created
          </h3>
          <button
            onClick={addUtilityAgent}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Staff
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {utilityAgents.map((agent) => (
            <AgentCard
              key={agent.agent_id}
              agent={agent}
              availableModels={availableModels}
              availableTasks={availableTasks}
              onChange={(updated) => {
                setUtilityAgents(
                  utilityAgents.map((a) => (a.agent_id === agent.agent_id ? updated : a))
                )
              }}
              onRemove={() => removeUtilityAgent(agent.agent_id)}
              showRemove
              isUtility
            />
          ))}
        </div>
      </div>

      {/* Connections Matrix */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Team Connections (Each Team Lead needs ≥2 Staff)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-2 px-4 border-b">Team Lead</th>
                {utilityAgents.map((util) => (
                  <th key={util.agent_id} className="text-center py-2 px-4 border-b text-sm">
                    {util.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {superAgents.map((superAgent) => (
                <tr key={superAgent.agent_id}>
                  <td className="py-2 px-4 border-b font-medium">{superAgent.name}</td>
                  {utilityAgents.map((utilAgent) => (
                    <td key={utilAgent.agent_id} className="text-center py-2 px-4 border-b">
                      <button
                        onClick={() => toggleConnection(superAgent.agent_id, utilAgent.agent_id)}
                        className={`w-8 h-8 rounded transition-colors ${
                          connections[superAgent.agent_id]?.includes(utilAgent.agent_id)
                            ? 'bg-success-500 text-white'
                            : 'bg-gray-200 text-gray-400'
                        }`}
                      >
                        <LinkIcon className="w-4 h-4 mx-auto" />
                      </button>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

// Agent Card Component
interface AgentCardProps {
  agent: AgentConfig
  availableModels: any[]
  availableTasks: any[]
  onChange: (agent: AgentConfig) => void
  onRemove?: () => void
  showRemove?: boolean
  isUtility?: boolean
}

function AgentCard({
  agent,
  availableModels,
  availableTasks,
  onChange,
  onRemove,
  showRemove,
  isUtility,
}: AgentCardProps) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 space-y-3">
      <div className="flex items-center justify-between">
        <input
          type="text"
          value={agent.name}
          onChange={(e) => onChange({ ...agent, name: e.target.value })}
          className="font-medium text-gray-900 border-none focus:outline-none focus:ring-2 focus:ring-primary-500 rounded px-2 py-1"
        />
        {showRemove && onRemove && (
          <button
            onClick={onRemove}
            className="text-danger-600 hover:text-danger-700"
            title="Remove"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Model Selection */}
      <div>
        <label className="block text-xs text-gray-600 mb-1">Model</label>
        <select
          value={agent.model}
          onChange={(e) => onChange({ ...agent, model: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          {availableModels.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </select>
      </div>

      {/* Task Selection (Utility Agents only) */}
      {isUtility && (
        <div>
          <label className="block text-xs text-gray-600 mb-1">Task</label>
          <select
            value={agent.task || ''}
            onChange={(e) => onChange({ ...agent, task: e.target.value as UtilityAgentTask })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            {availableTasks.map((task) => (
              <option key={task.id} value={task.id}>
                {task.name}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="text-xs text-gray-500">ID: {agent.agent_id.substring(0, 12)}...</div>
    </div>
  )
}
