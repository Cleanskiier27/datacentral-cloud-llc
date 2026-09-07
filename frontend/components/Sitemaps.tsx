import React, { useState } from 'react';
import { FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export default function Sitemaps() {
  const [sitemapUrl, setSitemapUrl] = useState('');

  const sitemaps = [
    { url: '/sitemap.xml', type: 'Sitemap', submitted: 'Oct 24, 2023', lastRead: 'Oct 25, 2023', status: 'Success', discovered: 1245 },
    { url: '/blog-sitemap.xml', type: 'Sitemap', submitted: 'Oct 20, 2023', lastRead: 'Oct 25, 2023', status: 'Success', discovered: 342 },
    { url: '/products-sitemap.xml', type: 'Sitemap', submitted: 'Sep 15, 2023', lastRead: 'Oct 24, 2023', status: 'Has errors', discovered: 890 },
  ];

  return (
    <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
      <header>
        <h1 className="text-2xl font-normal text-gray-800 tracking-tight">Sitemaps</h1>
      </header>

      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h2 className="text-lg font-medium text-gray-800 mb-4">Add a new sitemap</h2>
        <div className="flex items-center space-x-4">
          <div className="flex-1 flex items-center border border-gray-300 rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-transparent transition-shadow">
            <span className="px-4 py-2.5 bg-gray-50 text-gray-500 border-r border-gray-300 text-sm">
              https://example.com/
            </span>
            <input
              type="text"
              value={sitemapUrl}
              onChange={(e) => setSitemapUrl(e.target.value)}
              placeholder="Enter sitemap URL"
              className="flex-1 px-4 py-2.5 outline-none text-sm text-gray-900"
            />
          </div>
          <button className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors">
            Submit
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-800">Submitted sitemaps</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-gray-600">
            <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-medium">Sitemap</th>
                <th className="px-6 py-4 font-medium">Type</th>
                <th className="px-6 py-4 font-medium">Submitted</th>
                <th className="px-6 py-4 font-medium">Last read</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Discovered pages</th>
              </tr>
            </thead>
            <tbody>
              {sitemaps.map((s, idx) => (
                <tr key={idx} className="bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-medium text-blue-600 hover:underline cursor-pointer flex items-center">
                    <FileText className="w-4 h-4 mr-2 text-gray-400" />
                    {s.url}
                  </td>
                  <td className="px-6 py-4">{s.type}</td>
                  <td className="px-6 py-4">{s.submitted}</td>
                  <td className="px-6 py-4">{s.lastRead}</td>
                  <td className="px-6 py-4">
                    {s.status === 'Success' ? (
                      <span className="flex items-center text-green-600 font-medium">
                        <CheckCircle className="w-4 h-4 mr-1.5" /> Success
                      </span>
                    ) : (
                      <span className="flex items-center text-amber-600 font-medium">
                        <AlertTriangle className="w-4 h-4 mr-1.5" /> {s.status}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right font-medium">{s.discovered.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
