import React from 'react';

interface Props {
  title: string;
  value: string | number;
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
  );
}
