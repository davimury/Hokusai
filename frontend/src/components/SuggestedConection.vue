<template>
  <div class="bg-lightgray border border-lightgray rounded-lg block w-full text-white lg:float-left max-w-xs">
        <div class="flex items-center px-4 py-3">
            <img class="h-12 w-12 rounded-full" :src="require(`@/assets/img/profile/${this.user_id}.jpg`)" @error="$event.target.src = require(`@/assets/img/profile/default.jpg`)"/>
            <div class="ml-3">
              <span class="text-sm font-semibold antialiased block leading-tight">{{this.username}}</span>
              <h2>{{this.name}}</h2>
            </div>
          </div>
          <div class="flex flex-col px-4 py-3 ">
            <h1 class="mb-5 text-lg font-semibold">Sugestões de conexão</h1>
            <div v-if="suggestedConection.length > 0">
              <div v-for="user in suggestedConection" :key="user.user_id">
                <a :href="user.username">
                  <div class="flex items-center mb-3 w-100">
                    <img class="h-10 w-10 rounded-full " :src="require(`@/assets/img/profile/${user.user_id}.jpg`)" @error="$event.target.src = require(`@/assets/img/profile/default.jpg`)" />
                    <div class="ml-3 w-full">
                      <span class="text-sm font-semibold antialiased block leading-tight">{{user.username}}</span>
                      <h2 class="text-base font-semibold">{{user.name}}</h2>
                    </div>
                    <div class="text-center w-full">
                      <a
                      @click="requestConnection(user.username)" 
                      class="ml-5 text-purple-500 hover:text-purple-600" href="#"
                      >Conectar</a>
                    </div>
                  </div>
                </a>
              </div>
            </div>
            <div v-else>
              <span class="text-gray-500 font-medium text-sm p-5 inline-block">Nenhuma conexão encontrada!</span>
            </div>
          </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SuggestedConection",

  data() {
    return {
      name: this.$store.getters.Username,
      username: this.$store.getters.Name,
      user_id: this.$store.getters.UserId,
      cacheKey: +new Date(),
      suggestedConection: [],
    };
  },
  created() {
    this.interval = setInterval(() => {
      this.cacheKey = +new Date();
    }, 60 * 1000);
  },
  destroyed() {
    clearInterval(this.interval);
  },
  mounted() {
    axios.get("/profile/suggested").then((response) => {
      this.suggestedConection = response["data"];
    });
  },
  methods: {
    updateConnections: async function (){
      axios.get("/profile/suggested").then((response) => {
        this.suggestedConection = response["data"];
      });
    },
    requestConnection: async function (username) {
      await axios({
        method: "post",
        url: `/profile/${username}/connect`,
      }).then(() => this.updateConnections());
    },
  },
};
</script>

<style>
</style>