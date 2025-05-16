<template>
    <BaseLayoutUserInterface>
        <div class="Investments-display">
          <section class="Investments-display-section" style="max-height: 600px; overflow-y: auto;">
            <Prole></Prole>
          </section>
        </div>
    </BaseLayoutUserInterface>
    </template>
    <script>
    import BaseLayout from "../components/BaseLayout.vue";
    import BaseLayoutUserInterface from "../components/BaseLayoutUserInterface.vue";
    import Prole from "../components/Prole.vue";
    
    export default {
      name: "StockHistoryPage",
      components: {
        BaseLayoutUserInterface,
        Prole
      }
    }
    </script>