import type { ReactNode } from 'react'
import { Header } from './Header'
import { Footer } from './Footer'
import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

export function Layout({ children }: { children: ReactNode }) {
  const location = useLocation()
  useEffect(() => { const name = location.pathname === '/' ? 'Home' : location.pathname.slice(1).replace('-', ' '); document.title = `${name.charAt(0).toUpperCase() + name.slice(1)} | CodeSense AI` }, [location.pathname])
  return (
    <div className="min-h-screen">
      <Header />
      <main id="main-content">{children}</main>
      <Footer />
    </div>
  )
}
