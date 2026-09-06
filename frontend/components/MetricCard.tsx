import React from 'react';

interface Props {
  title: string;
  value: string | number;
interface MetricCardProps {
  title: string;
  value: string;
  color: string;
  isActive: boolean;
  onClick: () => void;
}

export default function MetricCard({ title, value, color, isActive, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-start p-4 rounded-lg transition-all duration-200 w-full text-left outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
        ${isActive ? 'bg-white shadow-sm' : 'bg-gray-50 hover:bg-gray-100'}
      `}
      style={{
        borderTop: isActive ? `4px solid ${color}` : '1px solid #e5e7eb',
        borderRight: isActive ? `1px solid ${color}40` : '1px solid #e5e7eb',
        borderBottom: isActive ? `1px solid ${color}40` : '1px solid #e5e7eb',
        borderLeft: isActive ? `1px solid ${color}40` : '1px solid #e5e7eb',
      }}
    >
      <span className="text-sm font-medium text-gray-600 mb-1">{title}</span>
      <span className="text-3xl font-normal tracking-tight" style={{ color: isActive ? color : '#374151' }}>
        {value}
      </span>
    </button>
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
