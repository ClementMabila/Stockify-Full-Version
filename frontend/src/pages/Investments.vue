<template>
  <div class="main-container">
    <div id="dashboard" class="d-flex vh-100">
  <div class="sidebar">
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link to="/Investments" class="nav-link"><span><img src="../assets/images/animated.png" alt="Google Icon" class="icon-side" /></span>Investment</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/InvestmentsDisplay" class="nav-link"><span><img src="../assets/images/stocks-icons2.png" alt="Google Icon" class="icon-side" /></span>Org Stats</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/stock-history" class="nav-link-free">Messanger</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/inventory" class="nav-link-free">Inventory</router-link>
      </li>
    </ul>
  </div>

  <section class="main-content flex-grow-1 p-4 bg-light">
    <div class="heading">
        <h4 class="logo" style="font-family: Batang, Arial, sans-serif; font-weight: 600; font-size: 16px; color: black; margin-bottom: 25px;">Stockify</h4>
        <div class="header-icons">
                <div class="search-field">
                    <img src="../assets/images/search.png" alt="Search" class="search-icon">
                    <input type="text" placeholder="Search for anything here" />
                </div>

                <div class="dropdown notification-dropdown"
                    @mouseenter="showDropdown = true"
                    @mouseleave="showDropdown = false">
                    
                    <a href="#" id="notification-icon" class="notification-icon-wrapper">
                        <img src="../assets/images/notification.png" alt="Notification" class="app-main-icons">
                        <span v-if="unseenCount > 0" class="notif-dot">{{ unseenCount > 9 ? '9+' : unseenCount }}</span>
                    </a>

                    <div v-if="showDropdown" class="dropdown-content">
                        <div class="notification-header">
                            <h5>Notifications</h5>
                            <small v-if="unseenCount > 0" class="mark-read" @click="markNotificationsSeen">Mark all as read</small>
                        </div>
                        <div class="notification-list">
                            <p v-if="notifications.length === 0" class="empty-notifications">No new notifications</p>
                            <ul v-else>
                                <li v-for="notification in notifications" :key="notification.id">
                                    <div class="notification-content">
                                        <strong>Requested {{ notification.quantity }} of {{ notification.product }}</strong>
                                        <p>{{ notification.status }} • {{ notification.date }}</p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

          <div class="dropdown">
              <a href="#" id="settings-icon">
                  <img src="../assets/images/settings.png" alt="Settings" class="app-main-icons">
              </a>
              <div class="dropdown-content-a settings-dropdown">
                    <a href="#">Account Settings</a>
                    <a href="#">Preferences</a>
                    <a href="#" @click.prevent="logout">Log Out</a>
                </div>
          </div>

                <a href="/profile/">
                    <img src="../assets/images/profile_pic.png" alt="Profile" class="app-main-icons profile-pic">
                </a>
            </div>
        </div>

    
    <div class="row d-flex justify-content-between" style="margin-right: 50px;">
    <div class="col-md-4 top-banner">
      <div class="banner banner-sales d-flex align-items-start" style="background-color: #d59bf6;">
        <div class="content">
          <h4 class="heading-dashboard" style="color: white;">Dashboard</h4>
          <div class="details">
            <section class="full-labels-section">
              <div class="full-label">
                <div class="icon-box">
                  <img src="../assets/images/acc-i1.png" alt="Sales Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;">Account Name</div>
                  <div class="text-name" style="color: white;">Mosh Mashabane</div>
                </div>
              </div>

              <div class="full-label ms-3">
                <div class="icon-box">
                  <img src="../assets/images/acc-i2.png" alt="Sales Chart Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;">Organisation</div>
                  <div class="text-name" style="color: white;">Nissan Cars</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4 top-banner glass-ef">
      <div class="banner banner-sales d-flex align-items-start glass-ef-sec" style="background-color: #a1f480;">
        <div class="content">
          <h4 style="color: white;">Inventory Overview</h4>
          <div class="details">
            <section class="full-labels-section">
              <div class="full-label">
                <div class="icon-box">
               </div>
               <div class="text-box" style="margin-top: -3px;">
                <div class="label" style="color: white;">Investment Stats</div>
                <div class="number trend-indicator">
                <template v-if="trendSignal.direction === 'up'">
                  <img src="../assets/images/inc-signal.png" alt="Up" class="trend-icon" />
                  <span class="trend-label" style="color: #4caf50;">+{{ trendSignal.percentage }}%</span>
                </template>
                <template v-else-if="trendSignal.direction === 'down'">
                  <img src="../assets/images/decr.png" alt="Down" class="trend-icon" />
                  <span class="trend-label" style="color: #f44336;">-{{ trendSignal.percentage }}%</span>
                </template>
                <template v-else>
                  <span>Loading...</span>
                </template>
              </div>
              </div>
              </div>

              <div class="full-label ms-3" style="margin-left: 16px;">
                <div class="icon-box">
                </div>
                <div class="text-box" style="margin-top: -3px;">
                  <div class="label" style="margin-left: 25px; color: white;">Account Balance</div>
                  <div class="number" style="margin-left: 25px; color: white; margin-top: 10px; font-weight: bold;">$16,200</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4 top-banner " >
      <div class="banner banner-sales-dark d-flex align-items-start">
        <div class="content">
          <h4 style="color: white;">Inventory Insights</h4>
          <div class="details">
            <section class="full-labels-section" style="margin-right: 10px;">
              <div class="full-label">
                <div class="icon-box">
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;"> Total Expenses</div>
                  <div class="number" style="color: white;">100</div>
                </div>
              </div>

              <div class="full-label ms-3">
                <div class="icon-box">
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;">Active Stock</div>
                  <div class="number" style="color: white;">200</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="graphs-section-display">
  <div class="graph-display" style="height: 110px;">
    <div class="Investment-performance-chart">
    <h4 style="margin-right: 370px; margin-top: 10px; font-weight: lighter; color: #4444;">Evaluation</h4>
    <div class="asset-banner">
    <div class="asset-label">Stocks Invested: <span>{{ totalAssets ?? '147' }}</span></div>
  </div>
    <section>
      <InvestmentPerformanceChart @trendSignal="handleTrendSignal" />
  </section>
  </div>
  </div>
  <div class="graph-display secon-dis" style="margin-left: -170px;">
      <section style="margin-top:-240px;">
      <InvestmentDetails/>
    </section>
  </div>
  </div>

  <div class="graphs-section-display">
    <div class="graph-display">
      <section >
      <ssss/>
    </section>
    </div>
    <div class="graph-display secon-dis">
      <section style="margin-top: -250px;">
      <TrendChart/>
    </section>
  </div>
</div>

  </section>
  </div>
</div>
    <router-view></router-view>
</template>

<script setup>
import { ref } from 'vue'
import InvestmentPerformanceChart from '../components/InvestmentPerformanceChart.vue'
import InvestmentDetails from '../components/InvestmentDetails.vue'
import TrendChart from '../components/TrendChart.vue'

const trendSignal = ref({ direction: null, percentage: 0 })

function handleTrendSignal(signal) {
  trendSignal.value = signal
  }

</script>

<style src="../assets/css/dashboard.css"></style>
<style scoped>


.trend-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  color: white;
  animation: fadeIn 0.5s ease-in-out;
}

.trend-icon {
  width: 15px;
  height: 15px;
}

.arrow {
  font-size: 24px;
  font-weight: bold;
  animation: bounce 1.2s infinite;
}

.arrow.up {
  color: #4caf50;
  text-shadow: 0 0 6px #4caf50aa;
}

.arrow.down {
  color: #f44336;
  text-shadow: 0 0 6px #f44336aa;
}

.trend-label {
  margin-top: 1.5px;
  color: #444;
  font-size: 11px;
  opacity: 0.9;
  font-weight: lighter;
}

/* Animations */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.total-assest {
  color: #4444;
  font-size: 11.5px;
  margin-right: 330px;
}

.Investment-performance-chart {
  background-color: white;
  border-radius: 10px;
  width: 600px;
  height: 300px;
  margin-top: 10px;
}

.asset-banner {
  background-color: #d59bf6;
  border-radius: 1.5rem;
  padding: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  max-width: 140px;
  margin: auto;
  margin-right: 68%;
}

.asset-label {
  font-size: 9px;
  color: white;
  font-weight: lighter;
  text-transform: uppercase;
  margin-bottom: 1px;
}

.trend-indicator {
  background-color: white;
  margin-top: 10px;
  padding: 1px;
}

#app{
    background-color: #F8F9FA;
    font-family: Arial, Helvetica, sans-serif;
    display: flex;
    padding-left: 110px;
    overflow: hidden;
}

.main-content {
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px; /* for avoiding layout shift due to scrollbar */
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

/* Chrome, Edge, Safari */
.main-content::-webkit-scrollbar {
  width: 6px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.main-content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.main-content:hover::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.3);
}


</style>
