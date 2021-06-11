<template>
  <div class="h-screen">
    <Header></Header>
    <main class="">
      <chat-window
        :current-user-id="currentUserId"
        :rooms="rooms"
        :messages="messages"
        :height="height"
        show-files="false"
        show-audio="false"
        text-formatting="false"
        theme="dark"
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
      rooms: [
        {
          roomId: 1,
          roomName: "Room 1",
          avatar: "assets/imgs/people.png",
          unreadCount: 4,
          index: 3,
          lastMessage: {
            content: "Last message received",
            senderId: 1234,
            username: "John Doe",
            timestamp: "10:20",
            saved: true,
            distributed: false,
            seen: false,
            new: true,
          },
          users: [
            {
              _id: 1234,
              username: "John Doe",
              avatar: "assets/imgs/doe.png",
              status: {
                state: "online",
                lastChanged: "today, 14:30",
              },
            },
            {
              _id: 4321,
              username: "John Snow",
              avatar: "assets/imgs/snow.png",
              status: {
                state: "offline",
                lastChanged: "14 July, 20:00",
              },
            },
          ],
          typingUsers: [4321],
        },
      ],
      messages: [
        {
          _id: 7890,
          content: "message 1",
          senderId: 1234,
          username: "John Doe",
          avatar: "assets/imgs/doe.png",
          date: "13 November",
          timestamp: "10:20",
          system: false,
          saved: true,
          distributed: true,
          seen: true,
          disableActions: false,
          disableReactions: false,
          file: {
            name: "My File",
            size: 67351,
            type: "png",
            audio: true,
            duration: 14.4,
            url: "https://firebasestorage.googleapis.com/...",
            preview: "data:image/png;base64,iVBORw0KGgoAA...",
          },
          reactions: {
            wink: [
              1234, // USER_ID
              4321,
            ],
            laughing: [1234],
          },
        },
      ],
      currentUserId: 1234,
      height: "calc(100vh - 60.8px)",
    };
  },
};
</script>

<style>
</style>