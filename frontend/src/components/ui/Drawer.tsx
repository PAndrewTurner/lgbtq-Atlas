import { useEffect, type ReactNode } from 'react'
import { X } from 'lucide-react'

interface DrawerProps {
  onClose?: () => void
  children: ReactNode
  title?: string
}

export function Drawer({ onClose, children, title }: DrawerProps) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === 'Escape' && onClose?.()
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  return (
    <aside className="w-[420px] flex-shrink-0 bg-[var(--surface)] border-l border-[var(--border)] flex flex-col overflow-hidden">
      <div className="flex items-center gap-2 px-5 py-4 border-b border-[var(--border)] flex-shrink-0">
        {title && (
          <h2 className="font-display text-base text-[var(--text-primary)] truncate">{title}</h2>
        )}
        {onClose && (
          <button
            onClick={onClose}
            className="ml-auto shrink-0 p-1.5 rounded hover:bg-[var(--surface-alt)] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors"
            aria-label="Close"
          >
            <X size={18} />
          </button>
        )}
      </div>
      <div className="flex-1 overflow-y-auto">{children}</div>
    </aside>
  )
}
