export interface ChatRequest { thread_id: string; message: string }
export interface InterruptDetails { status?: string | null; message?: string | null; instructions?: string | null }
export type ChatStatus = 'COMPLETED' | 'INTERRUPTED' | (string & {})
export interface ChatResponse { thread_id: string; status: ChatStatus; response: string | null; interrupt_details: InterruptDetails | null }
export interface ApproveEscalationRequest { thread_id: string; decision: string }
export interface ApproveEscalationResponse { thread_id: string; status: string; final_response: string | null }
