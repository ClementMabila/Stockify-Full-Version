<template>
  <BaseLayoutSec>
    <div class="sales-entries-container" style="height: 900px;">
      <div class="registration-form-section">

        <!-- Step 1: User Info -->
        <form 
          v-if="step === 1" 
          class="registration-form" 
          @submit.prevent="nextStepUser"
        >
          <h4 class="logo">Stockify</h4>
          <h4 class="welcome-text">User Info</h4>

          <!-- User Info Fields -->
          <div class="form-group">
            <input v-model="user.username" id="username" type="text" required placeholder=" " />
            <label for="username">Username</label>
          </div>
          <div class="form-group">
            <input v-model="user.first_name" id="first_name" type="text" required placeholder=" " />
            <label for="first_name">First Name</label>
          </div>
          <div class="form-group">
            <input v-model="user.last_name" id="last_name" type="text" required placeholder=" " />
            <label for="last_name">Last Name</label>
          </div>
          <div class="form-group">
            <input v-model="user.email" id="email" type="email" required placeholder=" " />
            <label for="email">Email</label>
          </div>
          <div class="form-group">
            <input v-model="user.password" id="password" type="password" required placeholder=" " />
            <label for="password">Password</label>
          </div>
          <div class="form-group">
            <input v-model="confirmPassword" id="confirm_password" type="password" required placeholder=" " />
            <label for="confirm_password">Confirm Password</label>
          </div>

          <button type="submit" class="submit-btn">Next</button>
          <p v-if="error" class="error-message">{{ error }}</p>
        </form>

        <!-- Step 2: Organization Info -->
        <form 
          v-if="step === 2" 
          class="registration-form" 
          @submit.prevent="register"
        >
          <h4 class="welcome-text">Organization Info</h4>

          <!-- Organization Info Fields -->
          <div class="form-group">
            <input v-model="organization.name" id="org_name" type="text" required placeholder=" " />
            <label for="org_name">Organization Name</label>
          </div>
          <div class="form-group">
            <input v-model="organization.description" id="org_desc" type="text" required placeholder=" " />
            <label for="org_desc">Description</label>
          </div>
          <div class="form-group">
            <input v-model="organization.address" id="org_address" type="text" required placeholder=" " />
            <label for="org_address">Address</label>
          </div>
          <div class="form-group">
            <input v-model="organization.phone_number" id="org_phone" type="text" placeholder=" " />
            <label for="org_phone">Phone Number</label>
          </div>
          <div class="form-group">
            <input v-model="organization.email" id="org_email" type="email" required placeholder=" " />
            <label for="org_email">Organization Email</label>
          </div>
          <div class="form-group">
            <input v-model="organization.date_established" id="org_date" type="date" required placeholder=" " />
            <label for="org_date">Date Established</label>
          </div>

          <button type="submit" class="submit-btn">Register & Continue</button>
          <p v-if="error" class="error-message">{{ error }}</p>
        </form>

        <!-- Step 3: OTP Form -->
        <form 
          v-if="step === 3" 
          class="registration-form otp-form" 
          @submit.prevent="verifyOTP"
        >
          <h3 class="welcome-text">Enter OTP</h3>
          <div class="otp-container">
            <p class="otp-info">
              We’ve sent a one-time password (OTP) to your email. Please enter the 6-digit code below.
            </p>
            <p class="otp-resend">
              Didn’t receive the code? <span class="timer">Request a new one in 30 seconds.</span>
            </p>
          </div>
          <div class="form-group">
            <input v-model="otp" type="text" required placeholder=" " />
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
import axios from "axios";
import { useAuthStore, getCSRFToken } from '../store/auth';

export default {
  components: {
    BaseLayoutSec,
  },
  data() {
    return {
      user: {
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
      },
      confirmPassword: '',
      organization: {
        name: '',
        description: '',
        address: '',
        phone_number: '',
        email: '',
        date_established: '',
      },
      otp: '',
      step: 1,
      showOTP: false,
      error: '',
      success: ''
    };
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    async register() {
      try {
        await this.authStore.setCsrfToken();

        const response = await fetch('http://localhost:8000/api/register-and-create-organization/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify({
            username: this.user.username,
            password: this.user.password,
            email: this.user.email,
            first_name: this.user.first_name,
            last_name: this.user.last_name,
            organization_name: this.organization.name,
            organization_description: this.organization.description,
            organization_address: this.organization.address,
            organization_phone_number: this.organization.phone_number,
            organization_email: this.organization.email,
            organization_date_established: this.organization.date_established,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          this.success = "Registered! Check your email for the OTP.";
          this.step = 3;
        } else {
          this.error = data.error || "Registration failed.";
        }
      } catch (error) {
        this.error = "Error: " + error;
      }
    },

    async verifyOTP() {
      try {
        await this.authStore.setCsrfToken();

        const response = await axios.post(
          "http://localhost:8000/api/verify-otp/",
          {
            otp: this.otp,
            email: this.user.email,
          },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': getCSRFToken(),
              'Content-Type': 'application/json'
            }
          }
        );

        if (response.status === 200 && response.data.token) {
          localStorage.setItem("authToken", response.data.token);
          localStorage.setItem("userEmail", this.user.email);

          await this.authStore.fetchUser();
          this.success = "OTP verified successfully!";
          this.$router.push("/dashboard");
        } else {
          this.error = response.data.error || "Invalid OTP.";
        }
      } catch (err) {
        this.error = "Error verifying OTP: " + err.message;
      }
    },

    async logout() {
      try {
        await this.authStore.logout(this.$router);
      } catch (err) {
        console.error('Logout failed', err);
      }
    },

    async loginUser() {
      try {
        await this.authStore.login(this.user.email, this.user.password, this.$router);
      } catch (err) {
        this.error = 'Login failed: ' + err.message;
      }
    },

    nextStepUser() {
      this.error = '';
      if (
        !this.user.username || !this.user.first_name || !this.user.last_name ||
        !this.user.email || !this.user.password || !this.confirmPassword
      ) {
        this.error = "Please fill in all fields.";
        return;
      }
      if (this.user.password !== this.confirmPassword) {
        this.error = "Passwords do not match.";
        return;
      }
      this.step = 2;
    }
  }
};
</script>

<style scoped>
.registration-form-section {
  margin-top: 100px;
  background-color: #F8F9FA;
  width: 350px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  border-radius: 12px;
}

.form-group {
  position: relative;
  margin-bottom: 20px;
}

.form-group input {
  width: 100%;
  padding: 12px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: transparent;
  outline: none;
}

.form-group label {
  position: absolute;
  left: 10px;
  top: 12px;
  transition: 0.3s ease;
  color: #777;
  font-size: 14px;
  background-color: #F8F9FA;
  padding: 0 4px;
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  top: -8px;
  font-size: 12px;
  color: #7c73e6;
}

.submit-btn {
  background-color: #7c73e6;
  color: #fff;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.otp-form {
  margin-top: 40px;
  height: 300px;
}

.error-message {
  color: red;
  font-size: 13px;
  margin-top: 10px;
}
</style>

<style src="../assets/css/dashboard.css"></style>