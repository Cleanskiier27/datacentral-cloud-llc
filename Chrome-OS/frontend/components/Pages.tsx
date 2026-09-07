import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { AlertCircle, CheckCircle } from 'lucide-react';

export default function Pages() {
  const data = [
    { name: 'Indexed', value: 1245, color: '#0f9d58' },
    { name: 'Not indexed', value: 342, color: '#e5e7eb' }
  ];

  const reasons = [
    { reason: 'Page with redirect', count: 156, status: 'Not indexed' },
    { reason: 'Excluded by \'noindex\' tag', count: 89, status: 'Not indexed' },
    { reason: 'Not found (404)', count: 45, status: 'Not indexed' },
    { reason: 'Alternate page with proper canonical tag', count: 32, status: 'Not indexed' },
    { reason: 'Crawled - currently not indexed', count: 20, status: 'Not indexed' },
  ];

  return (
    <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
      <header>
        <h1 className="text-2xl font-normal text-gray-800 tracking-tight">Pages</h1>
        <p className="text-sm text-gray-500 mt-1">Page indexing report</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h2 className="text-lg font-medium text-gray-800 mb-6">Indexing Status</h2>
          <div className="h-[300px] w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-center space-y-6">
          <div className="flex items-start space-x-4">
            <div className="p-2 bg-green-50 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-3xl font-light text-gray-900">1,245</div>
              <div className="text-sm font-medium text-gray-500 mt-1">Indexed pages</div>
            </div>
          </div>
          <div className="w-full h-px bg-gray-100"></div>
          <div className="flex items-start space-x-4">
            <div className="p-2 bg-gray-100 rounded-lg">
              <AlertCircle className="w-6 h-6 text-gray-500" />
            </div>
            <div>
              <div className="text-3xl font-light text-gray-900">342</div>
              <div className="text-sm font-medium text-gray-500 mt-1">Not indexed pages</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-800">Why pages aren't indexed</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-gray-600">
            <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-medium">Reason</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Pages</th>
              </tr>
            </thead>
            <tbody>
              {reasons.map((r, idx) => (
                <tr key={idx} className="bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900">{r.reason}</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      {r.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right font-medium">{r.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
