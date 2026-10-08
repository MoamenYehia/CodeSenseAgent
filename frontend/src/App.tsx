import { Route, Routes } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import { ScrollToTop } from './components/layout/ScrollToTop'
import { Chat } from './pages/Chat'
import { Home } from './pages/Home'
import { NotFound } from './pages/NotFound'
import { PlaceholderPage } from './pages/PlaceholderPage'
import { ChatProvider } from './components/chat/ChatProvider'
import { ChatLauncher } from './components/chat/ChatUI'
import { Pricing } from './pages/Pricing'

export function App() {
  return (
    <ChatProvider><Layout>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/platform" element={<PlaceholderPage kind="platform" />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/security" element={<PlaceholderPage kind="security" />} />
        <Route path="/how-it-works" element={<PlaceholderPage kind="how" />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
      </Layout><ChatLauncher /></ChatProvider>
  )
}
