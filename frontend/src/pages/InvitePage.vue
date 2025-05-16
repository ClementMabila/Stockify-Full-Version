<template>
  <BaseLayout>
    <div class="sales-entrie-container" style="background-color: transparent;">
      <div class="InviteContainer">
        <h4>Invite People</h4>
        <p>All invited people will have access to the sites in your organization.</p>

        <div class="invite-options">
          <button :class="{ active: inviteType === 'email' }" @click="setInviteType('email')">Invite with Email</button>
          <button :class="{ active: inviteType === 'link' }" @click="setInviteType('link')">Invite with Link</button>
        </div>

        <!-- Invite with Email -->
        <form v-if="inviteType === 'email'" @submit.prevent="sendInvitation">
          <div>
            <label for="email" class="email-label">Email</label>
            <input v-model="email" type="email" id="email" required />
          </div>

          <div>
            <label for="group" class="email-label">Select Group</label>
            <select v-model="selectedGroup" id="group" required>
              <option class="select-label" disabled value="">Select a group</option>
              <option v-for="group in groups" :key="group.id" :value="group.name">{{ group.name }}</option>
            </select>
          </div>

          <button type="submit">Send Invite</button>
        </form>

        <!-- Invite with Link -->
        <div v-if="inviteType === 'link'" class="invite-link-container">
          <div>
            <label for="email" class="email-label">Email</label>
            <input v-model="email" type="email" id="email" required />
          </div>

          <div>
            <label for="group">Select Group</label>
            <select v-model="selectedGroup" id="group" required>
              <option disabled value="">Select a group</option>
              <option class="group-value" v-for="group in groups" :key="group.id" :value="group.name">{{ group.name }}</option>
            </select>
          </div>

          <button v-if="!inviteLink" @click="generateInviteLink">Generate Link</button>
          <div v-else>
            <p>Your invite link:</p>
            <div class="link-box">
              <input v-model="inviteLink" readonly />
              <button @click="copyLink">Copy Link</button>
            </div>
          </div>
        </div>

        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>

        <div class="last-section">
          <p class="below-text">
            People with organisation email will be able to join with a link. 
            <a href="#">Deactivate</a> if you don't need this.
          </p>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from "../components/BaseLayout.vue";

export default {
  name: "InvitePage",
  components: {
    BaseLayout,
  },
  data() {
    return {
      email: "",
      inviteLink: "",
      inviteType: "email",
      message: "",
      error: "",
      selectedGroup: "",
      groups: [],
    };
  },
  async mounted() {
    try {
      // Fetch groups for the user
      const res = await fetch("http://localhost:8000/api/groups/", {
        method: "GET",
        credentials: "include",  // Important for persisting session cookies
      });
      const data = await res.json();
      this.groups = data.groups || [];
    } catch (err) {
      this.error = "Failed to load groups.";
    }
  },
  methods: {
    // Send an invitation to the user
    async sendInvitation() {
      try {
        // Fetch CSRF token first
        const csrfRes = await fetch("http://localhost:8000/api/set-csrf-token", {
          method: "GET",
          credentials: "include",  // Required to maintain session
        });
        const csrfData = await csrfRes.json();
        const csrfToken = csrfData.csrfToken;

        // Send the invitation with the CSRF token and session credentials
        const res = await fetch("http://localhost:8000/api/send-invitation/", {
          method: "POST",
          credentials: "include",  // Keep user logged in during request
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,  // Include CSRF token
          },
          body: JSON.stringify({ email: this.email, group: this.selectedGroup }),
        });

        const data = await res.json();
        if (res.ok) {
          this.message = data.message;
          this.error = "";
          this.email = "";
          this.selectedGroup = "";
        } else {
          this.error = data.error || "Failed to send invitation.";
          this.message = "";
        }
      } catch (err) {
        this.error = "An error occurred while sending the invitation.";
      }
    },

    // Generate invitation link
    async generateInviteLink() {
      try {
        const res = await fetch("http://localhost:8000/api/generate-invite-url/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: this.email, group: this.selectedGroup }),
        });

        const data = await res.json();
        if (res.ok) {
          this.inviteLink = data.invite_link;
          this.message = "Invite link generated successfully!";
          this.error = "";
        } else {
          this.error = data.error || "Failed to generate invite link.";
          this.message = "";
        }
      } catch (err) {
        this.error = "An error occurred while generating the invite link.";
      }
    },

    // Copy the invite link to clipboard
    copyLink() {
      navigator.clipboard.writeText(this.inviteLink).then(() => {
        this.message = "Link copied to clipboard!";
        this.error = "";
      }).catch(() => {
        this.error = "Failed to copy the link.";
        this.message = "";
      });
    },

    // Set invitation type (email or link)
    setInviteType(type) {
      this.inviteType = type;
      this.message = "";
      this.error = "";
      this.inviteLink = "";
    },
  },
};
</script>
