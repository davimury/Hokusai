<template>
  <div id="notification">
    <button @click="isActive = !isActive">
      <notification-bell
        :count="this.count"
        iconColor="#8b5cf6"
        :size="24"
        counterLocation="lowerRight"
        :animated="true"
      />
    </button>
    <transition
            mode="out-in"
            enter-active-class="animate__animated animate__fadeInDown"
            leave-active-class="animate__animated animate__fadeOutUp"
          >
    <div
      v-if="isActive"
      class="max-h-full inset-0 sm:w-auto sm:-right-8 sm:h-auto flex justify-center fixed"
      style=" top: -100px;"
      
      v-on-clickaway="away"
    >
      <div class="bg-lightgray mt-40 px-4 py-4 rounded-lg shadow-md max-w-xs">
        <div class="flex items-center justify-between">
          <span class="font-medium text-sm">Notificações</span>
          <button
            class=" rounded-full"
            @click="isActive = !isActive"
          >
            <span class="material-icons "> close </span>
          </button>
        </div>
          <div v-if="dataArr.length > 0">
            <div v-for="data in dataArr.slice(0, 5).reverse()" :key="data['id']">
              <div v-if="data['type'] == 0">
              </div>
              <div v-if="data['type'] == 1">
                <div
                  v-if="!data['status']"
                  class="flex items-center mt-3 rounded-lg px-1 py-1 cursor-pointer"
                >
                  <div class="flex flex-shrink-0">
                    <img
                      class="h-16 w-16 rounded-full"
                      :src="
                        require('@/assets/img/profile/' + data['user_id'] + '.jpg')
                      "
                    />
                  </div>
                  <div class="ml-3 text-left">
                    <span class="font-medium text-sm">{{ data["name"] }}</span>
                    <p class="text-sm mt-2">
                      {{ data["username"] }} pediu para se conectar com você!
                    </p>
                    <!-- <span class="text-sm text-blue font-semibold">Alguns segundos atrás</span> -->
                    <button
                      @click="acceptConnection(data['id'])"
                      class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white py-2 px-4 mr-2 mt-4 text-sm "
                    >
                      Aceitar
                    </button>
                    <button
                      @click="refuseConnection(data['id'])"
                      class="rounded-lg bg-darkgray hover:bg-lightergray focus:outline-none border-darkgray py-2 px-4 mr-2 mt-4 text-sm "
                    >
                      Recusar
                    </button>
                  </div>
                </div>
                <div
                  v-else
                  class="flex items-center mt-3 rounded-lg px-1 py-1 disabled opacity-50"
                >
                  <div class="flex flex-shrink-0">
                    <img
                      class="h-16 w-16 rounded-full"
                      :src="
                        require('@/assets/img/profile/' + data['user_id'] + '.jpg')
                      "
                    />
                  </div>
                  <div class="ml-3 text-left text-gray-400">
                    <p class="text-sm">
                      Você aceitou o pedido de <b>{{data["username"]}}</b> para se conectar com você!
                    </p>
                    <vue-moments-ago :date="data['last_updated']" elementClass="text-sm text-blue"></vue-moments-ago>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <span class="text-gray-500 font-medium text-sm text-center p-5 inline-block">Nenhuma notificação encontrada!</span>
          </div>
      </div>
    
    </div>
    </transition>
  </div>
</template>
<script>
import NotificationBell from "vue-notification-bell";
import VueMomentsAgo from './MomentsAgo.vue'
import { directive as onClickaway } from "vue-clickaway";
import Pusher from "pusher-js";
import axios from "axios";

export default {
  name: "Notification",

  components: {
    NotificationBell,
    VueMomentsAgo,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      isActive: false,
      count: 0,
      dataArr: [{ user_id: 1, username: "chris", name: "chris" }],
    };
  },
  created() {
    const pusher = new Pusher("ad8252dd0a9b80dd351f", { cluster: "us2" });
    const channel = pusher.subscribe("hokusai-notify");

    channel.bind(
      this.$store.getters.Username,
      function (data) {
        this.count = this.count + 1
        this.dataArr.push(data);
      },
      this
    );
  },
  mounted() {
    axios.get("/user/notifications").then((response) => {
      this.dataArr = response["data"];
      this.dataArr.forEach(element => {
        if(element['status'] != true)
          this.count = this.count + 1
      });
    });
  },
  computed: {
    getProfilePic(id) {
      return require("@/assets/img/profile/" + id + ".jpg");
    },
  },

  methods: {
    away: function () {
      this.isActive = false;
    },
    updateConnections: async function (){
      axios.get("/user/notifications")
      .then((response) => {
        this.dataArr = response["data"];
        this.count = 0
        this.dataArr.forEach(element => {
          if(element['status'] != true)
            this.count = this.count + 1
        });
      });
    },
    acceptConnection: function (id) {
      axios.post('/connection/accept', {con_id: id})
      .then(() => this.updateConnections());
    },
    refuseConnection: function (id) {
      axios.post('/connection/refuse', {con_id: id})
      .then(() => this.updateConnections());
    },
  },
};
</script>
<style>
</style>
