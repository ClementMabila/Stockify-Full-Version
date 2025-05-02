import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue';
import Login from './pages/Login.vue';
import StockAlerts from './pages/StockAlerts.vue';
import SalesEntries from './pages/SalesEntries.vue';
import StockHistory from './pages/StockHistory.vue';
import StockFullHistory from './pages/StockFullHistory.vue';
import Inventory from './pages/Inventory.vue';
import Register from './pages/Register.vue';
import Dashboard from './pages/Dashboard.vue';
import SalesStockChart from './components/SalesStockChart.vue';
import SalesDistributionPie from './components/SalesDistributionPie.vue';
import BaseLayout from './components/BaseLayout.vue';
import Investments from '../pages/Investments.vue';
import InvestmentDetails from '../pages/InvestmentDetails.vue';
import RecommendedSuppliers from '../components/RecommendedSuppliers.vue';


const routes = [
  { path: '/',name: 'home',component: Dashboard,},
  { path: '/login',name: 'login',component: Login,},
  { path: '/register',name: 'register',component: Register,},
  { path: '/', redirect: '/inventory' },
  { path: '/stock-alerts', component: StockAlerts },
  { path: '/sales-entries', component: SalesEntries },
  { path: '/stock-history', component: StockFullHistory },
  { path: '/stock-full-history', component: StockHistory },
  { path: '/inventory', component: Inventory },
  { path: '/dashboard', name: 'dashboard' ,component: Dashboard },
  { path: '/SalesStockChart', component: SalesStockChart },
  { path: '/SalesDistributionPie', component: SalesDistributionPie },
  { path: '/BaseLayout', component: BaseLayout },
  { path: '/Organization_reg', component: Organisation_reg },
  { path: '/Investments', component: Investments },
  { path: '/InvestmentDetails', component: InvestmentDetails },
  { path: '/RecommendedSuppliers', component: RecommendedSuppliers}]
  
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router