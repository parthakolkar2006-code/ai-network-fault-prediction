import React, { useEffect, useState } from 'react';
import { PredictionResult, SimulationResult } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { api } from '../services/api';
import {
  BrainCircuit,
  Info,
  Layers,
  Sparkles,
  AlertTriangle,
  Activity,
  CheckCircle2,
  ShieldAlert
} from 'lucide-react';

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  LineChart,
  Line,
  CartesianGrid
} from 'recharts';

interface AIPredictionPageProps {
  prediction: PredictionResult | null;
}

export const AIPredictionPage: React.FC<AIPredictionPageProps> = ({
  prediction
}) => {
  const [history, setHistory] = useState<any[]>([]);
  const [simResult, setSimResult] = useState<SimulationResult | null>(null);
  const [simulating, setSimulating] = useState<boolean>(false);
  const [simError, setSimError] = useState<string | null>(null);

  useEffect(() => {
    api.getPredictionHistory().then((res) => {
      if (res && res.data) {
        setHistory(res.data);
      }
    }).catch(() => {});
  }, [prediction?.timestamp]);

  const runSimulation = async (preset: 'severe' | 'moderate' | 'healthy') => {
    setSimulating(true);
    setSimError(null);
    try {
      const data = await api.simulateBenchmark(preset);
      setSimResult(data);
    } catch (e: any) {
      console.error('Simulation failed:', e);
      setSimError(e.message || 'Simulation execution failed. Please verify that the backend is running and the research model is loaded.');
    } finally {
      setSimulating(false);
    }
  };


  const contributingFactors = prediction?.contributing_factors || [];

  const historyChartData = history.map((h, i) => ({
    time: h.timestamp ? h.timestamp.split(' ')[1] : `#${i}`,
    risk: h.risk_probability !== null && h.risk_probability !== undefined ? h.risk_probability * 100 : null,
    instability: h.network_instability_score || null
  }));

  return (
    <div className="space-y-6">
      {/* Hero Prediction Risk Card */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <BrainCircuit className="w-5 h-5 text-blue-400" />
              <span className="text-xs font-bold text-blue-400 uppercase tracking-widest">
                Real-Time Degradation Risk Forecast
              </span>
            </div>
            <h2 className="text-3xl font-extrabold text-white tracking-tight">
              30-Minute Network Risk
            </h2>
            <p className="text-xs text-slate-400 max-w-xl leading-relaxed">
              Predicts whether a sustained Wi-Fi or gateway degradation event will occur within the next 30 minutes, based on causal rolling features and instability heuristics.
            </p>
          </div>

          <div className="bg-[#0A0E17] border border-slate-800 rounded-2xl p-6 text-center min-w-[260px]">
            <span className="text-xs text-slate-400 block font-medium mb-1">Risk Probability</span>
            <div className="text-4xl font-black text-white font-mono my-2 tracking-tight">
              {prediction?.risk_probability !== null && prediction?.risk_probability !== undefined ? (
                `${(prediction.risk_probability * 100).toFixed(1)}%`
              ) : (
                <div className="text-lg font-bold text-cyan-400 py-1">
                  Baseline Mode
                </div>
              )}
            </div>
            <div className="mt-3">
              <StatusBadge
                state={prediction?.prediction_state || 'BASELINE_COLLECTION'}
                size="lg"
              />
            </div>
          </div>
        </div>

        {/* Cold Start Explanation Box */}
        {prediction?.status === 'COLLECTING_BASELINE' && (
          <div className="mt-6 bg-[#0E1524] border border-cyan-900/40 rounded-xl p-4 flex items-start gap-3">
            <Info className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
            <div className="space-y-1 text-xs">
              <div className="font-bold text-cyan-300">
                Deployment Model Cold-Start: Collecting Baseline Telemetry
              </div>
              <p className="text-slate-300 leading-relaxed">
                In adherence to scientific domain-shift principles, the emulated core ISP model (LCORE-D) is maintained as a benchmark and is not falsely represented as a validated consumer Wi-Fi model. The laptop is actively recording raw Wi-Fi metrics, dual-path pings, and rolling features to assemble a deployment dataset.
              </p>
            </div>
          </div>
        )}

        {/* Metadata Strip */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-slate-400">
          <div>
            Model Architecture: <span className="text-slate-200 font-semibold">{prediction?.model_version || 'v0.1-baseline'}</span>
          </div>
          <div>
            Decision Threshold: <span className="text-slate-200 font-semibold">{prediction?.threshold ?? 'N/A (Collecting)'}</span>
          </div>
          <div>
            Heuristic Health: <span className="text-emerald-400 font-semibold">{prediction?.network_health_indicator || 'STABLE'}</span>
          </div>
        </div>
      </div>

      {/* LCORE-D Research Benchmark Simulation */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <BrainCircuit className="w-5 h-5 text-blue-400" />
              <h3 className="text-base font-bold text-white tracking-wide">
                LCORE-D Research Benchmark Simulation
              </h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Empirical scenario evaluation using complete 79-feature telemetry vectors from the research dataset.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => runSimulation('healthy')}
              disabled={simulating}
              className="bg-emerald-950/80 hover:bg-emerald-900/90 text-emerald-300 border border-emerald-800 text-xs px-3 py-1.5 rounded-lg font-bold transition-all disabled:opacity-50 flex items-center gap-1.5"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              Simulate Healthy Network
            </button>
            <button
              onClick={() => runSimulation('moderate')}
              disabled={simulating}
              className="bg-amber-950/80 hover:bg-amber-900/90 text-amber-300 border border-amber-800 text-xs px-3 py-1.5 rounded-lg font-bold transition-all disabled:opacity-50 flex items-center gap-1.5"
            >
              <Activity className="w-3.5 h-3.5" />
              Simulate Moderate Degradation
            </button>
            <button
              onClick={() => runSimulation('severe')}
              disabled={simulating}
              className="bg-rose-950/80 hover:bg-rose-900/90 text-rose-300 border border-rose-800 text-xs px-3 py-1.5 rounded-lg font-bold transition-all disabled:opacity-50 flex items-center gap-1.5"
            >
              <ShieldAlert className="w-3.5 h-3.5" />
              Simulate Severe Fault
            </button>
          </div>
        </div>

        {/* Explanatory Banner */}
        <div className="bg-[#0E1524] border border-blue-900/30 rounded-xl p-3.5 flex items-start gap-3">
          <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <p className="text-xs text-slate-300 leading-relaxed">
            This simulator evaluates the trained LCORE-D research benchmark model against realistic network telemetry profiles derived from the research dataset. It does not alter your live laptop Wi-Fi monitoring.
          </p>
        </div>

        {/* Error Alert Display */}
        {simError && (
          <div className="bg-rose-950/60 border border-rose-800 rounded-xl p-4 flex items-start gap-3 text-xs text-rose-300">
            <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold text-rose-200">Simulation Error</div>
              <p className="mt-0.5 leading-relaxed">{simError}</p>
            </div>
          </div>
        )}

        {/* Simulation Output Card */}
        {simResult && (
          <div className="mt-4 bg-[#0A0E17] border border-blue-900/40 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Scenario Profile:</span>
                <span className="text-xs font-mono font-bold text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-800/80 px-2.5 py-0.5 rounded">
                  {simResult.scenario} Network
                </span>
                <span className="text-[10px] text-slate-500 font-mono">
                  (79 features evaluated)
                </span>
              </div>
              <StatusBadge state={simResult.prediction_state || 'NORMAL'} size="md" />
            </div>

            {/* Prediction Summary Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-[#111827]/70 p-3.5 rounded-lg border border-slate-800">
              <div>
                <span className="text-[10px] text-slate-400 block uppercase font-mono">Model Risk Score</span>
                <span className={`text-xl font-black font-mono ${
                  simResult.risk_probability >= (simResult.threshold || 0.38)
                    ? 'text-rose-400'
                    : simResult.risk_probability >= (simResult.threshold || 0.38) * 0.5
                    ? 'text-amber-400'
                    : 'text-emerald-400'
                }`}>
                  {(simResult.risk_probability * 100).toFixed(1)}%
                </span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block uppercase font-mono">Classification</span>
                <span className="text-sm font-bold text-white font-mono">{simResult.prediction_state}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block uppercase font-mono">Decision Threshold</span>
                <span className="text-sm font-bold text-slate-300 font-mono">{simResult.threshold}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block uppercase font-mono">Active Benchmark</span>
                <span className="text-sm font-bold text-slate-300 font-mono truncate block">{simResult.model_name}</span>
              </div>
            </div>

            {/* Key Simulated Telemetry Metrics */}
            {simResult.key_metrics_summary && (
              <div className="space-y-1.5">
                <span className="text-[10px] text-slate-400 font-mono block uppercase font-bold">
                  Simulated Network Telemetry:
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
                  <div className="bg-[#111827] border border-slate-800/80 rounded p-2.5">
                    <span className="text-[10px] text-slate-500 block font-sans">ICMP Packet Loss</span>
                    <span className="text-slate-200 font-bold">
                      {simResult.key_metrics_summary.icmp_loss_pct}%
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      Max: {simResult.key_metrics_summary.icmp_loss_max_pct}%
                    </span>
                  </div>
                  <div className="bg-[#111827] border border-slate-800/80 rounded p-2.5">
                    <span className="text-[10px] text-slate-500 block font-sans">ICMP Latency & Jitter</span>
                    <span className="text-slate-200 font-bold">
                      {simResult.key_metrics_summary.icmp_latency_ms} ms
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      Jitter: {simResult.key_metrics_summary.icmp_jitter_ms} ms
                    </span>
                  </div>
                  <div className="bg-[#111827] border border-slate-800/80 rounded p-2.5">
                    <span className="text-[10px] text-slate-500 block font-sans">Discards / Errors</span>
                    <span className="text-slate-200 font-bold">
                      {simResult.key_metrics_summary.interface_discards} discards
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {simResult.key_metrics_summary.interface_errors} errors
                    </span>
                  </div>
                  <div className="bg-[#111827] border border-slate-800/80 rounded p-2.5">
                    <span className="text-[10px] text-slate-500 block font-sans">SNMP & Throughput</span>
                    <span className="text-slate-200 font-bold">
                      {simResult.key_metrics_summary.snmp_availability_pct}% Avail
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {simResult.key_metrics_summary.total_throughput_mbps} Mbps
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* XAI Attribution Factors */}
            {simResult.contributing_factors && simResult.contributing_factors.length > 0 && (
              <div className="pt-2 border-t border-slate-800/80 space-y-2">
                <span className="text-[10px] text-slate-400 font-mono block uppercase font-bold">
                  Top Explainable AI (XAI) Attribution Factors:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {simResult.contributing_factors.map((f: any, i: number) => (
                    <div key={i} className="bg-[#111827] border border-slate-800 rounded p-2.5 flex items-center justify-between text-xs font-mono">
                      <div className="space-y-0.5 truncate max-w-[200px]">
                        <span className="text-slate-200 font-medium block truncate">{f.feature}</span>
                        <span className="text-[10px] text-slate-500 block">
                          Value: {typeof f.value === 'number' ? f.value.toFixed(2) : String(f.value)}
                        </span>
                      </div>
                      <div className="text-right shrink-0">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                          f.impact > 0
                            ? 'bg-rose-950/80 text-rose-400 border border-rose-800/60'
                            : 'bg-emerald-950/80 text-emerald-400 border border-emerald-800/60'
                        }`}>
                          {f.impact > 0 ? `+${f.impact}` : f.impact}
                        </span>
                        <span className="text-[9px] text-slate-500 block uppercase mt-0.5">
                          {f.direction || (f.impact > 0 ? 'INCREASES_RISK' : 'DECREASES_RISK')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>


      {/* Row 2: Explainable AI Contributing Factors & Historical Risk Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Contributing Factors */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Explainable AI (Top Contributing Factors)</h3>
                <p className="text-xs text-slate-400">Derived from feature attribution and instability weights</p>
              </div>
            </div>
          </div>

          {contributingFactors.length > 0 ? (
            <div className="space-y-3">
              {contributingFactors.map((factor, idx) => (
                <div key={idx} className="bg-[#0A0E17] border border-slate-800 rounded-lg p-3 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <span className="text-xs font-bold text-slate-200 block font-mono">{factor.feature}</span>
                    <span className="text-[11px] text-slate-400">Observed Value: <span className="text-slate-300 font-semibold">{factor.value}</span></span>
                  </div>
                  <div className="text-right">
                    <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                      factor.impact > 0
                        ? 'bg-rose-950/80 text-rose-400 border border-rose-800/80'
                        : factor.impact < 0
                        ? 'bg-emerald-950/80 text-emerald-400 border border-emerald-800/80'
                        : 'bg-cyan-950/80 text-cyan-400 border border-cyan-800/80'
                    }`}>
                      {factor.impact > 0 ? `+${factor.impact}` : `${factor.impact}`}
                    </span>
                    <span className="text-[10px] text-slate-500 block uppercase font-mono mt-0.5">
                      {factor.direction}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center text-xs text-slate-500 font-mono">
              No contributing factors logged yet.
            </div>
          )}
        </div>

        {/* Prediction Risk History Chart */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-blue-400" />
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide">Risk Assessment History</h3>
                <p className="text-xs text-slate-400">Timeline of degradation assessments</p>
              </div>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={historyChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10 }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} domain={[0, 100]} unit="%" />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="risk" name="Degradation Risk %" stroke="#3B82F6" strokeWidth={2} dot={false} connectNulls />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
