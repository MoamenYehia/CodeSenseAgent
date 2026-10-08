import type { ReactNode } from 'react'
import { cn } from '../../lib/cn'

interface BadgeProps {
  children: ReactNode
  tone?: 'sand' | 'mist' | 'crimson'
  className?: string
}

export function Badge({ children, tone = 'sand', className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold text-ink',
        tone === 'sand' && 'bg-sand',
        tone === 'mist' && 'bg-mist',
        tone === 'crimson' && 'bg-crimson text-cream',
        className,
      )}
    >
      {children}
    </span>
  )
}
