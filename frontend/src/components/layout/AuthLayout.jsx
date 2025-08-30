import React from 'react';
import { Outlet } from 'react-router-dom';

const AuthLayout = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white">TECHNOSHIELD</h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Advanced Cybersecurity Monitoring Platform</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;