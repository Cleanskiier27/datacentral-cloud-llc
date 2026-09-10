import React, { useState, useMemo, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MetricCard from './components/MetricCard';
import PerformanceChart from './components/PerformanceChart';
import QueriesTable from './components/QueriesTable';
import AIInsights from './components/AIInsights';
import IncomeTracker from './components/IncomeTracker';
import Sitemaps from './components/Sitemaps';
import Links from './components/Links';
import Settings from './components/Settings';
import Pages from './components/Pages';
import { generateMockData, topQueries } from './mockData';
import { ActiveMetrics, DataPoint } from './types';

export default function App() {
  const [activeView, setActiveView] = useState('performance');
  const [activeMetrics, setActiveMetrics] = useState<ActiveMetrics>({
    clicks: true,
    impressions: true,
    ctr: false,
    position: false,
    conversions: true,
  });
  const [data, setData] = useState<DataPoint[]>(() => generateMockData());

  useEffect(() => {
    let isMounted = true;

    fetch('/api/dashboard-metrics')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch dashboard metrics');
        }
        return response.json();
      })
      .then((payload) => {
        if (isMounted && payload?.data?.length) {
          setData(payload.data);
        }
      })
      .catch(() => {
        if (isMounted) {
          setData(generateMockData());
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  // Calculate totals for the metric cards
  const totals = useMemo(() => {
    return data.reduce((acc, curr) => ({
      clicks: acc.clicks + curr.clicks,
      impressions: acc.impressions + curr.impressions,
      ctr: acc.ctr + curr.ctr, 
      position: acc.position + curr.position,
      conversions: acc.conversions + curr.conversions,
    }), { clicks: 0, impressions: 0, ctr: 0, position: 0, conversions: 0 });
  }, [data]);

  const avgCtr = ((totals.clicks / totals.impressions) * 100).toFixed(1);
  const avgPosition = (totals.position / data.length).toFixed(1);
  const conversionRate = ((totals.conversions / totals.clicks) * 100).toFixed(1);

  const toggleMetric = (metric: keyof ActiveMetrics) => {
    setActiveMetrics(prev => ({ ...prev, [metric]: !prev[metric] }));
  };

  const renderView = () => {
    switch (activeView) {
      case 'income':
        return (
          <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
            <IncomeTracker />
          </div>
        );
      
      case 'pages':
        return <Pages />;
      
      case 'sitemaps':
        return <Sitemaps />;
      
      case 'links':
        return <Links />;
      
      case 'settings':
        return <Settings />;
      
      default:
        // Performance view
        return (
      <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
        <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-normal text-gray-800 tracking-tight">Search Performance</h1>
            <p className="text-sm text-gray-500 mt-1">example.com</p>
          </div>
          <div className="text-sm text-gray-600 bg-white px-4 py-2 rounded-md border border-gray-200 shadow-sm inline-flex items-center">
            <span className="font-medium mr-2">Date:</span> Last 30 Days
          </div>
        </header>

        {/* Metrics Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-4">
          <MetricCard
            title="Total clicks"
            value={totals.clicks.toLocaleString()}
            color="#4285f4"
            isActive={activeMetrics.clicks}
            onClick={() => toggleMetric('clicks')}
          />
          <MetricCard
            title="Total impressions"
            value={totals.impressions.toLocaleString()}
            color="#5e35b1"
            isActive={activeMetrics.impressions}
            onClick={() => toggleMetric('impressions')}
          />
          <MetricCard
            title="Average CTR"
            value={`${avgCtr}%`}
            color="#0f9d58"
            isActive={activeMetrics.ctr}
            onClick={() => toggleMetric('ctr')}
          />
          <MetricCard
            title="Average position"
            value={avgPosition}
            color="#e67c73"
            isActive={activeMetrics.position}
            onClick={() => toggleMetric('position')}
          />
          <MetricCard
            title="Total conversions"
            value={totals.conversions.toLocaleString()}
            color="#f59e0b"
            isActive={activeMetrics.conversions}
            onClick={() => toggleMetric('conversions')}
          />
        </div>

        {/* Chart Section */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <PerformanceChart data={data} activeMetrics={activeMetrics} />
        </div>

        {/* AI Insights Section */}
        <AIInsights data={data} queries={topQueries} />

        {/* Queries Table Section */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-200 bg-white">
            <h2 className="text-lg font-medium text-gray-800">Top Queries</h2>
          </div>
          <QueriesTable queries={topQueries} />
        </div>
        
        <footer className="text-center text-sm text-gray-400 py-4">
          Conversion rate: {conversionRate}% across the last 30 days
        </footer>
      </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900 overflow-hidden">
      <Sidebar activeView={activeView} onViewChange={setActiveView} />
      
      <main className="flex-1 overflow-y-auto">
        {renderView()}
      </main>
    </div>
  );
}
