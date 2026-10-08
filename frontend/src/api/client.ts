export type ApiErrorKind = 'network' | 'timeout' | 'client' | 'server' | 'malformed'
export class ApiError extends Error { constructor(public kind: ApiErrorKind, public userMessage: string, public status?: number) { super(userMessage) } }
const BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? 'http://localhost:8000/api/v1'
export async function request<T>(path: string, init: RequestInit = {}, timeout = 60000): Promise<T> {
  const controller = new AbortController(); const timer = window.setTimeout(() => controller.abort(), timeout)
  try {
    let response: Response
    try { response = await fetch(`${BASE}${path}`, { ...init, signal: controller.signal, headers: { 'Content-Type': 'application/json', ...init.headers } }) }
    catch (error) { if (error instanceof DOMException && error.name === 'AbortError') throw new ApiError('timeout', 'The sales engineer took too long to respond. Please try again.'); throw new ApiError('network', 'We could not reach the sales engineer. Check that the API is running and try again.') }
    if (!response.ok) throw new ApiError(response.status >= 500 ? 'server' : 'client', response.status >= 500 ? 'The sales engineer is temporarily unavailable. Please try again.' : 'We could not process that request. Please check it and try again.', response.status)
    try { return await response.json() as T } catch { throw new ApiError('malformed', 'The sales engineer returned an unexpected response. Please try again.') }
  } finally { window.clearTimeout(timer) }
}
