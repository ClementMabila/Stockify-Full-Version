<template>
<BaseLayoutUserInterface>
    <div class="Investments-display">
      <section class="Investments-display-section" style="max-height: 600px; overflow-y: auto;">
        <ShowAllInvestment></ShowAllInvestment>
      </section>
    </div>
</BaseLayoutUserInterface>
</template>
<script>
import BaseLayout from "../components/BaseLayout.vue";
import BaseLayoutUserInterface from "../components/BaseLayoutUserInterface.vue";
import ShowAllInvestment from "../components/ShowAllInvestment.vue";

export default {
  name: "StockHistoryPage",
  components: {
    BaseLayoutUserInterface,
    ShowAllInvestment
  }
}
</script>

<style src="../assets/css/dashboard.css"></style>