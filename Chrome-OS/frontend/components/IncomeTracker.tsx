import React, { useState, useMemo, useEffect } from 'react';
import { DollarSign, TrendingUp, PiggyBank, Wallet } from 'lucide-react';

interface IncomeStream {
  name: string;
  amount: number;
  growth: number;
  color: string;
}

interface IncomeDataPoint {
  date: string;
  ads: number;
  subscriptions: number;
  affiliates: number;
  products: number;
}

export default function IncomeTracker() {
  const [incomeData, setIncomeData] = useState<IncomeDataPoint[]>([]);

  useEffect(() => {
    // Generate mock income data
    const data: IncomeDataPoint[] = [];
    let baseAds = 500;
    let baseSubs = 1200;
    let baseAff = 800;
    let baseProd = 2000;

    for (let i = 30; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);

      const variance = Math.random() * 0.2 - 0.1;
      const growth = 1.02;

      baseAds = Math.floor(baseAds * growth * (1 + variance));
      baseSubs = Math.floor(baseSubs * growth * (1 + variance));
      baseAff = Math.floor(baseAff * growth * (1 + variance));
      baseProd = Math.floor(baseProd * growth * (1 + variance));

      data.push({
        date: date.toISOString().split('T')[0],
        ads: baseAds,
        subscriptions: baseSubs,
        affiliates: baseAff,
        products: baseProd,
      });
    }
    setIncomeData(data);
  }, []);

  const totals = useMemo(() => {
    return incomeData.reduce(
      (acc, curr) => ({
        ads: acc.ads + curr.ads,
        subscriptions: acc.subscriptions + curr.subscriptions,
        affiliates: acc.affiliates + curr.affiliates,
        products: acc.products + curr.products,
      }),
      { ads: 0, subscriptions: 0, affiliates: 0, products: 0 }
    );
  }, [incomeData]);

  const totalRevenue = totals.ads + totals.subscriptions + totals.affiliates + totals.products;
  const avgDailyRevenue = incomeData.length > 0 ? totalRevenue / incomeData.length : 0;

  const streams: IncomeStream[] = [
    { name: 'Ad Revenue', amount: totals.ads, growth: 12.5, color: '#4285f4' },
    { name: 'Subscriptions', amount: totals.subscriptions, growth: 18.3, color: '#5e35b1' },
    { name: 'Affiliates', amount: totals.affiliates, growth: 9.7, color: '#0f9d58' },
    { name: 'Products', amount: totals.products, growth: 15.2, color: '#f59e0b' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-normal text-gray-800 tracking-tight">Income Megastructure</h2>
          <p className="text-sm text-gray-500 mt-1">Revenue streams and wealth accumulation</p>
        </div>
        <div className="flex items-center space-x-2 bg-gradient-to-r from-green-50 to-emerald-50 px-4 py-2 rounded-lg border border-green-200">
          <TrendingUp className="w-4 h-4 text-green-600" />
          <span className="text-sm font-medium text-green-700">+14.2% growth</span>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-5 rounded-xl border border-blue-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <DollarSign className="w-5 h-5 text-blue-600" />
            </div>
          </div>
          <div className="text-2xl font-semibold text-gray-900">
            ${totalRevenue.toLocaleString()}
          </div>
          <div className="text-xs text-gray-600 mt-1">Total Revenue (30d)</div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-5 rounded-xl border border-purple-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Wallet className="w-5 h-5 text-purple-600" />
            </div>
          </div>
          <div className="text-2xl font-semibold text-gray-900">
            ${avgDailyRevenue.toFixed(0)}
          </div>
          <div className="text-xs text-gray-600 mt-1">Avg Daily Revenue</div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-5 rounded-xl border border-green-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <PiggyBank className="w-5 h-5 text-green-600" />
            </div>
          </div>
          <div className="text-2xl font-semibold text-gray-900">
            ${streams.length}
          </div>
          <div className="text-xs text-gray-600 mt-1">Active Streams</div>
        </div>

        <div className="bg-gradient-to-br from-amber-50 to-orange-50 p-5 rounded-xl border border-amber-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2 bg-amber-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-amber-600" />
            </div>
          </div>
          <div className="text-2xl font-semibold text-gray-900">
            ${(totalRevenue * 0.35).toFixed(0)}
          </div>
          <div className="text-xs text-gray-600 mt-1">Est. Monthly Profit</div>
        </div>
      </div>

      {/* Income Streams */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-800">Revenue Streams</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {streams.map((stream, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: stream.color }} />
                  <div>
                    <div className="font-medium text-gray-900">{stream.name}</div>
                    <div className="text-sm text-gray-500">${stream.amount.toLocaleString()} total</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="text-sm font-medium text-green-600">+{stream.growth}%</div>
                  <div className="text-lg font-semibold text-gray-900">
                    ${(stream.amount / incomeData.length).toFixed(0)}/day
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Wealth Building Tips */}
      <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6 rounded-xl border border-indigo-100 shadow-sm">
        <h3 className="text-lg font-semibold text-indigo-900 mb-4">💎 Wealth Megastructure Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div className="flex items-start space-x-2">
            <span className="text-indigo-600 font-bold">•</span>
            <span>Diversify across {streams.length} income streams to reduce risk</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-purple-600 font-bold">•</span>
            <span>Reinvest {((totalRevenue * 0.2) / incomeData.length).toFixed(0)}$/day for compound growth</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-pink-600 font-bold">•</span>
            <span>Automate revenue collection and tracking systems</span>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-indigo-600 font-bold">•</span>
            <span>Scale top performer: Subscriptions (+18.3% growth)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
