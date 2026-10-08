import { Container } from '../components/ui/Container'
import { ChatSection } from '../components/chat/ChatUI'
import { plans } from '../data/plans'
import { Link } from 'react-router-dom'

export function Chat() {
  return <section className="min-h-[calc(100vh-76px)] py-8 md:py-12"><Container><div className="mb-6"><p className="font-mono text-xs uppercase tracking-[.2em] text-crimson">Conversation</p><h1 className="mt-3 font-display text-4xl">Your AI Sales Engineer is ready.</h1></div><div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]"><ChatSection /><aside className="hidden space-y-4 lg:block"><div className="rounded-card border border-line bg-paper p-6"><h2 className="font-display text-2xl">Your plan fit</h2><p className="mt-2 text-sm leading-6 text-ink-soft">Ask about your stack and team. These are the available paths.</p><div className="mt-5 space-y-3">{plans.map(plan => <Link key={plan.id} to="/pricing" className="block rounded-xl border border-line p-3 hover:border-crimson"><div className="font-semibold">{plan.name}</div><div className="mt-1 text-xs text-ink-soft">{plan.label}</div></Link>)}</div></div></aside></div></Container></section>
}
