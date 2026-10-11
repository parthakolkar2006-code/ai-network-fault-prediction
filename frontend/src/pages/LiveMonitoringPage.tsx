import React from 'react';
import { TelemetrySnapshot } from '../types';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';
import { Radio, Gauge, Activity, ArrowDownUp, Waves } from 'lucide-react';

interface LiveMonitoringPageProps {
  telemetry: TelemetrySnapshot | null;
  historyPoints: TelemetrySnapshot[];
  isConnected: boolean;
}

export const LiveMonitoringPage: React.FC<LiveMonitoringPageProps> = ({
  telemetry,
  historyPoints,
  isConnected
}) => {
  const chartData = historyPoints.map((pt) => ({
    time: pt.timestamp ? pt.timestamp.split(' ')[1] : '',
    gwLat: pt.gateway_latency,
    inetLat: pt.internet_latency,
    gwLoss: pt.gateway_packet_loss,
    inetLoss: pt.internet_packet_loss,
    gwJitter: pt.gateway_jitter,
    inetJitter: pt.internet_jitter,
    signal: pt.signal_strength,
    speed: pt.link_speed,
    downMbps: pt.download_mbps,
    upMbps: pt.upload_mbps
  }));

  return (
    <div className="space-y-6">
      {/* Live Stream Header Indicator */}
      <div className="flex items-center justify-between bg-[#111827] border border-[#1F2937] rounded-xl px-5 py-3">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Radio className={`w-5 h-5 ${isConnected ? 'text-emerald-400' : 'text-rose-500'}`} />
            {isConnected && (
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
            )}
          </div>
          <div>
            <h2 className="text-sm font-bold text-white tracking-wide">
              High-Frequency Live Telemetry Stream
            </h2>
            <p className="text-xs text-slate-400">
              Bi-directional WebSocket streaming at 2.0s refresh intervals. Continuous non-blocking network telemetry.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="text-slate-400">Sample Buffer:</span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-bold">
            {historyPoints.length} frames
          </span>
        </div>
      </div>

      {/* Row 1: Dual Path Latency & Jitter */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Latency Dynamics */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Path Latency (Round Trip Time)</h3>
                <span className="text-[11px] text-slate-400">Unit: Milliseconds (ms)</span>
              </div>
            </div>
            <div className="text-right font-mono text-xs">
              <span className="text-emerald-400 font-bold">{telemetry?.gateway_latency ?? 'N/A'} ms (GW)</span>
              <span className="text-slate-600 mx-1.5">|</span>
              <span className="text-blue-400 font-bold">{telemetry?.internet_latency ?? 'N/A'} ms (Inet)</span>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="ms" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="gwLat" name="Gateway Latency" stroke="#10B981" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="inetLat" name="Internet Latency" stroke="#3B82F6" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Jitter Dynamics */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Waves className="w-4 h-4 text-cyan-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Latency Variance (Jitter)</h3>
                <span className="text-[11px] text-slate-400">Unit: Milliseconds (ms)</span>
              </div>
            </div>
            <div className="text-right font-mono text-xs">
              <span className="text-cyan-400 font-bold">{telemetry?.gateway_jitter ?? '0'} ms (GW)</span>
              <span className="text-slate-600 mx-1.5">|</span>
              <span className="text-purple-400 font-bold">{telemetry?.internet_jitter ?? '0'} ms (Inet)</span>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="ms" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="gwJitter" name="Gateway Jitter" stroke="#06B6D4" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="inetJitter" name="Internet Jitter" stroke="#A855F7" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 2: Packet Loss & Traffic Throughput */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Packet Loss Rates */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-rose-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Packet Loss Ratio</h3>
                <span className="text-[11px] text-slate-400">Unit: Percentage (%)</span>
              </div>
            </div>
            <div className="text-right font-mono text-xs">
              <span className={(telemetry?.gateway_packet_loss || 0) > 0 ? 'text-rose-400 font-bold' : 'text-emerald-400'}>
                {telemetry?.gateway_packet_loss ?? 0}% GW
              </span>
              <span className="text-slate-600 mx-1.5">|</span>
              <span className={(telemetry?.internet_packet_loss || 0) > 0 ? 'text-amber-400 font-bold' : 'text-blue-400'}>
                {telemetry?.internet_packet_loss ?? 0}% Inet
              </span>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} domain={[0, 100]} unit="%" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="gwLoss" name="Gateway Loss %" stroke="#F43F5E" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="inetLoss" name="Internet Loss %" stroke="#F59E0B" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Traffic Throughput */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <ArrowDownUp className="w-4 h-4 text-blue-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Network Traffic Bandwidth</h3>
                <span className="text-[11px] text-slate-400">Unit: Megabits per second (Mbps)</span>
              </div>
            </div>
            <div className="text-right font-mono text-xs">
              <span className="text-blue-400 font-bold">{telemetry?.download_mbps ?? 0} Mbps Down</span>
              <span className="text-slate-600 mx-1.5">|</span>
              <span className="text-emerald-400 font-bold">{telemetry?.upload_mbps ?? 0} Mbps Up</span>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="Mbps" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="downMbps" name="Download (Mbps)" stroke="#3B82F6" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="upMbps" name="Upload (Mbps)" stroke="#10B981" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
