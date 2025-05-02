<template>
  <BaseLayoutSec>
    <div class="sales-entries-container" style="height: 900px;">
      <div class="registration-form-section">
        <form class="registration-form" style="height: 450px;" @submit.prevent="step === 'login' ? login() : verifyOtp()">
          <h4 class="logo">
            Stockify 
            <span><img src="../assets/images/animated.png" alt="Google Icon" class="icon" /></span>
          </h4>
          <h4 class="welcome-text" style="font-size: 18px; margin-bottom: -5px; color: black;">
            {{ step === 'login' ? 'Sign In' : 'Verify OTP' }}
          </h4>
          <p class="Inv-exp">
            {{ step === 'login' ? 'Sign in to manage your inventory' : 'Enter the OTP sent to your email' }}
          </p>

          <!-- Login Step -->
          <div v-if="step === 'login'">
            <div class="form-group">
              <input 
                v-model="email" 
                id="email" 
                type="text" 
                required 
                placeholder=" "
                @input="resetError"
              />
              <label for="email">Username</label>
            </div>

            <div class="form-group">
              <input 
                v-model="password" 
                id="password" 
                type="password" 
                required 
                placeholder=" "
                @input="resetError"
              />
              <label for="password">Password</label>
            </div>
          </div>

          <!-- OTP Step -->
          <div v-else-if="step === 'otp'" class="form-group">
            <input
              v-model="otp"
              id="otp"
              type="text"
              required
              placeholder="Enter OTP"
              @input="resetError"
            />
            <label for="otp">One-Time Password</label>
          </div>

          <button type="submit" class="submit-btn">
            {{ step === 'login' ? 'Continue' : 'Verify OTP' }}
          </button>

          <p v-if="error" class="error-message">{{ error }}</p>

          <div v-if="step === 'login'" class="or-separator">
            <span>or</span>
          </div>

          <a v-if="step === 'login'" href="" @click.prevent="loginWithGoogle" class="google-btn" style="text-decoration: none; background-color: transparent; font-size: 13px; border: none; padding: 10px; border-radius: 10px;">
            <span><img src="../assets/images/google.png" alt="Google Icon" class="icon" /></span> Continue with Google
          </a>

          <div v-if="step === 'login'" class="separator"></div>

          <p v-if="step === 'login'" class="signin-link">
            Don’t have an account? <a href="/register" style="color: #444;"><strong class="in-strn">Sign Up</strong></a>
          </p>
        </form>
      </div>
    </div>
  </BaseLayoutSec>
</template>

<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth'; // adjust path as needed
import BaseLayoutSec from "../components/BaseLayoutSec.vue";

export default {
  components: {
    BaseLayoutSec,
  },
  data() {
    return {
      email: '',
      password: '',
      error: '',
      otp: '',
      step: 'login',
      serverEmail: '',
    };
  },
  setup() {
    const router = useRouter();
    const auth = useAuthStore();
    return { router, auth };
  },
  methods: {
  async login() {
    this.resetError();
    try {
      await this.auth.setCsrfToken();
      const response = await this.auth.login(this.email, this.password);

      console.log("Login Response:", response);

      // Django sends 'message' when successful
      if (response.message && response.email) {
        this.step = 'otp'; // Show OTP input
        this.serverEmail = response.email;
      } else {
        // Otherwise, show the error from the backend
        this.error = response.error || "Login failed.";
      }
    } catch (err) {
      this.error = "Login failed: " + err.message;
    }
  },

  async verifyOtp() {
      this.resetError();
      try {
        await this.auth.setCsrfToken();
        const result = await this.auth.verifyOtp(this.otp, this.serverEmail);
        if (result.success) {
          // Store the token in localStorage
          localStorage.setItem("auth_token", result.token);
          
          this.router.push('/dashboard');
        } else {
          this.error = result.error || "OTP verification failed.";
        }
      } catch (err) {
        this.error = "Network error.";
      }
    },

    resetError() {
      this.error = '';
    },

    async loginWithGoogle() {
      const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
      const query = {
        client_id: '650542285771-9id4memc5l4t65dt30kn76betrajfmvs.apps.googleusercontent.com',
        redirect_uri: 'http://localhost:5173/dashboard',
        response_type: 'code',
        scope: 'openid email profile',
        state: this.generateState(),
      };

      const queryString = new URLSearchParams(query).toString();
      window.location.href = `${googleAuthUrl}?${queryString}`;
    },

    generateState() {
      return Math.random().toString(36).substring(2, 15) +
             Math.random().toString(36).substring(2, 15);
    },
  }
};
</script>



<style scoped>
.registration-form-section {
  margin-top: 100px;
  background-color: #F8F9FA;
  width: 200px;
}

.signin-link a {
  text-decoration: none; 
  color: #444;
}

.signin-link a:hover {
  text-decoration: none;
}

#app {
  background: url('../assets/images/screen-2.jpg') no-repeat center center;
  background-size: cover;
  position: relative;
}

.logo {
  margin-left: 121px;
  color: #444;
  font-size: 17px;
}

.error-message {
  color: red;
  font-size: 11px;
  text-align: center;
  margin-top: 10px;
}

.submit-btn {
   font-size: 13px;
}

.success-message {
  color: green;
  font-size: 11px;
  margin-top: 10px;
  text-align: center;
}

.logo {
  font-size: 18px;
  margin-bottom: 10px;
  display: inline-flex; 
  align-items: center;
  gap: 5px; 
}

.logo .icon {
  width: 20px;
  height: 20px; 
  vertical-align: middle;
}
</style>
<style src="../assets/css/dashboard.css"></style>

