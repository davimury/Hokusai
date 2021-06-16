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
        :showReactionEmojis="false"
        :show-audio="false"
        :text-formatting="false"
        :show-add-room="false"
        :text-messages="textMessages"
        :message-actions="messageActions"
        theme="dark"
        :styles="styles"
        @fetch-messages="fetchMessages"
        @send-message="sendMessage"
        @edit-message="editMessage"
        @delete-message="deleteMessage"
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
import moment from 'moment';

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
      msgQuerys: 0,
      curRoom: 0,
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
      messageActions: [
        {
          name: 'replyMessage',
          title: 'Responder'
        },
        {
          name: 'editMessage',
          title: 'Editar',
          onlyMe: true
        },
        {
          name: 'deleteMessage',
          title: 'Apagar',
          onlyMe: true
        }
      ],
      textMessages: {
        ROOMS_EMPTY: 'Nenhuma conexão encontrada!',
        ROOM_EMPTY: 'Nenhuma conexão selecionada!',
        NEW_MESSAGES: 'Nova mensagem!',
        MESSAGE_DELETED: 'Essa mensagem foi deletada.',
        MESSAGES_EMPTY: 'Nenhuma mensagem encontrada!',
        CONVERSATION_STARTED: 'Conversa iniciada em:',
        TYPE_MESSAGE: 'Escreva sua mensagem',
        SEARCH: 'Buscar',
        IS_ONLINE: 'Está online',
        LAST_SEEN: 'Ultima vez online: ',
        IS_TYPING: 'Está escrevendo...'
      }
    };
  },
   created: async function() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket(`ws://localhost:8000/ws/${this.user_id}`)

    var vm = this;
    
    this.connection.onmessage = function(event) {
      let data = JSON.parse(event['data'])

      if(data['rooms'] != undefined){
        data['rooms'].forEach((element) => {
          element['avatar'] = require(`../assets/img/profile/${element['avatar']}`)
          element['users'].forEach((element) => {
            element['avatar'] = require(`../assets/img/profile/${element['avatar']}`)
          });
        });

        vm.rooms = data['rooms']
        vm.loading_rooms = false
        vm.rooms_loaded = true
      } 
      
      else if (data['messages'] != undefined){
        if (data['messages'].length === 0){
          vm.messages_loaded = true
        } else {
          data['messages'].forEach((element) => {
            element['avatar'] = require(`../assets/img/profile/${element['avatar']}`)
          });

          var messages = vm.messages
          vm.messages = [...data['messages'], ...messages]
          this.messages_loaded = true
        }
      }

      else if (data['new_message'] != undefined){
        data['new_message']['avatar'] = require(`../assets/img/profile/${data['new_message']['avatar']}`)

        let messages = vm.messages
        messages.push(data['new_message'])
        vm.messages = messages

        vm.rooms.forEach((element, index) => {
          if (element['roomId'] == vm.curRoom){
            element['lastMessage']['content'] = data['new_message']['content']
            element['lastMessage']['timestamp'] = data['new_message']['timestamp']
            element['lastMessage']['seen'] = data['new_message']['seen']
          }
        })
      }

      else if (data['user_status'] != undefined){
        vm.rooms.forEach((element, index) => {
          element['users'].forEach((element, index) => {
            if (element['_id'] == data['user_status']['id']){
              moment.locale('pt');
              element['status']['state'] = data['user_status']['status'] ? "online" : "offline";
              element['status']['lastChanged'] = moment().format('DD [de] MMMM, H:mm');
            }
          })
        })
      }

      else if (data['seen_msg'] != undefined){
        console.log(data['seen_msg'])
        setTimeout(function () {
            vm.messages.forEach((element, index) => {
              if (element['_id'] == data['seen_msg']['id']){
                element['seen'] = true
              }
            });
            /* vm.rooms.forEach((element, index) => {
              if (element['lastMessage']['seen'] == false){
                element['lastMessage']['seen'] == true
                console.log(element['last_message']['seen'])
              }
            }) */
        }, 1000);
      }

      else if (data['edit_msg'] != undefined){
        vm.messages.forEach((element, index) => {
          if (element['_id'] == data['edit_msg']['_id']){
            element['content'] = data['edit_msg']['content']
          }
        });
      }

      else if (data['delete_msg'] != undefined){
        vm.messages.forEach((element, index) => {
          console.log(data['delete_msg'])
          if (element['_id'] == data['delete_msg']['_id']){
            let messages = vm.messages
            console.log(element['_id'])
            messages.splice(index, 1);
            vm.messages = messages
            console.log(vm.messages)
          }
        });
      }
    }

    this.connection.onopen = function(event) {
      console.log(event)
      console.log("Successfully connected to the echo websocket server...")
    }

  },
  methods: {
    async sendMessage ({ content, roomId, file, replyMessage }) {
      this.connection.send(JSON.stringify({'send_message': {'content': content, 'room_id': roomId, 'sender_id': this.user_id, 'reply_message': replyMessage}}))
    },
    async fetchMessages(	{ room, options }) {
      this.messages_loaded = false

      if (this.curRoom != room['roomId']){
        this.curRoom = room['roomId']
        this.msgQuerys = 0
        this.messages = []
      }
      
      this.connection.send(JSON.stringify({'get_messages': room['roomId'], 'query': this.msgQuerys}))
      this.msgQuerys = this.msgQuerys + 1;
    },
    async editMessage({ roomId, messageId, newContent, file, replyMessage, usersTag }) {
      this.connection.send(JSON.stringify({'edit_message': {'messageId': messageId, 'room_id': roomId, 'new_content': newContent, 'reply_message': replyMessage}}))
    },
    async deleteMessage({ roomId, message }){
      this.connection.send(JSON.stringify({'delete_message': message}))
    }
  },
};
</script>

<style>
</style>