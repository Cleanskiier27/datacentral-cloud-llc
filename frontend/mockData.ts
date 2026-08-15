import { DataPoint, Query } from './types';

export const generateMockData = (): DataPoint[] => {
  const data: DataPoint[] = [];
  let baseClicks = 150;
  let baseImpressions = 2200;

  for (let i = 30; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);

    // Add some random variance and a slight upward trend
    const variance = Math.random() * 0.3 - 0.15;
    const trend = 1.01;

    baseClicks = Math.floor(baseClicks * trend * (1 + variance));
    baseImpressions = Math.floor(baseImpressions * trend * (1 + variance));

    // Simulate weekend dips
    const day = date.getDay();
    const isWeekend = day === 0 || day === 6;
    const multiplier = isWeekend ? 0.7 : 1;

    const clicks = Math.max(10, Math.floor(baseClicks * multiplier));
    const impressions = Math.max(100, Math.floor(baseImpressions * multiplier));
    const ctr = parseFloat(((clicks / impressions) * 100).toFixed(2));
    const conversions = Math.max(1, Math.round(clicks * (0.06 + Math.random() * 0.08)));
    
    // Position improves slightly as clicks increase
    const position = parseFloat((12 + Math.random() * 4 - (clicks / 100)).toFixed(1));

    data.push({
      date: date.toISOString().split('T')[0],
      clicks,
      impressions,
      ctr,
      position: Math.max(1, position),
      conversions,
    });
  }
  return data;
};

export const topQueries: Query[] = [
  { query: 'react dashboard template', clicks: 342, impressions: 2100, ctr: 16.2, position: 2.4, conversions: 28 },
  { query: 'tailwind css components', clicks: 215, impressions: 1850, ctr: 11.6, position: 4.1, conversions: 20 },
  { query: 'google search console api', clicks: 189, impressions: 3400, ctr: 5.5, position: 8.7, conversions: 17 },
  { query: 'seo analytics tool', clicks: 145, impressions: 980, ctr: 14.7, position: 3.5, conversions: 12 },
  { query: 'recharts line chart example', clicks: 112, impressions: 1200, ctr: 9.3, position: 5.2, conversions: 9 },
  { query: 'gemini ai integration', clicks: 98, impressions: 650, ctr: 15.0, position: 1.8, conversions: 8 },
  { query: 'frontend performance metrics', clicks: 76, impressions: 1100, ctr: 6.9, position: 11.3, conversions: 6 },
];
