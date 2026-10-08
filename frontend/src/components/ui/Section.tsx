import type { HTMLAttributes, ReactNode } from 'react'
import { cn } from '../../lib/cn'

interface SectionProps extends HTMLAttributes<HTMLElement> {
  children: ReactNode
}

export function Section({ children, className, ...props }: SectionProps) {
  return (
    <section className={cn('py-20 md:py-28', className)} {...props}>
      {children}
    </section>
  )
}
