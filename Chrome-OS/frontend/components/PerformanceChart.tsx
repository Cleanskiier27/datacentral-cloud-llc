import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { DataPoint, ActiveMetrics } from '../types';

interface Props {
  data: DataPoint[];
  activeMetrics: ActiveMetrics;
}

export default function PerformanceChart({ data, activeMetrics }: Props) {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 shadow-lg rounded-lg text-sm min-w-[150px]">
          <p className="font-medium text-gray-800 mb-3 pb-2 border-b border-gray-100">{formatDate(label)}</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center justify-between mb-1.5">
              <div className="flex items-center space-x-2">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
                <span className="text-gray-600 capitalize">{entry.name}</span>
              </div>
              <span className="font-medium text-gray-900 ml-4">
                {entry.name === 'ctr' ? `${entry.value}%` : entry.value}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-[380px] w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickLine={false}
            axisLine={{ stroke: '#e5e7eb' }}
            minTickGap={30}
            dy={10}
          />
          <YAxis
            yAxisId="left"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickLine={false}
            axisLine={false}
            tickFormatter={(val) => val >= 1000 ? `${(val / 1000).toFixed(1)}k` : val}
            dx={-10}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickLine={false}
            axisLine={false}
            reversed={activeMetrics.position && !activeMetrics.ctr}
            dx={10}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#e5e7eb', strokeWidth: 2 }} />

          {activeMetrics.clicks && (
            <Line yAxisId="left" type="monotone" dataKey="clicks" name="Clicks" stroke="#4285f4" strokeWidth={2.5} dot={false} activeDot={{ r: 6, strokeWidth: 0 }} />
          )}
          {activeMetrics.impressions && (
            <Line yAxisId="left" type="monotone" dataKey="impressions" name="Impressions" stroke="#5e35b1" strokeWidth={2.5} dot={false} activeDot={{ r: 6, strokeWidth: 0 }} />
          )}
          {activeMetrics.ctr && (
            <Line yAxisId="right" type="monotone" dataKey="ctr" name="CTR" stroke="#0f9d58" strokeWidth={2.5} dot={false} activeDot={{ r: 6, strokeWidth: 0 }} />
          )}
          {activeMetrics.position && (
            <Line yAxisId="right" type="monotone" dataKey="position" name="Position" stroke="#e67c73" strokeWidth={2.5} dot={false} activeDot={{ r: 6, strokeWidth: 0 }} />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
