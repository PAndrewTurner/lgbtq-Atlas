import type { ReactNode } from 'react'

interface StatCardProps {
  label: string
  value: ReactNode
  sub?: string
  color?: string
}

export function StatCard({ label, value, sub, color }: StatCardProps) {
  return (
    <div className="bg-[var(--surface-alt)] rounded-lg p-3">
      <div className="text-xs text-[var(--text-muted)] mb-1">{label}</div>
      <div className="text-xl font-display" style={color ? { color } : undefined}>
        {value}
      </div>
      {sub && <div className="text-xs text-[var(--text-secondary)] mt-0.5">{sub}</div>}
    </div>
  )
}
