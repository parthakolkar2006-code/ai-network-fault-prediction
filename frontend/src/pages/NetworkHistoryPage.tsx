import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
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
import { History, Calendar, Activity, Gauge, Waves, ArrowDownUp } from 'lucide-react';

export const NetworkHistoryPage: React.FC = () => {
  const [timeframe, setTimeframe] = useState<string>('1h');
  const [historyData, setHistoryData] = useState<TelemetrySnapshot[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    setLoading(true);
    api.getTelemetryHistory(timeframe)
      .then((res) => {
        if (res && res.data) {
          setHistoryData(res.data);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [timeframe]);

  const ranges = [
    { id: '15m', label: '15 Minutes' },
    { id: '1h', label: '1 Hour' },
    { id: '6h', label: '6 Hours' },
    { id: '24h', label: '24 Hours' },
    { id: '7d', label: '7 Days' },
  ];

  const chartData = historyData.map((pt) => ({
    time: pt.timestamp ? pt.timestamp.replace(/^\d{4}-\d{2}-\d{2} /, '') : '',
    gwLat: pt.gateway_latency,
    inetLat: pt.internet_latency,
    gwLoss: pt.gateway_packet_loss,
    inetLoss: pt.internet_packet_loss,
    gwJitter: pt.gateway_jitter,
    inetJitter: pt.internet_jitter,
    signal: pt.signal_strength,
    downMbps: pt.download_mbps,
    upMbps: pt.upload_mbps
  }));

  return (
    <div className="space-y-6">
      {/* Header with Timeframe Selectors */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
        <div className="flex items-center gap-3">
          <History className="w-5 h-5 text-blue-400" />
          <div>
            <h2 className="text-sm font-bold text-white tracking-wide">Historical Telemetry Trends</h2>
            <p className="text-xs text-slate-400">Inspecting historical gateway, internet, and signal behavior</p>
          </div>
        </div>

        {/* Timeframe Buttons */}
        <div className="flex items-center gap-1.5 bg-[#0A0E17] border border-slate-800 p-1 rounded-lg">
          {ranges.map((r) => (
            <button
              key={r.id}
              onClick={() => setTimeframe(r.id)}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all ${
                timeframe === r.id
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="text-center py-6 text-xs text-slate-400 font-mono">
          Loading historical telemetry for timeframe {timeframe}...
        </div>
      )}

      {/* Latency History */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white tracking-wide">Path Latency Over Time</h3>
          </div>
          <span className="text-xs font-mono text-slate-400">{historyData.length} records</span>
        </div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
              <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
              <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="ms" />
              <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
              <Line type="monotone" dataKey="gwLat" name="Gateway Latency (ms)" stroke="#10B981" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line type="monotone" dataKey="inetLat" name="Internet Latency (ms)" stroke="#3B82F6" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Packet Loss & Jitter */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-rose-400" />
              <h3 className="text-sm font-bold text-white tracking-wide">Packet Loss History (%)</h3>
            </div>
          </div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} unit="%" domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="gwLoss" name="Gateway Loss %" stroke="#F43F5E" strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="inetLoss" name="Internet Loss %" stroke="#F59E0B" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Waves className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white tracking-wide">Jitter History (ms)</h3>
            </div>
          </div>
          <div className="h-56">
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
    </div>
  );
};
