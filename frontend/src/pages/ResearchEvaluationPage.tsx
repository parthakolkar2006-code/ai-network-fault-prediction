import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ModelComparison, AblationItem } from '../types';
import { FlaskConical, Award, Table, Sparkles, Sliders } from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';

export const ResearchEvaluationPage: React.FC = () => {
  const [metrics, setMetrics] = useState<ModelComparison[]>([]);
  const [ablation, setAblation] = useState<AblationItem[]>([]);
  const [importance, setImportance] = useState<Array<{ feature: string; importance: number }>>([]);
  const [curves, setCurves] = useState<any>(null);
  const [selectedModel, setSelectedModel] = useState<string>('HistGradientBoosting');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([
      api.getResearchMetrics(),
      api.getAblationResults(),
      api.getFeatureImportance(),
      api.getResearchCurves()
    ])
      .then(([metricsData, ablationData, importanceData, curvesData]) => {
        setMetrics(metricsData || []);
        setAblation(ablationData || []);
        setImportance(importanceData || []);
        setCurves(curvesData || null);
        if (metricsData && metricsData.length > 0) {
          setSelectedModel(metricsData[0].model_name);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const currentModelStats = metrics.find((m) => m.model_name === selectedModel);
  const cm = currentModelStats?.confusion_matrix || { tp: 0, fp: 0, fn: 0, tn: 0 };

  const rocData = curves?.curves?.[selectedModel]?.roc_curve || [];
  const prData = curves?.curves?.[selectedModel]?.pr_curve || [];
  const threshCurve = curves?.thresholds?.[selectedModel]?.curve || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg flex items-center justify-between">
        <div className="flex items-center gap-3">
          <FlaskConical className="w-5 h-5 text-blue-400" />
          <div>
            <h2 className="text-sm font-bold text-white tracking-wide">
              Empirical Research Benchmark Evaluation (LCORE-D)
            </h2>
            <p className="text-xs text-slate-400">
              Evaluated across 5 ML architectures using strict chronological embargo splitting and validation threshold optimization
            </p>
          </div>
        </div>
        <span className="text-xs font-mono bg-emerald-950 text-emerald-400 border border-emerald-800 px-3 py-1 rounded-full font-bold">
          Non-Fabricated Real Results
        </span>
      </div>

      {/* Model Selection Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {metrics.map((m) => (
          <button
            key={m.model_name}
            onClick={() => setSelectedModel(m.model_name)}
            className={`px-4 py-2 rounded-xl text-xs font-bold tracking-wide transition-all ${
              selectedModel === m.model_name
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30 border border-blue-500'
                : 'bg-[#111827] text-slate-400 hover:text-slate-200 border border-[#1F2937]'
            }`}
          >
            {m.model_name}
          </button>
        ))}
      </div>

      {/* Selected Model Performance Cards */}
      {currentModelStats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 font-mono text-center">
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">PR-AUC</span>
            <span className="text-lg font-black text-blue-400">{currentModelStats.test_pr_auc}</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">ROC-AUC</span>
            <span className="text-lg font-black text-cyan-400">{currentModelStats.test_roc_auc}</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">Recall</span>
            <span className="text-lg font-black text-emerald-400">{(currentModelStats.test_recall * 100).toFixed(1)}%</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">Precision</span>
            <span className="text-lg font-black text-amber-400">{(currentModelStats.test_precision * 100).toFixed(1)}%</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">F1 Score</span>
            <span className="text-lg font-black text-purple-400">{currentModelStats.test_f1}</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">F2 Score</span>
            <span className="text-lg font-black text-rose-400">{currentModelStats.test_f2}</span>
          </div>
          <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-3">
            <span className="text-[10px] text-slate-400 block font-sans">Opt. Threshold</span>
            <span className="text-lg font-black text-white">{currentModelStats.optimal_threshold}</span>
          </div>
        </div>
      )}

      {/* Row: Confusion Matrix & ROC / PR Curves */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Confusion Matrix */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white tracking-wide">Test Confusion Matrix</h3>
            <span className="text-xs font-mono text-slate-400">{selectedModel}</span>
          </div>

          <div className="grid grid-cols-2 gap-3 font-mono text-center pt-2">
            <div className="bg-emerald-950/60 border border-emerald-800/80 rounded-xl p-4">
              <span className="text-[10px] text-emerald-400 block uppercase font-sans">True Positives (TP)</span>
              <span className="text-2xl font-black text-emerald-300">{cm.tp}</span>
              <span className="text-[10px] text-emerald-500 block mt-1">Faults Correctly Predicted</span>
            </div>
            <div className="bg-amber-950/60 border border-amber-800/80 rounded-xl p-4">
              <span className="text-[10px] text-amber-400 block uppercase font-sans">False Positives (FP)</span>
              <span className="text-2xl font-black text-amber-300">{cm.fp}</span>
              <span className="text-[10px] text-amber-500 block mt-1">False Alarms</span>
            </div>
            <div className="bg-rose-950/60 border border-rose-800/80 rounded-xl p-4">
              <span className="text-[10px] text-rose-400 block uppercase font-sans">False Negatives (FN)</span>
              <span className="text-2xl font-black text-rose-300">{cm.fn}</span>
              <span className="text-[10px] text-rose-500 block mt-1">Missed Faults</span>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-[10px] text-slate-400 block uppercase font-sans">True Negatives (TN)</span>
              <span className="text-2xl font-black text-slate-200">{cm.tn}</span>
              <span className="text-[10px] text-slate-500 block mt-1">Normal Period Maintained</span>
            </div>
          </div>
        </div>

        {/* Precision-Recall Curve */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <h3 className="text-sm font-bold text-white mb-2 tracking-wide">Precision-Recall Curve (PR)</h3>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={prData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="x" stroke="#4B5563" tick={{ fontSize: 10 }} label={{ value: 'Recall', position: 'insideBottom', offset: -5, fontSize: 10, fill: '#9CA3AF' }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} label={{ value: 'Precision', angle: -90, position: 'insideLeft', fontSize: 10, fill: '#9CA3AF' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="y" name="Precision" stroke="#3B82F6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* ROC Curve */}
        <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg">
          <h3 className="text-sm font-bold text-white mb-2 tracking-wide">ROC Curve (TPR vs FPR)</h3>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={rocData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                <XAxis dataKey="x" stroke="#4B5563" tick={{ fontSize: 10 }} label={{ value: 'FPR', position: 'insideBottom', offset: -5, fontSize: 10, fill: '#9CA3AF' }} />
                <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} label={{ value: 'TPR (Recall)', angle: -90, position: 'insideLeft', fontSize: 10, fill: '#9CA3AF' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="y" name="TPR" stroke="#10B981" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Model Comparison Table */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex items-center gap-2">
          <Table className="w-4 h-4 text-blue-400" />
          <h3 className="text-sm font-bold text-white tracking-wide">Cross-Architecture Benchmark Comparison Table</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0E1320] border-b border-[#1F2937] text-slate-400 font-sans uppercase">
              <tr>
                <th className="py-3 px-4">Architecture</th>
                <th className="py-3 px-4">Threshold</th>
                <th className="py-3 px-4">PR-AUC</th>
                <th className="py-3 px-4">ROC-AUC</th>
                <th className="py-3 px-4">Precision</th>
                <th className="py-3 px-4">Recall</th>
                <th className="py-3 px-4">F1 Score</th>
                <th className="py-3 px-4">F2 Score</th>
                <th className="py-3 px-4">FPR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1F2937] text-slate-300">
              {metrics.map((m) => (
                <tr key={m.model_name} className="hover:bg-slate-800/40">
                  <td className="py-3 px-4 font-bold text-white font-sans">{m.model_name}</td>
                  <td className="py-3 px-4">{m.optimal_threshold}</td>
                  <td className="py-3 px-4 text-blue-400 font-bold">{m.test_pr_auc}</td>
                  <td className="py-3 px-4 text-cyan-400">{m.test_roc_auc}</td>
                  <td className="py-3 px-4">{(m.test_precision * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4 text-emerald-400">{(m.test_recall * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4 font-bold text-purple-400">{m.test_f1}</td>
                  <td className="py-3 px-4">{m.test_f2}</td>
                  <td className="py-3 px-4 text-slate-400">{(m.test_fpr * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Feature Ablation Study Bar Chart */}
      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-5 shadow-lg space-y-4">
        <div>
          <h3 className="text-sm font-bold text-white tracking-wide">Feature Ablation Study (Telemetric Increments)</h3>
          <p className="text-xs text-slate-400">Comparing PR-AUC, F1, and F2 performance across isolated telemetry sub-domains</p>
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={ablation}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
              <XAxis dataKey="feature_group" stroke="#4B5563" tick={{ fontSize: 10 }} />
              <YAxis stroke="#4B5563" tick={{ fontSize: 10 }} domain={[0, 1]} />
              <Tooltip contentStyle={{ backgroundColor: '#0E1320', borderColor: '#374151', borderRadius: '8px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
              <Bar dataKey="pr_auc" name="PR-AUC" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="f1" name="F1 Score" fill="#10B981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="f2" name="F2 Score" fill="#F59E0B" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
