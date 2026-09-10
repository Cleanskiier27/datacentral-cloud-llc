import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import PerformanceView from './components/PerformanceView';
import IncomeTracker from './components/IncomeTracker';
import UrlInspection from './components/UrlInspection';
import Pages from './components/Pages';
import Sitemaps from './components/Sitemaps';
import Links from './components/Links';
import Settings from './components/Settings';

export default function App() {
  const [activeTab, setActiveTab] = useState('performance');

  const renderContent = () => {
    switch (activeTab) {
      case 'performance': return <PerformanceView />;
      case 'income': return (
        <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
          <IncomeTracker />
        </div>
      );
      case 'inspection': return <UrlInspection />;
      case 'pages': return <Pages />;
      case 'sitemaps': return <Sitemaps />;
      case 'links': return <Links />;
      case 'settings': return <Settings />;
      default: return <PerformanceView />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900 overflow-hidden">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 overflow-y-auto">
        {renderContent()}
      </main>
    </div>
  );
}
