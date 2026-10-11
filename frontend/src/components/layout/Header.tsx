import React from 'react';
import { StatusBadge } from '../common/StatusBadge';
import { TelemetrySnapshot, PredictionResult } from '../../types';
import { Network, Router, Laptop, ShieldAlert } from 'lucide-react';

interface HeaderProps {
  title: string;
  telemetry: TelemetrySnapshot | null;
  prediction: PredictionResult | null;
  alertCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  title,
  telemetry,
  prediction,
  alertCount
}) => {
  return (
    <header className="h-16 bg-[#0E1320] border-b border-[#1F2937] px-6 flex items-center justify-between sticky top-0 z-30 ml-64">
      {/* Page Title */}
      <div className="flex items-center gap-3">
        <h1 className="text-lg font-bold text-white tracking-tight">{title}</h1>
      </div>

      {/* Network Header Pills */}
      <div className="flex items-center gap-3">
        {/* Active SSID Pill */}
        <div className="flex items-center gap-2 bg-[#141C2E] border border-slate-700/60 rounded-lg px-3 py-1.5 text-xs">
          <Network className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-400 font-medium">SSID:</span>
          <span className="font-mono font-bold text-slate-200">
            {telemetry?.ssid_hash ? telemetry.ssid_hash : 'Detecting...'}
          </span>
        </div>

        {/* Dynamic Gateway IP Pill */}
        <div className="flex items-center gap-2 bg-[#141C2E] border border-slate-700/60 rounded-lg px-3 py-1.5 text-xs">
          <Router className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400 font-medium">Gateway:</span>
          <span className="font-mono font-bold text-emerald-300">
            {telemetry?.gateway_ip ? telemetry.gateway_ip : 'Searching route...'}
          </span>
        </div>

        {/* Local IP Pill */}
        <div className="flex items-center gap-2 bg-[#141C2E] border border-slate-700/60 rounded-lg px-3 py-1.5 text-xs">
          <Laptop className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400 font-medium">Local:</span>
          <span className="font-mono font-bold text-cyan-300">
            {telemetry?.local_ip ? telemetry.local_ip : '127.0.0.1'}
          </span>
        </div>

        {/* AI Prediction Status Badge */}
        {prediction && (
          <StatusBadge
            state={prediction.prediction_state || 'COLLECTING_BASELINE'}
            size="md"
          />
        )}

        {/* Alert Indicator */}
        {alertCount > 0 && (
          <div className="flex items-center gap-1.5 bg-rose-950/60 border border-rose-800/80 text-rose-300 px-2.5 py-1 rounded-lg text-xs font-bold">
            <ShieldAlert className="w-3.5 h-3.5 text-rose-400 animate-pulse" />
            <span>{alertCount}</span>
          </div>
        )}
      </div>
    </header>
  );
};
