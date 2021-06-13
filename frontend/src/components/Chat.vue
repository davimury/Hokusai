<template>
  <div class="h-screen">
    <Header></Header>
    <main class="">
      <chat-window
        :current-user-id="user_id"
        :rooms="rooms"
        :loading-rooms="loading_rooms"
        :rooms-loaded="rooms_loaded"
        :messages-loaded="messages_loaded"
        :messages="messages"
        :height="height"
        :show-files='false'
        :show-audio="false"
        :text-formatting="false"
        :show-add-room="false"
        theme="dark"
        :styles="styles"
        @fetch-messages="fetchMessages"
        @send-message="sendMessage"
      />
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import ChatWindow from "vue-advanced-chat";
import "vue-advanced-chat/dist/vue-advanced-chat.css";
export default {
  name: "Chat",
  components: {
    Header,
    Footer,
    ChatWindow,
  },
  data() {
    return {
      user_id: this.$store.getters.UserId,
      connection: null,
      loading_rooms: true,
      rooms_loaded: false,
      messages_loaded: false,
      rooms: [],
      messages: [],
      styles: {
        icons: {
          add: '#8B5CF6',
          toggle: '#8B5CF6',
        },
        room: {
          backgroundCounterBadge: '#8B5CF6',
        }
        
      },
      currentUserId: 1234,
      height: "calc(100vh - 60.8px)",
    };
  },
   created: function() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket(`ws://localhost:8000/ws/${this.user_id}`)

    var vm = this;
    this.connection.onmessage = function(event) {
      let data = JSON.parse(event['data'])

      if(data['rooms'] != undefined){
        vm.rooms = data['rooms']
        vm.loading_rooms = false
        vm.rooms_loaded = true
      } 
      
      else if (data['messages'] != undefined){
        vm.messages = data['messages']
        vm.messages_loaded = true
      }

      else if (data['new_message'] != undefined){
        let messages = vm.messages
        messages.push(data['new_message'])
        vm.messages = messages
      }
    }

    this.connection.onopen = function(event) {
      console.log(event)
      console.log("Successfully connected to the echo websocket server...")
    }

  },
  methods: {
    sendMessage ({ content, roomId, file, replyMessage }) {
      this.connection.send(JSON.stringify({'send_message': {'content': content, 'room_id': roomId, 'sender_id': this.user_id}}))
    },
    fetchMessages(	{ room, options }) {
      this.connection.send(JSON.stringify({'get_messages': room['roomId']}))
    }
  },
};
</script>

<style>
</style>