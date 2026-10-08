import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cn } from '../../lib/cn'

type ButtonVariant = 'primary' | 'secondary' | 'ghost'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  children: ReactNode
}

export function Button({ variant = 'primary', className, children, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex min-h-11 items-center justify-center gap-2 rounded-full px-5 text-sm font-semibold transition-colors duration-200',
        'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-crimson',
        variant === 'primary' && 'bg-crimson text-cream hover:bg-crimson-deep',
        variant === 'secondary' && 'border-[1.5px] border-crimson bg-transparent text-crimson hover:bg-crimson-tint',
        variant === 'ghost' && 'text-crimson hover:bg-crimson-tint',
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}
