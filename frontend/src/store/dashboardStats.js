// src/services/dashboardStats.js
import http from '../services/http';

const fetchDashboardStats = async () => {
  try {
    const data = await http.get('/api/dashboard-stats/');
    return data;
  } catch (error) {
    console.error("Error fetching dashboard stats:", error);
    throw error;
  }
};

export default fetchDashboardStats;
