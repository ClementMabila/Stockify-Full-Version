<template>
<BaseLayoutUserInterface>
    <div class="Investments-display">
      <section class="Investments-display-section" style="max-height: 600px; overflow-y: auto;">
        <MessagingPage></MessagingPage>
      </section>
    </div>
</BaseLayoutUserInterface>
</template>
<script>
import BaseLayout from "../components/BaseLayout.vue";
import BaseLayoutUserInterface from "../components/BaseLayoutUserInterface.vue";
import MessagingPage from "../components/MessagingPage.vue";


export default {
  name: "StockHistoryPage",
  components: {
    BaseLayoutUserInterface,
    MessagingPage
  }
}
</script>

<style src="../assets/css/dashboard.css"></style>