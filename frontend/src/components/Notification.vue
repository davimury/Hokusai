<template>
  <div id="notification">
    <button @click="isActive = !isActive">
      <notification-bell
        :count="1"
        iconColor="#8b5cf6"
        :size="24"
        counterLocation="lowerRight"
        :animated="true"
      />
    </button>
    <div
      v-if="isActive"
      class="flex justify-center fixed"
      style="right: 185px; top: -100px"
    >
      <div class="bg-lightgray mt-40 px-4 py-3 rounded-lg shadow-md max-w-xs">
        <div class="flex items-center justify-between">
          <span class="font-medium text-sm">Notificações</span>
          <button
            class=" rounded-full"
            @click="isActive = !isActive"
          >
            <span class="material-icons "> close </span>
          </button>
        </div>
        <div v-for="data in dataArr" :key="data['id']">
          <div
            v-if="!data['status']"
            class="flex items-center mt-3 hover:bg-gray-100 rounded-lg px-1 py-1 cursor-pointer"
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
              <p class="text-sm">
                {{ data["username"] }} pediu para se conectar com você!
              </p>
              <!-- <span class="text-sm text-blue font-semibold">Alguns segundos atrás</span> -->
              <button
                @click="acceptConnection(data['id'])"
                class="bg-purple-600 hover:bg-purple-800 text-white py-2 px-4 mr-2 border text-sm rounded-md"
              >
                Aceitar
              </button>
              <button
                class="bg-white hover:bg-gray-50 py-2 px-4 text-sm border rounded-md"
              >
                Recusar
              </button>
            </div>
          </div>

          <div
            v-if="data['status']"
            class="flex items-center mt-3 rounded-lg px-1 py-1 cursor-pointer disabled opacity-50"
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
              <span class="font-medium text-sm">{{ data["name"] }}</span>
              <p class="text-sm">
                {{ data["username"] }} pediu para se conectar com você!
              </p>
              <span class="text-sm text-blue">Alguns segundos atrás</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NotificationBell from "vue-notification-bell";
import Pusher from "pusher-js";
import axios from "axios";

export default {
  name: "Notification",

  components: {
    NotificationBell,
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
        this.dataArr.push(data);
      },
      this
    );
  },
  mounted() {
    axios.get("/profile/notifications").then((response) => {
      this.dataArr = response["data"];
      console.log(this.dataArr);
    });
  },
  computed: {
    getProfilePic(id) {
      return require("@/assets/img/profile/" + id + ".jpg");
    },
  },

  methods: {
    acceptConnection: async function (id) {
      axios({
        method: "post",
        url: `/connection/${id}/accept`,
      });

      axios.get("/profile/notifications").then((response) => {
        console.log(this.dataArr);
        this.dataArr = response["data"];
      });
    },
  },
};
</script>
<style>
</style>
