export type AgentType = 'orchestrator' | 'super' | 'utility'

export type UtilityAgentTask =
  | 'compare_external_research'
  | 'compare_internal_research'
  | 'study_patient_data'
  | 'study_individual_data'
  | 'study_medical_guidelines'
  | 'predict_deterioration'

export interface AgentConfig {
  agent_id: string
  name: string
  agent_type: AgentType
  model: string
  task?: UtilityAgentTask
  metadata?: Record<string, any>
}

export interface AgentHierarchy {
  config_id: string
  name: string
  orchestrator: AgentConfig
  super_agents: AgentConfig[]
  utility_agents: AgentConfig[]
  connections: Record<string, string[]> // super_agent_id -> utility_agent_ids
  created_at?: string
  updated_at?: string
}

export interface AgentModel {
  id: string
  name: string
  type: 'fast' | 'standard' | 'advanced'
}

export interface AgentTask {
  id: UtilityAgentTask
  name: string
  description: string
}

export interface AgentQueryRequest {
  query: string
  patient_id?: string
  context?: Record<string, any>
}

export interface AgentQueryResponse {
  status: 'success' | 'error' | 'processing'
  final_response?: string
  super_agent_responses?: any[]
  error?: string
}

export interface AgentStatus {
  status: 'active' | 'not_initialized' | 'error'
  orchestrator?: any
  super_agents?: any[]
  total_super_agents?: number
}
