<template>
  <div id="app" class="bg-gray-200">
    <Login/>
  </div>
</template>

<script>
import Login from "./pages/Login.vue";

export default {
  name: "App",
  components: {
    Login
  }
};
</script>