import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
  color: string;
  isActive: boolean;
  onClick: () => void;
}

export default function MetricCard({ title, value, color, isActive, onClick }: MetricCardProps) {
  return (
    <div
      onClick={onClick}
      className={`p-6 rounded-xl border-2 cursor-pointer transition-all ${
        isActive
          ? 'bg-white border-blue-500 shadow-lg'
          : 'bg-white border-gray-200 opacity-60 hover:opacity-100'
      }`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-gray-500 font-medium uppercase tracking-wide mb-2">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div
          className="w-4 h-4 rounded-full"
          style={{ backgroundColor: color }}
        />
      </div>
    </div>
  );
}
