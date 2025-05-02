<template>
  <BaseLayoutSec>
    <div class="sales-entries-container" style="height: 900px;">
      <div class="registration-form-section">
  <form 
    v-if="!showOTP" 
    class="registration-form" style="height: 510px;"
    @submit.prevent="register"
    :class="{'slide-out': showOTP}"
  >
  <h4 class="logo">
      Stockify 
      <span><img src="../assets/images/animated.png" alt="Google Icon" class="icon" /></span>
  </h4>
    <h4 class="welcome-text" style="font-size: 18px; margin-bottom: -5px; color: black;">Sign In</h4>
    <p class="Inv-exp">Sign in to manage your inventory</p>

    <div class="form-group">
      <input 
        v-model="username" 
        id="username" 
        type="text" 
        required 
        placeholder=" "
      />
      <label for="username">Username</label>
    </div>

    <div class="form-group">
      <input 
        v-model="email" 
        id="email" 
        type="email" 
        required 
        readonly 
        placeholder=" "
      />
      <label for="email">Email</label>
    </div>

    <div class="form-group">
      <input 
        v-model="password" 
        id="password" 
        type="password" 
        required 
        placeholder=" "
      />
      <label for="password">Password</label>
    </div>

    <div class="form-group">
      <input 
        v-model="confirm_password" 
        id="confirm_password" 
        type="password" 
        required 
        placeholder=" "
      />
      <label for="confirm_password">Confirm Password</label>
    </div>

        <button type="submit" class="submit-btn">Sign Up</button>

    <div class="or-separator">
      <span>or</span>
    </div>

    <a href="/google-auth" class="google-btn" style="text-decoration: none; background-color: transparent; font-size: 13px; border: none; padding: 10px; border-radius: 10px;">
      <span><img src="../assets/images/google.png" alt="Google Icon" class="icon" /></span> Connect with Google
    </a>

    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-if="success" class="success-message">{{ success }}</p>

    <p class="signin-link">
      Already have an account? <a href="/login" style="color: #7c73e6;"><strong class="in-strn">Sign In</strong></a>
    </p>
  </form>

  <form 
      v-if="showOTP" 
      class="registration-form otp-form"
      @submit.prevent="verifyOTP"
    >
      <h3 class="welcome-text" style="font-size: 18px; color: black;">Enter OTP</h3>
      <div class="otp-container">
        <p class="otp-info">
          We’ve sent a one-time password (OTP) to your registered phone number/email.
          Please enter the 6-digit code below to verify your identity.
        </p>
        <p class="otp-resend">
          Didn’t receive the code? <span class="timer">You can request a new one in 30 seconds.</span>
        </p>
      </div>
      <div class="form-group">
        <input 
          v-model="otp" 
          type="text" 
          required
          placeholder=" "
        />
        <label for="otp">OTP</label>
      </div>
      <button type="submit" class="submit-btn">Verify OTP</button>
      </form>
    </div>
    </div>
  </BaseLayoutSec>
</template>


<script>
import BaseLayoutSec from "../components/BaseLayoutSec.vue";
import { useAuthStore, getCSRFToken } from '../store/auth';

export default {
  components: {
    BaseLayoutSec,
  },
  data() {
    return {
      email: '', 
      password: '',
      confirm_password: '',
      otp: '',
      showOTP: false,
      error: '',
      success: '' 
    };
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  mounted() {
    const token = this.$route.params.token;
    this.fetchEmailFromToken(token);
  },
  methods: {
    getCSRFToken() {
      const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
      return csrfToken ? csrfToken[1] : '';
    },
    async fetchEmailFromToken(token) {
      try {
        const response = await fetch(`http://localhost:8000/api/get-email-from-token/${token}/`);
        const data = await response.json();
        if (response.ok) {
          this.email = data.email; 
        } else {
          this.error = "Failed to fetch email. Please check the invitation token.";
        }
      } catch (err) {
        this.error = "";
      }
    },
    async register() {
      if (this.password !== this.confirm_password) {
        this.error = "Passwords do not match!";
        return;
      }
      try {
        const token = this.$route.params.token;
        
        const response = await fetch(`http://localhost:8000/api/register/${token}/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            confirm_password: this.confirm_password
          })
        });

        const data = await response.json();
        if (response.ok) {
          this.showOTP = true;
          this.success = "User registered, check email for OTP!";
        } else {
          this.error = data.error || "Registration failed";
        }
      } catch (err) {
        this.error = "Error during registration: " + err;
      }
    },

    async verifyOTP() {
    try {
      await this.authStore.setCsrfToken();
      
      console.log("Sending OTP verification request with:", this.email, this.otp);

      const response = await fetch("http://localhost:8000/api/verify-otp/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify({
          otp: this.otp,
          email: this.email,
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("Request failed:", response.status, errorData);
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("OTP Verification Response:", data);
      
      if (data.success) {
      localStorage.setItem("userEmail", this.email);
      await this.authStore.fetchUser();
      this.success = "OTP verified successfully!";
      this.$router.push("/dashboard");
    } else {
      this.error = data.error || "Invalid OTP.";
    }
    } catch (err) {
      this.error = "Error verifying OTP: " + err.message;
      console.error("Full error:", err);
      console.error("Error stack:", err.stack); // Add stack trace
    }
  },

    resetError() {
      this.error = '';
    },
  }
}
</script>

<style scoped>
.registration-form-section {
  margin-top: 100px;
  background-color: #F8F9FA;
  width: 200px;
}

.signin-link a {
  text-decoration: none; 
  color: #7c73e6;
}

.signin-link a:hover {
  text-decoration: none;
}

#app{
  background: url('../assets/images/screen-2.jpg') no-repeat center center;
  background-size: cover;
  position: relative;
}

.logo {
  margin-left: 121px;
  color: #444;
  font-size: 17px;
}

.otp-form {
  width: 100%;
  max-width: 400px;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  position: absolute;
  transition: transform 0.5s ease;
  align-items: center;
  height: 320px;
  margin-top: 10px;
}

.slide-out {
  transform: translateX(-100%);
}

.otp-heading {
  text-align: center;
  margin-bottom: 20px;
}

.in-strn {
  color: #444;
  text-decoration: none;
  font-size: 14px;
}

.error-message {
  color: red;
  font-size: 11px;
  text-align: center;
  margin-top: 10px;
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