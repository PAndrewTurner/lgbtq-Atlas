import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface TrendArrowProps {
  value: number
  threshold?: number
  size?: number
}

export function TrendArrow({ value, threshold = 1, size = 16 }: TrendArrowProps) {
  if (value > threshold) return <TrendingUp size={size} className="text-[var(--health)]" />
  if (value < -threshold) return <TrendingDown size={size} className="text-[var(--safety)]" />
  return <Minus size={size} className="text-[var(--text-muted)]" />
}
