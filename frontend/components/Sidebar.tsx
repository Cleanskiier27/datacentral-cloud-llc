import React from 'react';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 hidden md:block">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-gray-900">Search Console</h1>
        <p className="text-xs text-gray-500 mt-1">AI Dashboard</p>
      </div>
    </aside>
  );
}
