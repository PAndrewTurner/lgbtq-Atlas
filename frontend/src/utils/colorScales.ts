import * as d3 from 'd3'

export const SCORE_COLORS = {
  low:    '#C0392B',
  midLow: '#E67E22',
  mid:    '#F1C40F',
  high:   '#27AE60',
  top:    '#1ABC9C',
}

export const scoreColorScale = d3.scaleThreshold<number, string>()
  .domain([30, 45, 60, 75])
  .range([SCORE_COLORS.low, SCORE_COLORS.midLow, SCORE_COLORS.mid, SCORE_COLORS.high, SCORE_COLORS.top])

export const DIMENSION_META: Record<string, { label: string; color: string; icon: string }> = {
  legal:     { label: 'Legal Protections',  color: '#8B5CF6', icon: '⚖️' },
  safety:    { label: 'Physical Safety',    color: '#EF4444', icon: '🛡️' },
  health:    { label: 'Healthcare Access',  color: '#10B981', icon: '❤️' },
  economic:  { label: 'Economic Equity',    color: '#F59E0B', icon: '💼' },
  community: { label: 'Community Presence', color: '#3B82F6', icon: '🏳️‍🌈' },
  youth:     { label: 'Youth Support',      color: '#14B8A6', icon: '🎓' },
}

export function scoreToColor(score: number): string {
  return scoreColorScale(score)
}

export function scoreToLabel(score: number): string {
  if (score >= 75) return 'Thriving'
  if (score >= 60) return 'Supportive'
  if (score >= 45) return 'Mixed'
  if (score >= 30) return 'Challenging'
  return 'Hostile'
}
