export function buildDashboardMetrics() {
  const data = [];
  let baseClicks = 150;
  let baseImpressions = 2200;

  for (let i = 30; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);

    const variance = Math.random() * 0.3 - 0.15;
    const trend = 1.01;

    baseClicks = Math.floor(baseClicks * trend * (1 + variance));
    baseImpressions = Math.floor(baseImpressions * trend * (1 + variance));

    const day = date.getDay();
    const isWeekend = day === 0 || day === 6;
    const multiplier = isWeekend ? 0.7 : 1;

    const clicks = Math.max(10, Math.floor(baseClicks * multiplier));
    const impressions = Math.max(100, Math.floor(baseImpressions * multiplier));
    const ctr = Number(((clicks / impressions) * 100).toFixed(2));
    const position = Number((12 + Math.random() * 4 - (clicks / 100)).toFixed(1));
    const conversions = Math.max(1, Math.round(clicks * (0.06 + Math.random() * 0.08)));

    data.push({
      date: date.toISOString().split('T')[0],
      clicks,
      impressions,
      ctr,
      position: Math.max(1, position),
      conversions,
    });
  }

  const totals = data.reduce(
    (acc, curr) => ({
      clicks: acc.clicks + curr.clicks,
      impressions: acc.impressions + curr.impressions,
      ctr: acc.ctr + curr.ctr,
      position: acc.position + curr.position,
      conversions: acc.conversions + curr.conversions,
    }),
    { clicks: 0, impressions: 0, ctr: 0, position: 0, conversions: 0 }
  );

  const avgCtr = totals.clicks > 0 ? (totals.clicks / totals.impressions) * 100 : 0;
  const avgPosition = data.length > 0 ? totals.position / data.length : 0;
  const conversionRate = totals.clicks > 0 ? (totals.conversions / totals.clicks) * 100 : 0;

  return {
    data,
    summary: {
      totalClicks: totals.clicks,
      totalImpressions: totals.impressions,
      totalConversions: totals.conversions,
      avgCtr: Number(avgCtr.toFixed(1)),
      avgPosition: Number(avgPosition.toFixed(1)),
      conversionRate: Number(conversionRate.toFixed(1)),
    },
  };
}
