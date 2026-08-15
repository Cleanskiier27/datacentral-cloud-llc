import React, { useState } from 'react';
import { Search, CheckCircle, Loader2 } from 'lucide-react';

export default function UrlInspection() {
  const [url, setUrl] = useState('');
  const [isInspecting, setIsInspecting] = useState(false);
  const [result, setResult] = useState<null | 'success'>(null);

  const handleInspect = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    setIsInspecting(true);
    setResult(null);
    setTimeout(() => {
      setIsInspecting(false);
      setResult('success');
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 md:p-8 space-y-8">
      <header>
        <h1 className="text-2xl font-normal text-gray-800 tracking-tight">URL Inspection</h1>
        <p className="text-sm text-gray-500 mt-1">Inspect a URL in the current property</p>
      </header>

      <form onSubmit={handleInspect} className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Inspect any URL in 'example.com'"
          className="block w-full pl-11 pr-4 py-4 bg-white border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-shadow"
          required
        />
        <button
          type="submit"
          disabled={isInspecting || !url}
          className="absolute inset-y-2 right-2 px-4 bg-gray-50 hover:bg-gray-100 text-gray-700 text-sm font-medium rounded-lg border border-gray-200 transition-colors disabled:opacity-50 flex items-center"
        >
          {isInspecting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Test URL'}
        </button>
      </form>

      {result === 'success' && (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="p-6 border-b border-gray-100 flex items-start space-x-4">
            <div className="mt-1">
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
            <div>
              <h2 className="text-xl font-medium text-gray-900">URL is on Google</h2>
              <p className="text-gray-600 mt-1">It can appear in Google Search results (if not subject to a manual action or removal request) with all relevant enhancements.</p>
            </div>
          </div>
          <div className="bg-gray-50 p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <div className="text-sm font-medium text-gray-500 uppercase tracking-wider">Coverage</div>
              <div className="flex items-center text-green-700 font-medium">
                <CheckCircle className="w-4 h-4 mr-2" /> Submitted and indexed
              </div>
            </div>
            <div className="space-y-2">
              <div className="text-sm font-medium text-gray-500 uppercase tracking-wider">Mobile Usability</div>
              <div className="flex items-center text-green-700 font-medium">
                <CheckCircle className="w-4 h-4 mr-2" /> Page is usable on mobile
              </div>
            </div>
            <div className="space-y-2">
              <div className="text-sm font-medium text-gray-500 uppercase tracking-wider">Enhancements</div>
              <div className="flex items-center text-green-700 font-medium">
                <CheckCircle className="w-4 h-4 mr-2" /> 1 valid item detected
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
