import { ArrowRight, Check, GitBranch, ShieldCheck, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Badge } from '../components/ui/Badge'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Container } from '../components/ui/Container'
import { Section } from '../components/ui/Section'

const capabilities = [
  ['Real-time PR reviews', 'Find security issues, logic flaws, memory leaks, and performance bottlenecks inside the pull request.', ShieldCheck],
  ['Automated refactoring', 'Turn review findings into clear, actionable suggestions with a path toward a safer codebase.', Sparkles],
  ['Dependency & secret scanning', 'Catch exposed API keys, private tokens, and vulnerable dependencies before they ship.', GitBranch],
  ['Architecture guardrails', 'Surface high-complexity functions, N+1 query patterns, and architectural regressions.', Check],
]

export function Home() {
  return (
    <>
      <section className="texture overflow-hidden border-b border-line">
        <Container className="grid gap-12 py-20 md:grid-cols-[1.05fr_.95fr] md:items-center md:py-28">
          <div>
            <Badge tone="mist">AI-native code confidence</Badge>
            <h1 className="mt-6 max-w-3xl font-display text-5xl leading-[1.04] tracking-tight text-ink sm:text-6xl">
              Code review that keeps pace with <em className="text-crimson">ambition.</em>
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-8 text-ink-soft">
              AI-powered code review and security analysis for every pull request, built to meet your team inside the workflow.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/chat"><Button>Talk to an AI Sales Engineer <ArrowRight size={17} /></Button></Link>
              <Link to="/pricing"><Button variant="secondary">Explore plans</Button></Link>
            </div>
          </div>
          <Card className="relative overflow-hidden p-5 sm:p-7">
            <div className="flex items-center justify-between border-b border-line pb-4">
              <span className="font-mono text-xs text-ink-soft">src/auth/session.ts</span>
              <Badge tone="crimson">Security finding</Badge>
            </div>
            <div className="mt-6 rounded-lg bg-crimson-deep p-4 font-mono text-xs leading-7 text-cream">
              <div><span className="text-mist">−</span> const token = process.env.API_KEY</div>
              <div><span className="text-sand">+</span> const token = getSecret('API_KEY')</div>
            </div>
            <div className="mt-5 rounded-lg border border-line bg-cream p-4">
              <div className="flex items-center gap-2 text-sm font-semibold"><ShieldCheck size={17} className="text-success" /> Hardcoded secret prevented</div>
              <p className="mt-2 text-sm leading-6 text-ink-soft">Use your secret manager instead of reading credentials from source.</p>
            </div>
            <p className="mt-4 text-right text-xs text-ink-soft">Illustrative preview</p>
          </Card>
        </Container>
      </section>
      <Section>
        <Container>
          <p className="text-center text-sm font-medium text-ink-soft">Works with the tools your team already uses</p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            {['GitHub', 'GitLab', 'Bitbucket'].map((name) => <Badge key={name} tone="sand"><GitBranch size={14} /> {name}</Badge>)}
          </div>
        </Container>
      </Section>
      <Section className="bg-paper">
        <Container>
          <div className="max-w-2xl"><p className="font-mono text-xs uppercase tracking-[.2em] text-crimson">Platform</p><h2 className="mt-4 font-display text-4xl tracking-tight">The signal your pull requests need.</h2></div>
          <div className="mt-12 grid gap-5 md:grid-cols-2">
            {capabilities.map(([title, description, Icon]) => {
              const CapabilityIcon = Icon as typeof ShieldCheck
              return <Card key={title as string} className="p-6"><CapabilityIcon className="text-crimson" /><h3 className="mt-5 font-display text-2xl">{title as string}</h3><p className="mt-3 leading-7 text-ink-soft">{description as string}</p></Card>
            })}
          </div>
        </Container>
      </Section>
      <section className="bg-crimson py-20 text-cream md:py-24">
        <Container className="flex flex-col items-start justify-between gap-8 md:flex-row md:items-center">
          <div><p className="font-mono text-xs uppercase tracking-[.2em] text-mist">Find your fit</p><h2 className="mt-4 max-w-2xl font-display text-4xl">Not sure which plan fits?</h2><p className="mt-4 max-w-xl leading-7 text-cream/80">Ask our AI Sales Engineer about your stack, team, and deployment needs.</p></div>
          <Link to="/chat"><Button className="shrink-0 bg-cream text-crimson hover:bg-sand">Start a conversation <ArrowRight size={17} /></Button></Link>
        </Container>
      </section>
    </>
  )
}
