import { createContext, useCallback, useContext, useMemo, useReducer, useRef } from 'react'
import type { ReactNode } from 'react'
import { sendChatMessage } from '../../api/chat'
import { ApiError } from '../../api/client'
import type { ChatResponse } from '../../api/types'
interface Message { id: string; role: 'user' | 'assistant'; text: string; at: string }
interface State { threadId: string; messages: Message[]; loading: boolean; error: ApiError | null; failed: string | null; drawerOpen: boolean; escalation: { message: string; instructions: string } | null }
type Action = { type: 'new' } | { type: 'user'; text: string } | { type: 'assistant'; text: string } | { type: 'loading'; value: boolean } | { type: 'error'; error: ApiError; failed: string } | { type: 'clearError' } | { type: 'drawer'; value: boolean } | { type: 'escalation'; value: { message: string; instructions: string } | null }
const id = () => crypto.randomUUID?.() ?? `session-${Date.now()}`
const initial = (): State => { const threadId = sessionStorage.getItem('codesense-thread') ?? id(); sessionStorage.setItem('codesense-thread', threadId); return { threadId, messages: [], loading: false, error: null, failed: null, drawerOpen: false, escalation: null } }
function reducer(state: State, action: Action): State {
  if (action.type === 'new') { const threadId = id(); sessionStorage.setItem('codesense-thread', threadId); return { ...initial(), threadId } }
  if (action.type === 'user') return { ...state, messages: [...state.messages, { id: id(), role: 'user', text: action.text, at: new Date().toISOString() }], error: null, failed: null }
  if (action.type === 'assistant') return { ...state, messages: [...state.messages, { id: id(), role: 'assistant', text: action.text, at: new Date().toISOString() }] }
  if (action.type === 'loading') return { ...state, loading: action.value }
  if (action.type === 'error') return { ...state, loading: false, error: action.error, failed: action.failed }
  if (action.type === 'clearError') return { ...state, error: null }
  if (action.type === 'escalation') return { ...state, escalation: action.value }
  return { ...state, drawerOpen: action.value }
}
interface ContextValue extends State { send: (text: string, retry?: boolean) => Promise<void>; newConversation: () => void; setDrawer: (open: boolean) => void }
const ChatContext = createContext<ContextValue | null>(null)
export function ChatProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, undefined, initial); const latest = useRef(state); latest.current = state
  const send = useCallback(async (text: string, retry = false) => {
    const trimmed = text.trim(); if (!trimmed || latest.current.loading) return
    if (!retry) dispatch({ type: 'user', text: trimmed }); else dispatch({ type: 'clearError' })
    dispatch({ type: 'loading', value: true })
    try {
      const result: ChatResponse = await sendChatMessage(latest.current.threadId, trimmed)
      dispatch({ type: 'loading', value: false }); if (result.response) dispatch({ type: 'assistant', text: result.response })
      if (result.status.toUpperCase() === 'INTERRUPTED') { const detail = result.interrupt_details; dispatch({ type: 'escalation', value: { message: typeof detail?.message === 'string' ? detail.message : '', instructions: typeof detail?.instructions === 'string' ? detail.instructions : '' } }) }
      else if (result.status.toUpperCase() !== 'COMPLETED' && !result.response) dispatch({ type: 'assistant', text: 'I could not determine the next step from that response. Please try again or ask about plans, integrations, or security.' })
    } catch (error) { const apiError = error instanceof ApiError ? error : new ApiError('network', 'We could not reach the sales engineer. Check that the API is running and try again.'); dispatch({ type: 'error', error: apiError, failed: trimmed }) }
  }, [])
  const value = useMemo(() => ({ ...state, send, newConversation: () => dispatch({ type: 'new' }), setDrawer: (value: boolean) => dispatch({ type: 'drawer', value }) }), [state, send])
  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}
export function useChat() { const value = useContext(ChatContext); if (!value) throw new Error('useChat must be used inside ChatProvider'); return value }
