import React, { useState } from 'react';
import { DataPoint, Query } from '../types';

interface Props {
  data: DataPoint[];
  queries: Query[];
}

export default function AIInsights({ data, queries }: Props) {
  const [insights, setInsights] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async () => {
    setIsLoading(true);
    setInsights("Analysis feature coming soon. This will provide AI-powered insights about your search performance.");
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-blue-50 p-6 rounded-xl border border-indigo-100 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 bg-indigo-100 rounded-md">
            <span className="text-2xl">✨</span>
          </div>
          <h2 className="text-lg font-semibold text-indigo-900">AI Insights</h2>
        </div>
        {!insights && !isLoading && (
          <button
            onClick={handleAnalyze}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors shadow-sm"
          >
            Analyze Performance
          </button>
        )}
      </div>

      {isLoading && (
        <div className="flex items-center space-x-3 text-indigo-600 py-6 justify-center bg-white/40 rounded-lg border border-indigo-100/50">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
          <span className="text-sm font-medium">Analyzing search data...</span>
        </div>
      )}

      {insights && !isLoading && (
        <div className="bg-white/70 backdrop-blur-sm p-5 rounded-lg border border-indigo-100/50 shadow-sm">
          <p className="text-sm text-gray-800">{insights}</p>
        </div>
      )}
    </div>
  );
}
