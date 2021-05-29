<template>
    <div id="notification">
        <button @click="isActive = !isActive">
            <notification-bell count=1 iconColor="#8b5cf6" size=24 counterLocation="lowerRight" animated="true"/>
        </button>
        <div v-if="isActive" class="flex justify-center fixed" style="right: 185px; top: -100px;">
            <div class="bg-white mt-40 px-4 py-3 rounded-lg shadow-md max-w-xs">
                <div class="flex items-center justify-between">
                    <span class="font-medium text-sm">Notificações</span>
                    <button class="bg-gray-200 p-2 rounded-full" @click="isActive = !isActive">
                        <svg class="h-3 w-3 fill-current" viewBox="0 0 20 20"><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"/></svg>
                    </button>
                </div>
                <div class="flex items-center mt-3 hover:bg-gray-100 rounded-lg px-1 py-1 cursor-pointer">
                    <div class="flex flex-shrink-0 ">
                        <img class="h-16 w-16 rounded-full" :src="getProfilePic">
                    </div>
                    <div class="ml-3 text-left">
                        <span class="font-medium text-sm">John Doe</span>
                        <p class="text-sm">reacted to your comment: "Comment..."</p>
                        <span class="text-sm text-blue font-semibold">Alguns segundos atrás</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import NotificationBell from 'vue-notification-bell'

export default ({
    name: "Notification",
    props: ["postData"],

    components: {
        NotificationBell 
    },
    computed: {
        getProfilePic() { 
            return require('@/assets/img/profile/' + this.$store.getters.UserId + '.jpg')
        }
    },
    data: () => ({
        isActive: false,
  }),
})
</script>
<style>

</style>
