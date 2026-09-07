export interface DataPoint {
  date: string;
  clicks: number;
  impressions: number;
  ctr: number;
  position: number;
  conversions: number;
}

export interface Query {
  query: string;
  clicks: number;
  impressions: number;
  ctr: number;
  position: number;
  conversions: number;
}

export interface ActiveMetrics {
  clicks: boolean;
  impressions: boolean;
  ctr: boolean;
  position: boolean;
  conversions: boolean;
}

export interface DashboardSummary {
  totalClicks: number;
  totalImpressions: number;
  totalConversions: number;
  avgCtr: number;
  avgPosition: number;
  conversionRate: number;
}
