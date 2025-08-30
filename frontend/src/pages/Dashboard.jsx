import React from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_URL, DASHBOARD_CONFIG } from '../config';

// Components
import AlertSummary from '../components/dashboard/AlertSummary';
import IncidentSummary from '../components/dashboard/IncidentSummary';
import MetricCard from '../components/dashboard/MetricCard';
import ThreatMap from '../components/dashboard/ThreatMap';

const fetchDashboardData = async () => {
  const response = await axios.get(`${API_URL}/api/v1/dashboard/summary`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  });
  return response.data;
};

const Dashboard = () => {
  const { data, isLoading, error } = useQuery(
    'dashboardData',
    fetchDashboardData,
    {
      refetchInterval: DASHBOARD_CONFIG.refreshInterval,
    }
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg
              className="h-5 w-5 text-red-400"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">
              Error loading dashboard data. Please try again later.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Metrics Overview */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Total Alerts"
          value={data?.total_alerts || 0}
          icon="bell"
          change={data?.alerts_change || 0}
          changeType={data?.alerts_change >= 0 ? 'increase' : 'decrease'}
        />
        <MetricCard
          title="Critical Alerts"
          value={data?.alerts_by_severity?.critical || 0}
          icon="exclamation"
          change={data?.critical_alerts_change || 0}
          changeType={data?.critical_alerts_change >= 0 ? 'increase' : 'decrease'}
          color="red"
        />
        <MetricCard
          title="Active Incidents"
          value={data?.incidents_by_status?.active || 0}
          icon="shield-exclamation"
          change={data?.active_incidents_change || 0}
          changeType={data?.active_incidents_change >= 0 ? 'increase' : 'decrease'}
          color="amber"
        />
        <MetricCard
          title="Total Users"
          value={data?.total_users || 0}
          icon="users"
          change={0}
          changeType="neutral"
          color="blue"
        />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {/* Recent Alerts */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Recent Alerts</h3>
            <Link
              to="/alerts"
              className="text-sm font-medium text-blue-600 hover:text-blue-500"
            >
              View all
            </Link>
          </div>
          <div className="border-t border-gray-200">
            <AlertSummary alerts={data?.recent_alerts || []} />
          </div>
        </div>

        {/* Active Incidents */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Active Incidents</h3>
            <Link
              to="/incidents"
              className="text-sm font-medium text-blue-600 hover:text-blue-500"
            >
              View all
            </Link>
          </div>
          <div className="border-t border-gray-200">
            <IncidentSummary incidents={data?.recent_incidents || []} />
          </div>
        </div>
      </div>

      {/* Threat Map */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Threat Map</h3>
        </div>
        <div className="border-t border-gray-200 p-4">
          <div className="h-96">
            <ThreatMap threatData={data?.threat_map_data || []} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;