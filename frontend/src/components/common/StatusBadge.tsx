import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, Info, Database } from 'lucide-react';

interface StatusBadgeProps {
  state: string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ state, size = 'md' }) => {
  const normalized = (state || 'UNKNOWN').toUpperCase();

  let colorClasses = 'bg-slate-800 text-slate-300 border-slate-700';
  let Icon = Info;
  let glow = '';

  if (normalized === 'NORMAL' || normalized === 'ONLINE' || normalized === 'STABLE' || normalized === 'CONNECTED') {
    colorClasses = 'bg-emerald-950/80 text-emerald-400 border-emerald-800/80';
    Icon = ShieldCheck;
    glow = 'glow-emerald';
  } else if (normalized === 'WATCH') {
    colorClasses = 'bg-blue-950/80 text-blue-400 border-blue-800/80';
    Icon = Info;
    glow = 'glow-blue';
  } else if (normalized === 'ELEVATED' || normalized === 'WARNING' || normalized === 'DEGRADED') {
    colorClasses = 'bg-amber-950/80 text-amber-400 border-amber-800/80';
    Icon = AlertTriangle;
    glow = 'glow-amber';
  } else if (normalized === 'HIGH RISK' || normalized === 'CRITICAL' || normalized === 'DISCONNECTED') {
    colorClasses = 'bg-rose-950/80 text-rose-400 border-rose-800/80';
    Icon = AlertOctagon;
    glow = 'glow-rose';
  } else if (normalized === 'BASELINE_COLLECTION' || normalized === 'COLLECTING') {
    colorClasses = 'bg-cyan-950/80 text-cyan-400 border-cyan-800/80';
    Icon = Database;
    glow = 'glow-blue';
  }

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 gap-1',
    md: 'text-xs font-semibold px-2.5 py-1 gap-1.5',
    lg: 'text-sm font-bold px-3.5 py-1.5 gap-2'
  }[size];

  return (
    <span className={`inline-flex items-center rounded-full border uppercase tracking-wider ${sizeClasses} ${colorClasses} ${glow}`}>
      <Icon className={size === 'lg' ? 'w-4 h-4' : 'w-3.5 h-3.5'} />
      <span>{normalized.replace('_', ' ')}</span>
    </span>
  );
};
