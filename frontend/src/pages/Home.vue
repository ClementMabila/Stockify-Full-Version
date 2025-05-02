<script>
import { useAuthStore } from '../store/auth.js'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return {
      authStore,
      router
    }
  },
  methods: {
    async logout() {
      try {
        await this.authStore.logout(this.$router)
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
  },
  async mounted() {
    try {
      await this.authStore.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }
}
</script>

<template>
  <div>
    <h1>Welcome to the home page</h1>
    <div v-if="authStore.isAuthenticated">
      <p>Hi there {{ authStore.user?.username }}!</p>
      <p>You are logged in.</p>
      <button @click="logout">Logout</button>
    </div>
    <p v-else>
      You are not logged in.
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>