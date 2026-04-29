import { LineChart, Line, ResponsiveContainer, Tooltip } from 'recharts'
import type { TrendPoint } from '../../types/profile'

interface TrendSparklineProps {
  data: TrendPoint[]
  color?: string
  height?: number
}

export function TrendSparkline({ data, color = '#3B82F6', height = 48 }: TrendSparklineProps) {
  if (!data?.length) return null

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="composite_score"
          stroke={color}
          strokeWidth={2}
          dot={false}
          isAnimationActive={false}
        />
        <Tooltip
          contentStyle={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 6,
            fontSize: 11,
          }}
          formatter={(v: number) => [v.toFixed(1), 'Score']}
          labelFormatter={(l) => `Year: ${l}`}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
