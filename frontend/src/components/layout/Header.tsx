import { Menu, MessageCircle, X } from 'lucide-react'
import { Link, NavLink } from 'react-router-dom'
import { useState } from 'react'
import { Button } from '../ui/Button'
import { cn } from '../../lib/cn'
import { useChat } from '../chat/ChatProvider'

const links = [
  { label: 'Platform', to: '/platform' },
  { label: 'Plans', to: '/pricing' },
  { label: 'Security', to: '/security' },
  { label: 'How it works', to: '/how-it-works' },
]

function Mark() {
  return (
    <svg aria-hidden="true" className="h-8 w-8" viewBox="0 0 32 32" fill="none">
      <path d="M12 7 5.5 16 12 25M20 7l6.5 9-6.5 9" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" />
      <path d="m12.5 16 3 3 5-6" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function Header() {
  const [open, setOpen] = useState(false)
  const { setDrawer } = useChat()
  return (
    <header className="sticky top-0 z-40 border-b border-line/80 bg-cream/95 backdrop-blur">
      <div className="mx-auto flex h-[76px] max-w-[1200px] items-center justify-between px-5 sm:px-8">
        <Link to="/" className="flex items-center gap-2 text-crimson" aria-label="CodeSense AI home" onClick={() => setOpen(false)}>
          <Mark />
          <span className="font-display text-xl font-semibold tracking-tight">CodeSense AI</span>
        </Link>
        <nav className="hidden items-center gap-7 md:flex" aria-label="Primary navigation">
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} className={({ isActive }) => cn('text-sm font-medium text-ink-soft transition-colors hover:text-crimson', isActive && 'text-crimson')}>
              {link.label}
            </NavLink>
          ))}
        </nav>
        <Button className="hidden md:inline-flex" onClick={() => setDrawer(true)}><MessageCircle size={17} /> Talk to an AI Sales Engineer</Button>
        <button
          type="button"
          aria-label={open ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={open}
          className="rounded-lg p-2 text-crimson md:hidden"
          onClick={() => setOpen((current) => !current)}
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>
      {open && (
        <nav className="border-t border-line bg-cream px-5 py-4 md:hidden" aria-label="Mobile navigation">
          <div className="mx-auto flex max-w-[1200px] flex-col gap-1">
            {links.map((link) => (
              <NavLink key={link.to} to={link.to} onClick={() => setOpen(false)} className="rounded-lg px-3 py-3 font-medium text-ink hover:bg-crimson-tint">
                {link.label}
              </NavLink>
            ))}
            <Link to="/chat" onClick={() => setOpen(false)} className="mt-2">
              <Button className="w-full"><MessageCircle size={17} /> Start conversation</Button>
            </Link>
          </div>
        </nav>
      )}
    </header>
  )
}
