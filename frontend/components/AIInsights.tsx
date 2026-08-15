import React, { useState } from 'react';
import { Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { getSEOInsights } from '../services/gemini';
import { DataPoint, Query } from '../types';

interface Props {
  data: DataPoint[];
  queries: Query[];
}

export default function AIInsights({ data, queries }: Props) {
  const [insights, setInsights] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Create a concise summary to save tokens and provide context
      const recentData = data.slice(-7);
      const summary = `
        Last 7 Days Trend:
        Total Clicks: ${recentData.reduce((sum, d) => sum + d.clicks, 0)}
        Total Impressions: ${recentData.reduce((sum, d) => sum + d.impressions, 0)}
        
        Top 5 Queries:
        ${queries.slice(0, 5).map(q => `- "${q.query}": ${q.clicks} clicks, pos ${q.position}`).join('\n')}
      `;
      
      const result = await getSEOInsights(summary);
      setInsights(result);
    } catch (err: any) {
      setError(err.message || 'Failed to generate insights. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatText = (text: string) => {
    return text.split('\n').map((line, i) => {
      if (line.trim().startsWith('-') || line.trim().startsWith('*')) {
        return <li key={i} className="ml-6 list-disc text-gray-800 mb-1.5">{line.replace(/^[-*]\s*/, '')}</li>;
      }
      if (line.trim() === '') return <div key={i} className="h-3" />;
      return <p key={i} className="text-gray-800 mb-2">{line}</p>;
    });
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-blue-50 p-6 rounded-xl border border-indigo-100 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 bg-indigo-100 rounded-md">
            <Sparkles className="w-5 h-5 text-indigo-600" />
          </div>
          <h2 className="text-lg font-semibold text-indigo-900">Gemini SEO Insights</h2>
        </div>
        {!insights && !isLoading && (
          <button
            onClick={handleAnalyze}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors shadow-sm flex items-center space-x-2"
          >
            <span>Analyze Performance</span>
          </button>
        )}
      </div>

      {isLoading && (
        <div className="flex items-center space-x-3 text-indigo-600 py-6 justify-center bg-white/40 rounded-lg border border-indigo-100/50">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span className="text-sm font-medium">Analyzing search data with Gemini...</span>
        </div>
      )}

      {error && (
        <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-4 rounded-lg border border-red-100">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm">{error}</span>
        </div>
      )}

      {insights && !isLoading && (
        <div className="bg-white/70 backdrop-blur-sm p-5 rounded-lg border border-indigo-100/50 shadow-sm">
          <div className="text-sm leading-relaxed">
            {formatText(insights)}
          </div>
          <div className="mt-5 pt-4 border-t border-indigo-100/60 flex justify-end">
             <button
              onClick={handleAnalyze}
              className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors flex items-center space-x-1"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Refresh Insights</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
