import { create } from 'zustand'
import { ChatMessage } from '../types/chat.types'
import { chatService } from '../services/chatService'

interface ChatState {
  messages: Record<string, ChatMessage[]> // patientId -> messages
  isLoading: boolean
  error: string | null
  sendMessage: (patientId: string | undefined, message: string, language?: string) => Promise<void>
  addMessage: (patientId: string | undefined, message: ChatMessage) => void
  clearMessages: (patientId: string | undefined) => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: {},
  isLoading: false,
  error: null,

  sendMessage: async (patientId: string | undefined, message: string, language = 'en') => {
    const key = patientId || 'general'

    // Add user message
    const userMessage: ChatMessage = {
      message_id: `user-${Date.now()}`,
      patient_id: patientId,
      user_id: 'current-user',
      role: 'user',
      content: message,
      language,
      timestamp: new Date().toISOString(),
    }

    set((state) => ({
      messages: {
        ...state.messages,
        [key]: [...(state.messages[key] || []), userMessage],
      },
      isLoading: true,
      error: null,
    }))

    try {
      const response = await chatService.sendTextMessage({
        patient_id: patientId,
        message,
        language,
      })

      // Add agent response
      const agentMessage: ChatMessage = {
        message_id: response.message_id,
        patient_id: patientId,
        user_id: 'agent',
        role: 'agent',
        content: response.content,
        audio_url: response.audio_url,
        language,
        timestamp: response.timestamp,
      }

      set((state) => ({
        messages: {
          ...state.messages,
          [key]: [...(state.messages[key] || []), agentMessage],
        },
        isLoading: false,
      }))
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  },

  addMessage: (patientId: string | undefined, message: ChatMessage) => {
    const key = patientId || 'general'
    set((state) => ({
      messages: {
        ...state.messages,
        [key]: [...(state.messages[key] || []), message],
      },
    }))
  },

  clearMessages: (patientId: string | undefined) => {
    const key = patientId || 'general'
    set((state) => ({
      messages: {
        ...state.messages,
        [key]: [],
      },
    }))
  },
}))
