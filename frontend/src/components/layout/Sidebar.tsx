import React from 'react';
import {
  Activity,
  Radio,
  BrainCircuit,
  History,
  Layers,
  Database,
  FlaskConical,
  Wifi
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isConnected: boolean;
  sessionId?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  isConnected,
  sessionId
}) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'live', label: 'Live Monitoring', icon: Radio },
    { id: 'prediction', label: 'AI Prediction', icon: BrainCircuit },
    { id: 'history', label: 'Network History', icon: History },
    { id: 'sessions', label: 'Network Sessions', icon: Layers },
    { id: 'dataset', label: 'Dataset & Model', icon: Database },
    { id: 'research', label: 'Research Evaluation', icon: FlaskConical },
  ];

  return (
    <aside className="w-64 bg-[#0E1320] border-r border-[#1F2937] flex flex-col h-screen fixed left-0 top-0 z-40 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-[#1F2937]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center glow-blue">
            <Wifi className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <div className="text-sm font-extrabold text-white tracking-wide flex items-center gap-1.5">
              <span>NETFAULT</span>
              <span className="text-xs bg-blue-600/30 text-blue-400 px-1.5 py-0.2 rounded font-mono font-bold">AI</span>
            </div>
            <p className="text-[10px] text-slate-400 font-mono tracking-tight uppercase">Predictive XAI Monitor</p>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-150 ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-md shadow-blue-900/10'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-500'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Status & Session Footer */}
      <div className="p-4 border-t border-[#1F2937] bg-[#0A0E17]/60">
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-slate-400 font-medium">Telemetry Stream</span>
          <div className="flex items-center gap-1.5">
            <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
            <span className={`text-[11px] font-mono font-semibold ${isConnected ? 'text-emerald-400' : 'text-rose-400'}`}>
              {isConnected ? 'LIVE' : 'DISCONNECTED'}
            </span>
          </div>
        </div>

        <div className="text-[11px] font-mono text-slate-400 truncate">
          Session: <span className="text-slate-300 font-semibold">{sessionId ? sessionId.replace('sess_', '') : 'Initializing...'}</span>
        </div>
      </div>
    </aside>
  );
};
