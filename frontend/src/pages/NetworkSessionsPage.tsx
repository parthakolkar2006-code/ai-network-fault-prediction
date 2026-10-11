import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { NetworkSession } from '../types';
import { Layers, Router, Clock, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const NetworkSessionsPage: React.FC = () => {
  const [sessions, setSessions] = useState<NetworkSession[]>([]);
  const [selectedSession, setSelectedSession] = useState<NetworkSession | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    api.getNetworkSessions()
      .then((data) => {
        setSessions(data || []);
        if (data && data.length > 0) {
          setSelectedSession(data[0]);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const formatDuration = (seconds?: number | null) => {
    if (!seconds && seconds !== 0) return 'Ongoing';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    if (m === 0) return `${s}s`;
    return `${m}m ${s}s`;
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Layers className="w-5 h-5 text-blue-400" />
          <div>
            <h2 className="text-sm font-bold text-white tracking-wide">Monitored Wi-Fi & Gateway Sessions</h2>
            <p className="text-xs text-slate-400">
              Automatic session creation across Wi-Fi network handovers (Home, College, Mobile Hotspot, Access Points)
            </p>
          </div>
        </div>
        <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded">
          {sessions.length} total sessions
        </span>
      </div>

      {/* Selected Session Inspector Panel */}
      {selectedSession && (
        <div className="bg-[#141C2E] border border-blue-900/40 rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-blue-400 uppercase tracking-widest">Selected Session Inspector</span>
              <span className="font-mono text-xs text-slate-300 font-bold">{selectedSession.session_id}</span>
            </div>
            {selectedSession.is_active && (
              <span className="inline-flex items-center gap-1.5 bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs px-2.5 py-0.5 rounded-full font-bold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                ACTIVE SESSION
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 font-mono text-xs">
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">SSID Hash</span>
              <span className="text-slate-200 font-bold">{selectedSession.ssid_hash || 'N/A'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">Gateway IP</span>
              <span className="text-emerald-300 font-bold">{selectedSession.gateway_ip || 'N/A'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">Interface</span>
              <span className="text-slate-200 font-bold">{selectedSession.interface_name || 'Wi-Fi'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">Avg Latency</span>
              <span className="text-white font-bold">{selectedSession.avg_gateway_latency ? `${selectedSession.avg_gateway_latency} ms` : 'N/A'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">Avg Loss</span>
              <span className="text-white font-bold">{selectedSession.avg_gateway_loss !== null ? `${selectedSession.avg_gateway_loss}%` : 'N/A'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-sans">Duration</span>
              <span className="text-cyan-300 font-bold">{formatDuration(selectedSession.duration_seconds)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Sessions Table */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl overflow-hidden shadow-lg">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#0E1320] border-b border-[#1F2937] text-slate-400 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Session ID</th>
                <th className="py-3 px-4">Network (SSID Hash)</th>
                <th className="py-3 px-4">Gateway IP</th>
                <th className="py-3 px-4">Start Time</th>
                <th className="py-3 px-4">Duration</th>
                <th className="py-3 px-4">Avg Latency</th>
                <th className="py-3 px-4">Avg Loss</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Inspect</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1F2937] font-mono text-slate-300">
              {sessions.map((sess) => {
                const isSelected = selectedSession?.session_id === sess.session_id;
                return (
                  <tr
                    key={sess.session_id}
                    onClick={() => setSelectedSession(sess)}
                    className={`cursor-pointer transition-colors ${
                      isSelected ? 'bg-blue-950/30' : 'hover:bg-slate-800/40'
                    }`}
                  >
                    <td className="py-3 px-4 font-bold text-white">{sess.session_id.slice(0, 16)}...</td>
                    <td className="py-3 px-4">{sess.ssid_hash}</td>
                    <td className="py-3 px-4 text-emerald-400">{sess.gateway_ip}</td>
                    <td className="py-3 px-4 text-slate-400">{sess.start_time}</td>
                    <td className="py-3 px-4">{formatDuration(sess.duration_seconds)}</td>
                    <td className="py-3 px-4">{sess.avg_gateway_latency ? `${sess.avg_gateway_latency} ms` : 'N/A'}</td>
                    <td className="py-3 px-4">{sess.avg_gateway_loss !== null ? `${sess.avg_gateway_loss}%` : 'N/A'}</td>
                    <td className="py-3 px-4">
                      {sess.is_active ? (
                        <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] px-2 py-0.5 rounded font-bold">
                          ACTIVE
                        </span>
                      ) : (
                        <span className="text-slate-500 text-[10px]">CLOSED</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button className="text-blue-400 hover:text-blue-300 font-sans text-xs flex items-center gap-1 ml-auto">
                        <span>Details</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
