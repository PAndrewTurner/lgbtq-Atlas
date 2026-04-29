import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Header } from './components/nav/Header'
import { AtlasMap } from './components/map/AtlasMap'
import { StateProfileDrawer } from './components/profile/StateProfileDrawer'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="fixed inset-0 flex flex-col bg-[var(--bg)]">
        <Header />
        <div className="flex-1 flex overflow-hidden" style={{ marginTop: '48px' }}>
          <main className="flex-1 relative">
            <AtlasMap />
          </main>
          <StateProfileDrawer />
        </div>
      </div>
    </QueryClientProvider>
  )
}

export default App
