import React from 'react';
import { Query } from '../types';

interface Props {
  queries: Query[];
}

export default function QueriesTable({ queries }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left text-gray-600">
        <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-6 py-4 font-medium">Top Queries</th>
            <th className="px-6 py-4 font-medium text-right">Clicks</th>
            <th className="px-6 py-4 font-medium text-right">Impressions</th>
            <th className="px-6 py-4 font-medium text-right">CTR</th>
            <th className="px-6 py-4 font-medium text-right">Position</th>
          </tr>
        </thead>
        <tbody>
          {queries.map((q, idx) => (
            <tr key={idx} className="bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 font-medium text-gray-900">{q.query}</td>
              <td className="px-6 py-4 text-right">{q.clicks.toLocaleString()}</td>
              <td className="px-6 py-4 text-right">{q.impressions.toLocaleString()}</td>
              <td className="px-6 py-4 text-right">{q.ctr}%</td>
              <td className="px-6 py-4 text-right">{q.position}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
