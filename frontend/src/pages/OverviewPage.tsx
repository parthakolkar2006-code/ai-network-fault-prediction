import React from 'react';
import { MetricCard } from '../components/common/MetricCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { TelemetrySnapshot, PredictionResult } from '../types';
import {
  Wifi,
  Router,
  Globe,
  ArrowDownUp,
  BrainCircuit,
  Zap,
  Radio,
  Clock,
  ShieldAlert
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip
} from 'recharts';

interface OverviewPageProps {
  telemetry: TelemetrySnapshot | null;
  prediction: PredictionResult | null;
  historyPoints: TelemetrySnapshot[];
}

export const OverviewPage: React.FC<OverviewPageProps> = ({
  telemetry,
  prediction,
  historyPoints
}) => {
  const chartData = historyPoints.map((pt) => ({
    time: pt.timestamp ? pt.timestamp.split(' ')[1] : '',
    gwLat: pt.gateway_latency,
    inetLat: pt.internet_latency,
    gwLoss: pt.gateway_packet_loss,
    inetLoss: pt.internet_packet_loss,
    signal: pt.signal_strength,
    downMbps: pt.download_mbps,
    upMbps: pt.upload_mbps
  }));

  return (
    <div className="space-y-6">
      {/* Top Banner: AI 30-Minute Degradation Risk */}
      <div className="bg-gradient-to-r from-[#141C2E] via-[#111827] to-[#151D30] border border-blue-900/40 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <BrainCircuit className="w-5 h-5 text-blue-400" />
              <span className="text-xs font-bold text-blue-400 uppercase tracking-widest">
                Predictive AI Network Engine
              </span>
            </div>
            <h2 className="text-2xl font-extrabold text-white tracking-tight mb-1">
              30-Minute Network Degradation Forecast
            </h2>
            <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
              Continuous causal inference evaluating local gateway stability, internet health delta, signal dynamics, and sustained telemetry indicators.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-[#0A0E17]/80 border border-slate-800 rounded-xl p-4 min-w-[280px]">
            <div className="text-right flex-1">
              <span className="text-[11px] text-slate-400 block font-medium">Risk Assessment</span>
              <div className="text-xl font-black text-white mt-0.5">
                {prediction?.risk_probability !== null && prediction?.risk_probability !== undefined
                  ? `${(prediction.risk_probability * 100).toFixed(1)}%`
                  : <span className="text-sm font-semibold text-cyan-400">Baseline Telemetry</span>}
              </div>
              <span className="text-[10px] text-slate-500 font-mono">
                {prediction?.threshold ? `Threshold: ${prediction.threshold}` : 'Collecting Samples'}
              </span>
            </div>
            <div>
              <StatusBadge
                state={prediction?.prediction_state || 'BASELINE_COLLECTION'}
                size="lg"
              />
            </div>
          </div>
        </div>

        {/* Cold Start Notice If Applicable */}
        {prediction?.status === 'COLLECTING_BASELINE' && (
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-cyan-300/90 font-mono">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              <span>{prediction.message}</span>
            </div>
            <span className="text-slate-500 text-[11px]">Domain shift compliance active: No fabricated probabilities</span>
          </div>
        )}
      </div>

      {/* Grid: Local Network vs Internet Health vs Wi-Fi vs Traffic */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Local Gateway Health */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Router className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">Local Gateway</span>
            </div>
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${telemetry?.gateway_reachable ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'}`}>
              {telemetry?.gateway_reachable ? 'REACHABLE' : 'UNREACHABLE'}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div>
              <span className="text-[10px] text-slate-400 block">Latency</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.gateway_latency !== null && telemetry?.gateway_latency !== undefined ? `${telemetry.gateway_latency}ms` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Loss</span>
              <span className={`text-base font-bold font-mono ${(telemetry?.gateway_packet_loss || 0) > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {telemetry?.gateway_packet_loss !== null && telemetry?.gateway_packet_loss !== undefined ? `${telemetry.gateway_packet_loss}%` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Jitter</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.gateway_jitter !== null && telemetry?.gateway_jitter !== undefined ? `${telemetry.gateway_jitter}ms` : '0ms'}
              </span>
            </div>
          </div>
          <div className="text-[11px] text-slate-400 font-mono truncate">
            Target: <span className="text-slate-300 font-semibold">{telemetry?.gateway_ip || 'Discovering...'}</span>
          </div>
        </div>

        {/* Internet Health */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-blue-400" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">Internet Health</span>
            </div>
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${telemetry?.internet_reachable ? 'bg-blue-950 text-blue-400 border border-blue-800' : 'bg-rose-950 text-rose-400 border border-rose-800'}`}>
              {telemetry?.internet_reachable ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div>
              <span className="text-[10px] text-slate-400 block">Latency</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.internet_latency !== null && telemetry?.internet_latency !== undefined ? `${telemetry.internet_latency}ms` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Loss</span>
              <span className={`text-base font-bold font-mono ${(telemetry?.internet_packet_loss || 0) > 0 ? 'text-amber-400' : 'text-blue-400'}`}>
                {telemetry?.internet_packet_loss !== null && telemetry?.internet_packet_loss !== undefined ? `${telemetry.internet_packet_loss}%` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Jitter</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.internet_jitter !== null && telemetry?.internet_jitter !== undefined ? `${telemetry.internet_jitter}ms` : '0ms'}
              </span>
            </div>
          </div>
          <div className="text-[11px] text-slate-400 font-mono truncate">
            Target: <span className="text-slate-300 font-semibold">1.1.1.1 (Cloudflare Edge)</span>
          </div>
        </div>

        {/* Wi-Fi Interface & Signal */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Wifi className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">Wi-Fi Radio</span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
              {telemetry?.radio_type || '802.11'}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div>
              <span className="text-[10px] text-slate-400 block">Signal</span>
              <span className="text-base font-bold text-cyan-300 font-mono">
                {telemetry?.signal_strength ? `${telemetry.signal_strength}%` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Rate</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.link_speed ? `${telemetry.link_speed}M` : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Channel</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.wifi_channel || 'N/A'}
              </span>
            </div>
          </div>
          <div className="text-[11px] text-slate-400 font-mono truncate">
            RSSI: <span className="text-slate-300 font-semibold">{telemetry?.rssi_dbm ? `${telemetry.rssi_dbm} dBm` : 'N/A'}</span>
          </div>
        </div>

        {/* Live Traffic */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <ArrowDownUp className="w-4 h-4 text-purple-400" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">Traffic & Errors</span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-400 border border-purple-800">
              {telemetry?.interface_status || 'UP'}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <span className="text-[10px] text-slate-400 block">Download</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.download_mbps !== undefined ? `${telemetry.download_mbps} Mbps` : '0.00 Mbps'}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block">Upload</span>
              <span className="text-base font-bold text-white font-mono">
                {telemetry?.upload_mbps !== undefined ? `${telemetry.upload_mbps} Mbps` : '0.00 Mbps'}
              </span>
            </div>
          </div>
          <div className="text-[11px] text-slate-400 font-mono truncate">
            Errors / Discards: <span className="text-slate-300 font-semibold">{telemetry?.packet_errors || 0} / {telemetry?.packet_discards || 0}</span>
          </div>
        </div>
      </div>

      {/* Real-Time Telemetry Sparklines */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Latency Comparison Chart */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white tracking-wide">Path Latency Dynamics</h3>
              <p className="text-xs text-slate-400">Comparing Local Gateway vs External Internet (1.1.1.1)</p>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                <span className="text-slate-300">Gateway</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-400" />
                <span className="text-slate-300">Internet</span>
              </div>
            </div>
          </div>

          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="ms" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="gwLat" name="Gateway Latency" stroke="#10B981" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="inetLat" name="Internet Latency" stroke="#3B82F6" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Packet Loss & Signal Chart */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white tracking-wide">Signal & Packet Loss</h3>
              <p className="text-xs text-slate-400">Wi-Fi Signal Strength (%) and Packet Loss (%)</p>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
                <span className="text-slate-300">Signal %</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-400" />
                <span className="text-slate-300">Loss %</span>
              </div>
            </div>
          </div>

          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="%" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="signal" name="Signal Strength" stroke="#06B6D4" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="gwLoss" name="Gateway Loss" stroke="#F43F5E" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
