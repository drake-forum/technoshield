// API Configuration
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Feature Flags
export const FEATURES = {
  ENABLE_NOTIFICATIONS: true,
  ENABLE_REAL_TIME_UPDATES: true,
  ENABLE_THREAT_INTELLIGENCE: false,
};

// Dashboard Configuration
export const DASHBOARD_CONFIG = {
  refreshInterval: 60000, // 1 minute
  alertsLimit: 5,
  incidentsLimit: 5,
};

// Theme Configuration
export const THEME = {
  PRIMARY_COLOR: '#3B82F6', // Blue
  SECONDARY_COLOR: '#10B981', // Green
  DANGER_COLOR: '#EF4444', // Red
  WARNING_COLOR: '#F59E0B', // Amber
  INFO_COLOR: '#6366F1', // Indigo
};