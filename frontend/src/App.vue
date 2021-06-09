<template>
  <div id="app" class="w-full">
    <div v-if="loading" class="w-screen h-screen flex align-middle">
      <fingerprint-spinner
        :animation-duration="1500"
        :size="90"
        color="#8B5CF6"
        class="m-auto "
      />
    </div>
    <router-view v-else />
  </div>
</template>

<script>
import { FingerprintSpinner } from "epic-spinners";
export default {
  components: {
    FingerprintSpinner,
  },
  name: "App",
  data() {
    return {
      loading: true,
    };
  },
  mounted() {
    
    this.loading = false;
  },
};
</script>