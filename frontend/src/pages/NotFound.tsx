import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Container } from '../components/ui/Container'

export function NotFound() {
  return <section className="min-h-[60vh] py-28"><Container className="text-center"><p className="font-mono text-sm text-crimson">404</p><h1 className="mt-4 font-display text-5xl">That page wandered off.</h1><p className="mx-auto mt-4 max-w-md text-ink-soft">Let’s get you back to the CodeSense AI homepage.</p><Link to="/" className="mt-8 inline-block"><Button>Back home</Button></Link></Container></section>
}
