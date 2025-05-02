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
import InvitePage from './pages/InvitePage.vue';
import Investments from './pages/Investments.vue';
import Organisation_reg from './pages/Organisation_reg.vue';
import InvestmentPerformanceChart from './components/InvestmentPerformanceChart.vue';
import InvestmentDetails from './components/InvestmentDetails.vue';
import CandleStickGraph from './components/CandleStickGraph.vue';
import ShowAllInvestment from './components/ShowAllInvestment.vue';
import InvestmentsDisplay from './pages/InvestmentsDisplay.vue' 
import TrendChart from './components/TrendChart.vue';
import RecommendedSuppliers from './components/RecommendedSuppliers.vue';
import MessagingPage from './components/MessagingPage.vue';
import Prole from './components/Prole.vue';

const routes = [
  {path: '/',name: 'home',component: Home,},
  {path: '/login',name: 'login',component: Login,},
    {
      path: '/register/:token?', 
      name: 'register',
      component: Register,       
    },  
  { path: '/', redirect: '/inventory' },
  { path: '/stock-alerts', component: StockAlerts },
  { path: '/sales-entries', component: SalesEntries },
  { path: '/stock-history', component: StockFullHistory },
  { path: '/stock-full-history', component: StockHistory },
  { path: '/inventory', component: Inventory },
  { path: '/dashboard', name:'dashboard', component: Dashboard },
  { path: '/SalesStockChart', component: SalesStockChart },
  { path: '/SalesDistributionPie', component: SalesDistributionPie },
  { path: '/BaseLayout', component: BaseLayout },
  { path: '/InvitePage', component: InvitePage },
  { path: '/Investments', component: Investments },
  { path: '/Organisation_reg', component: Organisation_reg },
  { path: '/InvestmentPerformanceChart', component: InvestmentPerformanceChart },
  { path: '/InvestmentDetails', component: InvestmentDetails },
  { path: '/CandleStickGraph', component: CandleStickGraph },
  { path: '/ShowAllInvestments', component: ShowAllInvestment},
  { path: '/InvestmentsDisplay', component: InvestmentsDisplay},
  { path: '/TrendChart', component: TrendChart},
  { path: '/RecommendedSuppliers', component: RecommendedSuppliers},
  { path: '/MessagingPage', component: MessagingPage},
  { path: '/Prole', component: Prole}
]
  
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router