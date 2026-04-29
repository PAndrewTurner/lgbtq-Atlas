import { LayerSwitcher } from './LayerSwitcher'
import { SearchBar } from './SearchBar'

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-20 bg-[var(--surface)]/90 backdrop-blur border-b border-[var(--border)] px-4 h-12 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3 flex-shrink-0">
        <span className="font-display text-base text-[var(--text-primary)] leading-none">
          LGBTQ+ Atlas
        </span>
        <span className="text-[var(--text-muted)] text-xs hidden sm:block">2024</span>
      </div>

      <div className="flex-1 flex items-center justify-center">
        <LayerSwitcher />
      </div>

      <SearchBar />
    </header>
  )
}
