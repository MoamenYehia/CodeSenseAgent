import { ApiError, request } from './client'
import type { ApproveEscalationRequest, ApproveEscalationResponse, ChatResponse, InterruptDetails } from './types'
function isResponse(value: unknown): value is ChatResponse {
  if (!value || typeof value !== 'object') return false
  const item = value as Record<string, unknown>
  return typeof item.thread_id === 'string' && typeof item.status === 'string' && (item.response === null || typeof item.response === 'string') && (item.interrupt_details === null || typeof item.interrupt_details === 'object')
}
export async function sendChatMessage(threadId: string, message: string): Promise<ChatResponse> {
  const value: unknown = await request('/chat', { method: 'POST', body: JSON.stringify({ thread_id: threadId, message }) })
  if (!isResponse(value)) throw new ApiError('malformed', 'The sales engineer returned an unexpected response. Please try again.')
  return value
}
export function checkPendingReview(threadId: string) { return request<InterruptDetails | null>(`/pending_reviews/${encodeURIComponent(threadId)}`) }
export function approveEscalation(threadId: string, decision: string) { const body: ApproveEscalationRequest = { thread_id: threadId, decision }; return request<ApproveEscalationResponse>('/approve_escalation', { method: 'POST', body: JSON.stringify(body) }) }
