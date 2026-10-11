import React, { useState } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { OverviewPage } from './pages/OverviewPage';
import { LiveMonitoringPage } from './pages/LiveMonitoringPage';
import { AIPredictionPage } from './pages/AIPredictionPage';
import { NetworkHistoryPage } from './pages/NetworkHistoryPage';
import { NetworkSessionsPage } from './pages/NetworkSessionsPage';
import { DatasetModelPage } from './pages/DatasetModelPage';
import { ResearchEvaluationPage } from './pages/ResearchEvaluationPage';
import { useLiveTelemetry } from './hooks/useLiveTelemetry';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const { telemetry, prediction, alerts, historyPoints, isConnected } = useLiveTelemetry(50);

  const getPageTitle = (tab: string) => {
    switch (tab) {
      case 'overview':
        return 'Network Operations Center (NOC) Overview';
      case 'live':
        return 'Live High-Frequency Telemetry Stream';
      case 'prediction':
        return 'Explainable AI Predictive Degradation Engine';
      case 'history':
        return 'Historical Telemetry Analytics & Metrics';
      case 'sessions':
        return 'Dynamic Wi-Fi Network & Gateway Sessions';
      case 'dataset':
        return 'LCORE-D v2 Dataset Transparency & Leakage Audit';
      case 'research':
        return 'Empirical Machine Learning Research Benchmark';
      default:
        return 'Network Operations Center';
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex">
      {/* Fixed Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isConnected={isConnected}
        sessionId={telemetry?.session_id}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title={getPageTitle(activeTab)}
          telemetry={telemetry}
          prediction={prediction}
          alertCount={alerts.length}
        />

        <main className="ml-64 p-6 overflow-y-auto">
          {activeTab === 'overview' && (
            <OverviewPage
              telemetry={telemetry}
              prediction={prediction}
              historyPoints={historyPoints}
            />
          )}

          {activeTab === 'live' && (
            <LiveMonitoringPage
              telemetry={telemetry}
              historyPoints={historyPoints}
              isConnected={isConnected}
            />
          )}

          {activeTab === 'prediction' && (
            <AIPredictionPage prediction={prediction} />
          )}

          {activeTab === 'history' && (
            <NetworkHistoryPage />
          )}

          {activeTab === 'sessions' && (
            <NetworkSessionsPage />
          )}

          {activeTab === 'dataset' && (
            <DatasetModelPage />
          )}

          {activeTab === 'research' && (
            <ResearchEvaluationPage />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
