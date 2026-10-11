import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number | null | undefined;
  unit?: string;
  subtitle?: string;
  icon?: LucideIcon;
  badge?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  accentColor?: 'blue' | 'emerald' | 'amber' | 'rose' | 'cyan' | 'purple';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  unit,
  subtitle,
  icon: Icon,
  badge,
  trend,
  trendValue,
  accentColor = 'blue'
}) => {
  const accentBorder = {
    blue: 'hover:border-blue-500/50',
    emerald: 'hover:border-emerald-500/50',
    amber: 'hover:border-amber-500/50',
    rose: 'hover:border-rose-500/50',
    cyan: 'hover:border-cyan-500/50',
    purple: 'hover:border-purple-500/50'
  }[accentColor];

  const iconColor = {
    blue: 'text-blue-400 bg-blue-950/60 border-blue-800/50',
    emerald: 'text-emerald-400 bg-emerald-950/60 border-emerald-800/50',
    amber: 'text-amber-400 bg-amber-950/60 border-amber-800/50',
    rose: 'text-rose-400 bg-rose-950/60 border-rose-800/50',
    cyan: 'text-cyan-400 bg-cyan-950/60 border-cyan-800/50',
    purple: 'text-purple-400 bg-purple-950/60 border-purple-800/50'
  }[accentColor];

  return (
    <div className={`bg-[#111827] border border-[#1F2937] rounded-xl p-4 transition-all duration-200 shadow-lg ${accentBorder}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-1.5 rounded-lg border ${iconColor}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-2xl font-extrabold text-white tracking-tight">
          {value !== null && value !== undefined ? value : <span className="text-slate-600 text-lg">Unavailable</span>}
        </span>
        {unit && value !== null && value !== undefined && (
          <span className="text-xs font-semibold text-slate-400">{unit}</span>
        )}
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>{subtitle || ''}</span>
        {badge && <div>{badge}</div>}
        {trendValue && (
          <span className={trend === 'up' ? 'text-amber-400' : trend === 'down' ? 'text-emerald-400' : 'text-slate-400'}>
            {trendValue}
          </span>
        )}
      </div>
    </div>
  );
};
