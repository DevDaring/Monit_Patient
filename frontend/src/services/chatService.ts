import api from './api'
import { ChatRequest, ChatResponse, VoiceResponse } from '../types/chat.types'

export const chatService = {
  // Send text message
  async sendTextMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post('/api/chat/text', request)
    return response.data
  },

  // Send voice message
  async sendVoiceMessage(
    audio: Blob,
    patientId?: string,
    language = 'en'
  ): Promise<VoiceResponse> {
    const formData = new FormData()
    formData.append('audio', audio)
    if (patientId) {
      formData.append('patient_id', patientId)
    }
    formData.append('language', language)

    const response = await api.post('/api/chat/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Convert text to speech
  async textToSpeech(text: string, language = 'en'): Promise<any> {
    const response = await api.post('/api/chat/text-to-speech', null, {
      params: { text, language },
    })
    return response.data
  },

  // Get available voices
  async getAvailableVoices(): Promise<{ voices: any[] }> {
    const response = await api.get('/api/chat/voices')
    return response.data
  },
}
