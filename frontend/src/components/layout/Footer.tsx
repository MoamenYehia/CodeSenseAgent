import { Link } from 'react-router-dom'
import { Container } from '../ui/Container'

export function Footer() {
  return (
    <footer className="border-t border-line bg-paper py-12">
      <Container className="flex flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">
        <div className="max-w-sm">
          <Link to="/" className="font-display text-xl font-semibold text-crimson">CodeSense AI</Link>
          <p className="mt-3 text-sm leading-6 text-ink-soft">AI-powered code review and security analysis for every pull request.</p>
        </div>
        <div className="flex gap-12 text-sm">
          <div className="flex flex-col gap-3">
            <span className="font-semibold text-ink">Product</span>
            <Link to="/platform" className="text-ink-soft hover:text-crimson">Platform</Link>
            <Link to="/pricing" className="text-ink-soft hover:text-crimson">Plans</Link>
            <Link to="/security" className="text-ink-soft hover:text-crimson">Security</Link>
          </div>
          <div className="flex flex-col gap-3">
            <span className="font-semibold text-ink">Explore</span>
            <Link to="/how-it-works" className="text-ink-soft hover:text-crimson">How it works</Link>
            <Link to="/chat" className="text-ink-soft hover:text-crimson">Talk to our AI</Link>
          </div>
        </div>
      </Container>
      <Container className="mt-10 border-t border-line pt-5 text-xs text-ink-soft">
        Avoid sharing secrets or credentials in chat. This conversation lasts for your current session.
      </Container>
    </footer>
  )
}
