import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { useAtlasStore } from './store/atlasStore.ts'

// Expose store in dev for testing
if (import.meta.env.DEV) {
  (window as unknown as Record<string, unknown>).__atlasStore = useAtlasStore
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
