import React from 'react';
import { Link as LinkIcon, ExternalLink, ArrowRight } from 'lucide-react';

export default function Links() {
  return (
    <div className="max-w-6xl mx-auto p-6 md:p-8 space-y-8">
      <header>
        <h1 className="text-2xl font-normal text-gray-800 tracking-tight">Links</h1>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* External Links */}
        <div className="space-y-6">
          <h2 className="text-xl font-medium text-gray-800 flex items-center">
            <ExternalLink className="w-5 h-5 mr-2 text-gray-500" />
            External links
          </h2>
          
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
              <h3 className="font-medium text-gray-800">Top linked pages</h3>
              <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center">
                More <ArrowRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            <div className="p-6">
              <div className="text-3xl font-light text-gray-900 mb-4">8,492 <span className="text-sm text-gray-500 font-normal">total external links</span></div>
              <div className="space-y-3">
                {['/', '/blog', '/about', '/pricing', '/contact'].map((path, i) => (
                  <div key={i} className="flex justify-between items-center text-sm">
                    <span className="text-gray-600 truncate pr-4">{path}</span>
                    <span className="font-medium text-gray-900">{Math.floor(3000 / (i + 1))}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
              <h3 className="font-medium text-gray-800">Top linking sites</h3>
              <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center">
                More <ArrowRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            <div className="p-6 space-y-3">
              {['github.com', 'twitter.com', 'medium.com', 'reddit.com', 'dev.to'].map((site, i) => (
                <div key={i} className="flex justify-between items-center text-sm">
                  <span className="text-gray-600 truncate pr-4">{site}</span>
                  <span className="font-medium text-gray-900">{Math.floor(1500 / (i + 1))}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Internal Links */}
        <div className="space-y-6">
          <h2 className="text-xl font-medium text-gray-800 flex items-center">
            <LinkIcon className="w-5 h-5 mr-2 text-gray-500" />
            Internal links
          </h2>
          
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
              <h3 className="font-medium text-gray-800">Top linked pages</h3>
              <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center">
                More <ArrowRight className="w-4 h-4 ml-1" />
              </button>
            </div>
            <div className="p-6">
              <div className="text-3xl font-light text-gray-900 mb-4">24,105 <span className="text-sm text-gray-500 font-normal">total internal links</span></div>
              <div className="space-y-3">
                {['/', '/features', '/blog', '/docs', '/pricing'].map((path, i) => (
                  <div key={i} className="flex justify-between items-center text-sm">
                    <span className="text-gray-600 truncate pr-4">{path}</span>
                    <span className="font-medium text-gray-900">{Math.floor(8000 / (i + 1))}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
