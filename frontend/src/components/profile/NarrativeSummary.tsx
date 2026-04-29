interface NarrativeSummaryProps {
  narrative?: string
}

export function NarrativeSummary({ narrative }: NarrativeSummaryProps) {
  if (!narrative) return null

  return (
    <div className="rounded-lg border border-[var(--border)] p-4 bg-[var(--surface-alt)]">
      <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-2">
        AI Summary
      </div>
      <p className="text-sm text-[var(--text-secondary)] leading-relaxed">{narrative}</p>
    </div>
  )
}
