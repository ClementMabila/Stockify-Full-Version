<template>
  <BaseLayoutSec>
    <div class="registration-container">
      <!-- Progress Bar -->
      <div class="progress-container">
        <div class="progress-bar">
          <div class="progress" :style="{ width: progressWidth + '%' }"></div>
        </div>
        <div class="steps-indicator">
          <div class="step" :class="{ active: step >= 1, completed: step > 1 }">
            <div class="step-number">1</div>
            <span class="step-text">Account</span>
          </div>
          <div class="step" :class="{ active: step >= 2, completed: step > 2 }">
            <div class="step-number">2</div>
            <span class="step-text">Organisation</span>
          </div>
          <div class="step" :class="{ active: step >= 3 }">
            <div class="step-number">3</div>
            <span class="step-text">Verifications</span>
          </div>
        </div>
      </div>

      <!-- Registration Cards -->
      <div class="card-container">
        <!-- Step 1: User Info -->
        <transition name="fade" mode="out-in">
          <form 
            v-if="step === 1" 
            class="registration-card" 
            @submit.prevent="nextStepUser"
          >

          <h1>Lets get you registared as the Organisation Administrator</h1>
          <div class="banners-container">
          <!-- Banner 1 -->
          <div class="banner" style="border: 1px solid #6366f1;">
            <p class="banner-text"><span style="font-weight: bold; color: #6366f1;"><span><img src="../assets/images/info-33.png" alt="Info" class="info-icon"/></span>Why Join Stockify? </span>Stay ahead of the curve with real-time stock insights and smart alerts. Make smarter investment decisions effortlessly.</p>
          </div>

          <!-- Banner 2 -->
          <div class="banner" style="background: linear-gradient(90deg, #6366f1, #a855f7);">
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Your Data is Safe </span>We use bank-level security to keep your personal and investment data private and protected.</p>
          </div>

          <!-- Banner 3 -->
          <div class="banner" style="background-color: #d59bf6;">
            <h3 class="banner-title"></h3>
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Fast & Easy Setup </span>Create your account in under a minute. No paperwork, no hassle – just seamless onboarding.</p>
          </div>
        </div>


            <div class="form-grid">
              <div class="form-group">
                <label for="username">Username</label>
                <input 
                  v-model="user.username" 
                  id="username" 
                  type="text" 
                  required 
                  autocomplete="username"
                  :class="{ 'input-error': fieldErrors.username }"
                />
                <span v-if="fieldErrors.username" class="error-text">{{ fieldErrors.username }}</span>
              </div>
              
              <div class="form-group">
                <label for="first_name">First Name</label>
                <input 
                  v-model="user.first_name" 
                  id="first_name" 
                  type="text" 
                  required 
                  autocomplete="given-name"
                  :class="{ 'input-error': fieldErrors.first_name }"
                />
                <span v-if="fieldErrors.first_name" class="error-text">{{ fieldErrors.first_name }}</span>
              </div>
              
              <div class="form-group">
                <label for="last_name">Last Name</label>
                <input 
                  v-model="user.last_name" 
                  id="last_name" 
                  type="text" 
                  required 
                  autocomplete="family-name"
                  :class="{ 'input-error': fieldErrors.last_name }"
                />
                <span v-if="fieldErrors.last_name" class="error-text">{{ fieldErrors.last_name }}</span>
              </div>
              
              <div class="form-group">
                <label for="email">Email Address</label>
                <input 
                  v-model="user.email" 
                  id="email" 
                  type="email" 
                  required 
                  autocomplete="email"
                  :class="{ 'input-error': fieldErrors.email }"
                />
                <span v-if="fieldErrors.email" class="error-text">{{ fieldErrors.email }}</span>
              </div>
              
              <div class="form-group">
                <label for="password">Password</label>
                  <input 
                    v-model="user.password" 
                    id="password" 
                    :type="showPassword ? 'text' : 'password'" 
                    required 
                    autocomplete="new-password"
                    :class="{ 'input-error': fieldErrors.password }"
                  />
                <span v-if="fieldErrors.password" class="error-text">{{ fieldErrors.password }}</span>
                <div class="password-strength" v-if="user.password">
                  <div class="strength-meter">
                    <div class="strength-segment" :class="passwordStrength >= 1 ? 'active' : ''"></div>
                    <div class="strength-segment" :class="passwordStrength >= 2 ? 'active' : ''"></div>
                    <div class="strength-segment" :class="passwordStrength >= 3 ? 'active' : ''"></div>
                    <div class="strength-segment" :class="passwordStrength >= 4 ? 'active' : ''"></div>
                  </div>
                  <span class="strength-text">{{ passwordStrengthText }}</span>
                </div>
              </div>
              
              <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                  <input 
                    v-model="confirmPassword" 
                    id="confirm_password" 
                    :type="showConfirmPassword ? 'text' : 'password'" 
                    required 
                    autocomplete="new-password"
                    :class="{ 'input-error': fieldErrors.confirmPassword }"
                  />
                <span v-if="fieldErrors.confirmPassword" class="error-text">{{ fieldErrors.confirmPassword }}</span>
              </div>
            </div>

            <div class="card-footer">
              <p v-if="error" class="error-message">{{ error }}</p>
              <div class="button-container">
                <button type="submit" class="primary-btn next-btn">
                  SIGN ME UP!
                  <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"></path>
                  </svg>
                </button>
              </div>
              <p class="login-link">Already have an account? <a href="/login">Sign in</a></p>
            </div>
          </form>
        </transition>

        <!-- Step 2: Organization Info -->
        <transition name="fade" mode="out-in">
          <form 
            v-if="step === 2" 
            class="registration-card-second" 
            @submit.prevent="register"
          >
              <h1>Now Lets know more About your Organisation</h1>
          <div class="banners-container">
          <!-- Banner 1 -->
          <div class="banner" style="border: 1px solid #6366f1;">
            <p class="banner-text"><span style="font-weight: bold; color: #6366f1;"><span><img src="../assets/images/info-33.png" alt="Info" class="info-icon"/></span>Why Join Stockify? </span>Stay ahead of the curve with real-time stock insights and smart alerts. Make smarter investment decisions effortlessly.</p>
          </div>

          <!-- Banner 2 -->
          <div class="banner" style="background: linear-gradient(90deg, #6366f1, #a855f7);">
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Your Data is Safe </span>We use bank-level security to keep your personal and investment data private and protected.</p>
          </div>

          <!-- Banner 3 -->
          <div class="banner" style="background-color: #d59bf6;">
            <h3 class="banner-title"></h3>
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Fast & Easy Setup </span>Create your account in under a minute. No paperwork, no hassle – just seamless onboarding.</p>
          </div>
        </div>

            <div class="form-grid">
              <div class="form-group full-width">
                <label for="org_name">Organization Name</label>
                <input 
                  v-model="organization.name" 
                  id="org_name" 
                  type="text" 
                  required 
                  :class="{ 'input-error': fieldErrors.orgName }"
                />
                <span v-if="fieldErrors.orgName" class="error-text">{{ fieldErrors.orgName }}</span>
              </div>

              <div class="form-group full-width">
                <label for="org_desc">Organization Description</label>
                <textarea 
                  v-model="organization.description" 
                  id="org_desc" 
                  rows="3" 
                  required 
                  :class="{ 'input-error': fieldErrors.orgDescription }"
                ></textarea>
                <span v-if="fieldErrors.orgDescription" class="error-text">{{ fieldErrors.orgDescription }}</span>
              </div>

              <div class="form-group full-width">
                <label for="org_address">Address</label>
                <input 
                  v-model="organization.address" 
                  id="org_address" 
                  type="text" 
                  required 
                  :class="{ 'input-error': fieldErrors.orgAddress }"
                />
                <span v-if="fieldErrors.orgAddress" class="error-text">{{ fieldErrors.orgAddress }}</span>
              </div>

              <div class="form-group">
                <label for="org_phone">Phone Number</label>
                <input 
                  v-model="organization.phone_number" 
                  id="org_phone" 
                  type="tel" 
                  autocomplete="tel"
                  :class="{ 'input-error': fieldErrors.orgPhone }"
                />
                <span v-if="fieldErrors.orgPhone" class="error-text">{{ fieldErrors.orgPhone }}</span>
              </div>

              <div class="form-group">
                <label for="org_email">Organization Email</label>
                <input 
                  v-model="organization.email" 
                  id="org_email" 
                  type="email" 
                  required 
                  autocomplete="email"
                  :class="{ 'input-error': fieldErrors.orgEmail }"
                />
                <span v-if="fieldErrors.orgEmail" class="error-text">{{ fieldErrors.orgEmail }}</span>
              </div>

              <div class="form-group">
                <label for="org_date">Date Established</label>
                <input 
                  v-model="organization.date_established" 
                  id="org_date" 
                  type="date" 
                  required
                  :max="currentDate"
                  :class="{ 'input-error': fieldErrors.orgDate }"
                />
                <span v-if="fieldErrors.orgDate" class="error-text">{{ fieldErrors.orgDate }}</span>
              </div>
            </div>

            <div class="card-footer">
              <p v-if="error" class="error-message">{{ error }}</p>
              <div class="button-container-second">
                <button type="button" class="secondary-btn back-btn" @click="step = 1">
                  <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 12H5M12 19l-7-7 7-7"></path>
                  </svg>
                  Back
                </button>
                <button type="submit" class="primary-btn" :disabled="loading">
                  <span v-if="loading" class="loading-spinner"></span>
                  <span v-else>Register & Continue</span>
                </button>
              </div>
            </div>
          </form>
        </transition>

        <!-- Step 3: OTP Form -->
        <transition name="fade" mode="out-in">
          <form 
            v-if="step === 3" 
            class="registration-card otp-card" 
            @submit.prevent="verifyOTP"
          >
          <h1>Now lets Verify and get You in the System</h1>
          <div class="banners-container">
          <!-- Banner 1 -->
          <div class="banner" style="border: 1px solid #6366f1;">
            <p class="banner-text"><span style="font-weight: bold; color: #6366f1;"><span><img src="../assets/images/info-33.png" alt="Info" class="info-icon"/></span>Why Join Stockify? </span>Stay ahead of the curve with real-time stock insights and smart alerts. Make smarter investment decisions effortlessly.</p>
          </div>

          <!-- Banner 2 -->
          <div class="banner" style="background: linear-gradient(90deg, #6366f1, #a855f7);">
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Your Data is Safe </span>We use bank-level security to keep your personal and investment data private and protected.</p>
          </div>

          <!-- Banner 3 -->
          <div class="banner" style="background-color: #d59bf6;">
            <h3 class="banner-title"></h3>
            <p class="banner-text" style="color: white;"><span style="font-weight: bold; color: white;"><span><img src="../assets/images/info.png" alt="Info" class="info-icon"/></span>Fast & Easy Setup </span>Create your account in under a minute. No paperwork, no hassle – just seamless onboarding.</p>
          </div>
        </div>

            <div class="otp-container">
              <label class="otp-label">Enter 6-digit code</label>
              <div class="otp-input-group">
                <input 
                  v-for="(_, index) in 6" 
                  :key="index"
                  ref="otpInputs"
                  v-model="otpDigits[index]"
                  type="text" 
                  maxlength="1"
                  class="otp-input"
                  @input="handleOtpInput(index)"
                  @keydown="handleOtpKeydown($event, index)"
                  inputmode="numeric"
                  pattern="[0-9]*"
                />
              </div>
              <p v-if="error" class="error-message">{{ error }}</p>
              
              <div class="resend-container">
                <p class="user-sent-to">We've sent a verification code to<br><strong>{{ user.email }}</strong></p>
                <p class="otp-resend">
                  Didn't receive the code? 
                  <button 
                    type="button" 
                    class="resend-btn" 
                    :disabled="resendCountdown > 0"
                    @click="resendOTP"
                  >
                    <span v-if="resendCountdown > 0">Request new code in {{ resendCountdown }}s</span>
                    <span v-else>Resend code</span>
                  </button>
                </p>
              </div>
            </div>

            <div class="card-footer">
              <div class="button-container">
                <button type="submit" class="primary-btn verify-btn" :disabled="loading || !isOtpComplete">
                  <span v-if="loading" class="loading-spinner"></span>
                  <span v-else>Verify & Continue</span>
                </button>
              </div>
            </div>
          </form>
        </transition>
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
      otpDigits: ['', '', '', '', '', ''],
      step: 1,
      error: '',
      success: '',
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      fieldErrors: {},
      resendCountdown: 30,
      resendTimer: null,
      currentDate: new Date().toISOString().split('T')[0]
    };
  },
  computed: {
    progressWidth() {
      return (this.step / 3) * 100;
    },
    passwordStrength() {
      const password = this.user.password;
      if (!password) return 0;
      
      let strength = 0;
      
      // Length check
      if (password.length >= 8) strength++;
      
      // Contains uppercase
      if (/[A-Z]/.test(password)) strength++;
      
      // Contains lowercase
      if (/[a-z]/.test(password)) strength++;
      
      // Contains numbers or special chars
      if (/[0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
      
      return strength;
    },
    passwordStrengthText() {
      const strength = this.passwordStrength;
      if (strength === 0) return "Very Weak";
      if (strength === 1) return "Weak";
      if (strength === 2) return "Medium";
      if (strength === 3) return "Strong";
      if (strength === 4) return "Very Strong";
      return "";
    },
    otp() {
      return this.otpDigits.join('');
    },
    isOtpComplete() {
      return this.otpDigits.every(digit => digit.length === 1);
    }
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    validateUserInfo() {
      this.fieldErrors = {};
      let isValid = true;
      
      // Username validation
      if (!this.user.username) {
        this.fieldErrors.username = "Username is required";
        isValid = false;
      } else if (this.user.username.length < 3) {
        this.fieldErrors.username = "Username must be at least 3 characters";
        isValid = false;
      }
      
      // Name validation
      if (!this.user.first_name) {
        this.fieldErrors.first_name = "First name is required";
        isValid = false;
      }
      
      if (!this.user.last_name) {
        this.fieldErrors.last_name = "Last name is required";
        isValid = false;
      }
      
      // Email validation
      if (!this.user.email) {
        this.fieldErrors.email = "Email is required";
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(this.user.email)) {
        this.fieldErrors.email = "Please enter a valid email address";
        isValid = false;
      }
      
      // Password validation
      if (!this.user.password) {
        this.fieldErrors.password = "Password is required";
        isValid = false;
      } else if (this.user.password.length < 8) {
        this.fieldErrors.password = "Password must be at least 8 characters";
        isValid = false;
      } else if (this.passwordStrength < 3) {
        this.fieldErrors.password = "Password is too weak";
        isValid = false;
      }
      
      // Confirm password
      if (this.user.password !== this.confirmPassword) {
        this.fieldErrors.confirmPassword = "Passwords do not match";
        isValid = false;
      }
      
      return isValid;
    },
    
    validateOrgInfo() {
      this.fieldErrors = {};
      let isValid = true;
      
      if (!this.organization.name) {
        this.fieldErrors.orgName = "Organization name is required";
        isValid = false;
      }
      
      if (!this.organization.description) {
        this.fieldErrors.orgDescription = "Description is required";
        isValid = false;
      }
      
      if (!this.organization.address) {
        this.fieldErrors.orgAddress = "Address is required";
        isValid = false;
      }
      
      if (!this.organization.email) {
        this.fieldErrors.orgEmail = "Email is required";
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(this.organization.email)) {
        this.fieldErrors.orgEmail = "Please enter a valid email address";
        isValid = false;
      }
      
      if (!this.organization.date_established) {
        this.fieldErrors.orgDate = "Date established is required";
        isValid = false;
      }
      
      return isValid;
    },
    
    nextStepUser() {
      this.error = '';
      if (this.validateUserInfo()) {
        this.step = 2;
      }
    },

    async register() {
      if (!this.validateOrgInfo()) {
        return;
      }
      
      this.error = '';
      this.loading = true;
      
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
          this.startResendCountdown();
        } else {
          this.error = data.error || "Registration failed.";
        }
      } catch (error) {
        this.error = "Error: " + error;
      } finally {
        this.loading = false;
      }
    },

    async verifyOTP() {
      if (!this.isOtpComplete) {
        this.error = "Please enter the complete 6-digit code";
        return;
      }
      
      this.error = '';
      this.loading = true;
      
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

        if (response.status === 200 && response.data.email) {
          localStorage.setItem("userEmail", response.data.email);
          await this.authStore.fetchUser();
          this.success = "OTP verified successfully!";
          
          // Show success animation
          this.showSuccessAnimation();
          
          // Redirect after a short delay
          setTimeout(() => {
            this.$router.push("/dashboard");
          }, 500);
        } else {
          this.error = response.data.error || "Invalid OTP.";
        }
      } catch (err) {
        this.error = "Error verifying OTP: " + err.message;
      } finally {
        this.loading = false;
      }
    },
    
    handleOtpInput(index) {
      // Format to ensure only numbers
      this.otpDigits[index] = this.otpDigits[index].replace(/[^0-9]/g, '');
      
      // Auto-focus next input
      if (this.otpDigits[index] && index < 5) {
        this.$nextTick(() => {
          this.$refs.otpInputs[index + 1].focus();
        });
      }
    },
    
    handleOtpKeydown(event, index) {
      // Handle backspace to go to previous input
      if (event.key === 'Backspace' && !this.otpDigits[index] && index > 0) {
        this.$refs.otpInputs[index - 1].focus();
      }
    },
    
    startResendCountdown() {
      this.resendCountdown = 30;
      clearInterval(this.resendTimer);
      this.resendTimer = setInterval(() => {
        if (this.resendCountdown > 0) {
          this.resendCountdown--;
        } else {
          clearInterval(this.resendTimer);
        }
      }, 1000);
    },
    
    async resendOTP() {
      if (this.resendCountdown > 0) return;
      
      try {
        await this.authStore.setCsrfToken();
        
        const response = await axios.post(
          "http://localhost:8000/api/resend-otp/",
          {
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
        
        if (response.status === 200) {
          this.success = "A new OTP has been sent to your email";
          this.startResendCountdown();
        } else {
          this.error = response.data.error || "Failed to resend OTP";
        }
      } catch (err) {
        this.error = "Error resending OTP: " + err.message;
      }
    },
    
    showSuccessAnimation() {
      // You would implement a success animation here
      // This is just a placeholder
      console.log("Show success animation");
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
  },
  beforeUnmount() {
    clearInterval(this.resendTimer);
  }
};
</script>

<style scoped>
.registration-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1rem;
  min-height: 100vh;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f9f9fd;
  margin-right: 400px;
}

.progress-container {
  width: 30%;
  max-width: 600px;
  margin-bottom: 2rem;
}

.progress-bar {
  height: 8px;
  background-color: #e0e6ff;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  margin-top: 10px;
  margin-left: -110px;
}

.progress {
  height: 50%;
  background: linear-gradient(90deg, #6366f1, #a855f7);
  border-radius: 4px;
  transition: width 0.4s ease;
}

.steps-indicator {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-left: -80px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  color: #444;
  transition: all 0.3s ease;
  font-size: 12px;
  margin-right: 10px;
  font-weight: lighter;
}

.step.active {
  color: #4c1d95;
  font-weight: 600;
}

.step.completed {
  color: #6366f1;
}

.step-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 600;
  margin-bottom: 8px;
  background-color: #e0e6ff;
  border: 2px solid #e0e6ff;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background-color: #a855f7;
  color: white;
  border-color: #a855f7;
}

.step.completed .step-number {
  background-color: #6366f1;
  color: white;
  border-color: #6366f1;
}

.card-container {
  width: 100%;
  max-width: 600px;
  perspective: 1000px;
}

.registration-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1);
  width: 100%;
  transition: transform 0.4s ease, opacity 0.4s ease;
  transform-style: preserve-3d;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: -15px;
  margin-left: -120px;
}

.registration-card-second {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1);
  width: 750px;
  transition: transform 0.4s ease, opacity 0.4s ease;
  transform-style: preserve-3d;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 800px;
  margin-left: -150px;
}

.card-header {
  text-align: center;
  margin-bottom: 1rem;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.logo-icon {
  width: 25px;
  height: 25px;
  color: #6366f1;
  margin-right: 8px;
}

.logo-text {
  font-size: 15px;
  font-weight: 700;
  color: #6366f1;
  margin: 0;
}

.welcome-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #718096;
  margin: 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  height: 170px;
}

.form-group {
  display: flex;
  flex-direction: column;
  position: relative;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 12px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 10px;
  margin-left: -3px;
}

.form-group input, 
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 11px;
  color: #444;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.form-group input.input-error,
.form-group textarea.input-error {
  border-color: #e53e3e;
}

.error-text {
  color: #e53e3e;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.password-input-container {
  position: relative;
}

.password-toggle-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #718096;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.eye-icon {
  width: 20px;
  height: 20px;
}

.password-strength {
  margin-top: 0.5rem;
}

.strength-meter {
  display: flex;
  gap: 4px;
  margin-bottom: 4px;
}

.strength-segment {
  height: 4px;
  flex: 1;
  background-color: #e2e8f0;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-segment.active:nth-child(1) {
  background-color: #fc8181;
}

.strength-segment.active:nth-child(2) {
  background-color: #f6ad55;
}

.strength-segment.active:nth-child(3) {
  background-color: #68d391;
}

.strength-segment.active:nth-child(4) {
  background-color: #38a169;
}

.strength-text {
  font-size: 0.75rem;
  color: #718096;
}

.card-footer {
  margin-top: 1rem;

}

.button-container {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.button-container-second {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 150px;
}

.primary-btn, 
.secondary-btn {
  border-radius: 8px;
  padding: 10px;
  font-size: 12px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  border: none;
  font-size: 11px;
}

.secondary-btn.back-btn {
  background-color: black;
  color: white;
}
.primary-btn {
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  flex: 1;
  font-size: 12px;
  text-transform: uppercase;
}

.primary-btn.next-btn {
  width: 60%;
  max-width: 360px;
  margin-top: 10px;
}

.primary-btn:hover {
  background: linear-gradient(135deg, #4f46e5, #9333ea);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.primary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.secondary-btn {
  background-color: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.secondary-btn:hover {
  background-color: #e2e8f0;
  color: #475569;
}

.next-btn {
  width: 60%;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 12px;
  color: #718096;
  text-decoration: none;
}

.login-link a {
  color: #6366f1;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: none;
  color: #4c1d95;
}

.error-message {
  color: #e53e3e;
  text-align: center;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

/* OTP Card Styles */
.otp-card {
  padding-bottom: 3rem;
}

.email-icon {
  width: 48px;
  height: 48px;
  color: #6366f1;
  margin: 1rem 0;
}

.otp-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.otp-label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1rem;
  margin-bottom: -0.5rem;
}

.otp-input-group {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.otp-input {
  width: 50px;
  height: 60px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.otp-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.resend-container {
  margin-top: 1rem;
  text-align: center;
}

.otp-resend {
  color: #4a5568;
  font-size: 0.875rem;
  margin: 0;
}

.resend-btn {
  background: none;
  border: none;
  color: #6366f1;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 0.25rem;
  font-size: 0.875rem;
}

.resend-btn:disabled {
  color: #a0aec0;
  cursor: not-allowed;
}

.verify-btn {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.fade-enter-active, 
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Responsive Adjustments */
@media (max-width: 640px) {
  .registration-container {
    padding: 1rem 0.5rem;
  }
  
  .registration-card {
    padding: 1.5rem;
    border-radius: 12px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .button-container {
    flex-direction: column;
  }
  
  .otp-input {
    width: 40px;
    height: 50px;
    font-size: 1.25rem;
  }
}

.password-toddle-btn {
  width: 10px;
  height: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}
.password-toddle-btn:hover {
  color: #4a5568;
}

.welcome-text {
  font-size: 15px;
  color: #4a5568;
  font-weight: 600;
  margin-top: 50px;
  margin-left: -70px;
}

.registration-card {
  width: 700px;
  margin-right: 170px;
}

.banners-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  margin-top: -50px;
}

@media (min-width: 768px) {
  .banners-container {
    flex-direction: row;
    justify-content: space-between;
  }
}

.banner {
  background: #fff;
  border-radius: 20px;
  padding: 10px;
  flex: 1;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.banner:hover {
  transform: translateY(-5px);
}

.icon-circle {
  width: 60px;
  height: 60px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

.banner-title {
  font-size: 11px;
  font-weight: 600;
}

.banner-text {
  font-size: 11px;
  color: #555;
}
.main-container {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  gap: 20px;
  padding: 20px;
  -webkit-overflow-scrolling: touch; /* Smooth on iOS */
}

/* Hide scrollbar for Webkit (Chrome, Safari) */
.main-container::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for Firefox */
.main-container {
  scrollbar-width: none; /* Firefox */
}

/* Hide scrollbar for Edge and IE */
.main-container {
  -ms-overflow-style: none; /* IE and Edge */
}


#dashboard .d-flex .vh-100{
  margin-right: 500px;
}

.info-icon {
  width: 15px;
  height: 15px;
  margin-right: 5px;
}

/* Hide scrollbar for Webkit browsers (Chrome, Safari) */
.registration-container::-webkit-scrollbar {
  width: 0px;
  background: transparent;
}

/* Hide scrollbar for Firefox */
.registration-container {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}

.registration-container::-webkit-scrollbar {
  display: none;
}

.step-text {
  color: black;
  font-size: 15px;
}

.user-sent-to {
  font-size: 12px;
  margin-top: -20px;
  color: #4444;
}
</style>