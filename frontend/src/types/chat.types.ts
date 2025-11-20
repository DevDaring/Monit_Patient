export interface ChatMessage {
  message_id: string
  patient_id?: string
  user_id: string
  role: 'user' | 'agent' | 'system'
  content: string
  audio_url?: string
  language: string
  metadata?: Record<string, any>
  timestamp: string
}

export interface ChatRequest {
  patient_id?: string
  message: string
  language?: string
}

export interface VoiceChatRequest {
  patient_id?: string
  language?: string
  audio: Blob
}

export interface ChatResponse {
  message_id: string
  content: string
  audio_url?: string
  timestamp: string
}

export interface VoiceResponse {
  text: string
  audio_url: string
  language: string
}
