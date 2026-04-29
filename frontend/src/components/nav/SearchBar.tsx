import { useState, useRef, useEffect } from 'react'
import { Search } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { atlasApi } from '../../api/atlas'
import { useAtlasStore } from '../../store/atlasStore'

export function SearchBar() {
  const [q, setQ] = useState('')
  const [open, setOpen] = useState(false)
  const { setSelectedFips } = useAtlasStore()
  const ref = useRef<HTMLDivElement>(null)

  const { data: results } = useQuery({
    queryKey: ['search', q],
    queryFn: () => atlasApi.search(q),
    enabled: q.length >= 2,
    staleTime: 30_000,
  })

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={ref} className="relative w-56">
      <div className="flex items-center gap-2 bg-[var(--surface-alt)] border border-[var(--border)] rounded-lg px-3 py-1.5">
        <Search size={14} className="text-[var(--text-muted)]" />
        <input
          value={q}
          onChange={(e) => { setQ(e.target.value); setOpen(true) }}
          onFocus={() => setOpen(true)}
          placeholder="Search states & cities…"
          className="bg-transparent text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] outline-none w-full"
        />
      </div>

      {open && results && results.length > 0 && (
        <div className="absolute top-full mt-1 left-0 right-0 bg-[var(--surface)] border border-[var(--border)] rounded-lg shadow-xl z-50 max-h-60 overflow-y-auto">
          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => {
                if (r.type === 'state' && r.fips) setSelectedFips(r.fips)
                setQ('')
                setOpen(false)
              }}
              className="w-full text-left px-3 py-2 text-sm hover:bg-[var(--surface-alt)] flex items-center gap-2"
            >
              <span className="text-[var(--text-muted)] text-xs w-10 flex-shrink-0">
                {r.type === 'state' ? 'State' : r.state_abbr}
              </span>
              <span className="text-[var(--text-primary)]">{r.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
