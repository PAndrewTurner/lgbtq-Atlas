import type { Organization } from '../../types/profile'

function formatRevenue(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`
  return n > 0 ? `$${n}` : '—'
}

interface Props {
  organizations: Organization[]
}

export function CommunityPanel({ organizations }: Props) {
  if (!organizations.length) return null

  return (
    <div className="space-y-2">
      <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
        LGBTQ+ Organizations
      </div>
      <div className="space-y-1.5">
        {organizations.map((org, i) => (
          <div
            key={i}
            className="bg-[var(--surface-alt)] rounded-lg px-3 py-2.5 flex items-start justify-between gap-3"
          >
            <div className="min-w-0">
              <div className="text-sm font-medium text-[var(--text-primary)] truncate leading-snug">
                {org.org_name_display}
              </div>
              <div className="text-xs text-[var(--text-muted)] mt-0.5">
                {org.org_addr_city}
                {org.ntee_code_definition ? ` · ${org.ntee_code_definition}` : ''}
              </div>
            </div>
            {org.revenue_amount > 0 && (
              <div className="shrink-0 text-xs font-mono text-[var(--community)] mt-0.5">
                {formatRevenue(org.revenue_amount)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
