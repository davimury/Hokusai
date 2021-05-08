<template>
<div class="overflow-hidden ">

    <header class="sticky w-screen z-20 bg-darkgray ">
      <nav class="w-full p-2 px-24 flex justify-between ">
        <div>
          <img class="w-60 inline-block" src="@/assets/img/logo-symb-nobg.svg">
        </div>

        <div class="relative inline-block w-1/4">
            <span  class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center">search</span>
            <input class="block p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500 w-full text-white" placeholder="Pesquisar">
        </div>

        <div class=" text-center text-purple-500   flex">

          <div  class="mr-5 hover:text-purple-600 text-3xl relative">
            <button >
              <span class="material-icons">
              notifications
              <div style="width: .5rem; height: .5rem" class="bg-red-600 rounded-full -ml-1 float-right z-10"></div>
              </span>
            </button>
            
          </div>
          <div  class="mr-5 hover:text-purple-600 text-3xl">
            <a href="#"><span class="material-icons">
            queue
            </span></a>
          </div>
          <div  class="mr-5 hover:text-purple-600 text-3xl">
            <a href="#"><span class="material-icons">
            question_answer
            </span></a>
          </div>
          <div  class="mr-5 hover:text-purple-600 text-3xl">
            <a href="#"><span class="material-icons">
            bookmark
            </span></a>
          </div>
         
            <div class="relative">
              <button v-on-clickaway="away" v-on:click="show = !show" class="flex items-center outline-none focus:outline-none  rounded-full" :class="{ 'focus:ring-2 focus:ring-purple-500': show === true }">
                <img class="h-8 w-8 rounded-full " src="https://picsum.photos/id/1027/150/150"/>
              </button>
              <!-- Dropdown Body -->
              <transition 
                    mode="out-in"
                    enter-active-class="animate__animated animate__flipInX"
                    leave-active-class="animate__animated animate__flipOutX"
                >

              <div v-if="show" id="dropBodyMenu" class="z-0 absolute right-0 w-40 mt-2 py-2 bg-lightgray border border-lightgray rounded-lg text-white">   
                <ul class="text-left">
                  <li class="my-2 hover:text-gray-300"><a href="#" class="  px-4 py-2">    
                Perfil
                </a></li>
                  <li class="my-2 hover:text-gray-300"><a href="#" class=" px-4 py-2">Configurações</a></li>
                  <li class="my-2 hover:text-gray-300"><a href="#" class=" px-4 py-2">    
                Logout
                </a></li>
                </ul>
            </div>
            </transition>
            <!-- // Dropdown Body -->
            </div>
            
        </div>
      </nav>
    </header>


  <div class="flex justify-between container h-screen w-full mx-auto">

    <div class="w-1/3 h-screen hidden lg:block">
    </div>

    <div id="posts" class="w-full md:w-4/5 lg:w-3/5 h-screen overflow-y-scroll p-3 ">
      <div class="w-full flex flex-col">

        <Post></Post>

      </div>
      
    </div>

    <div id="right-bar" class="w-1/3 md:2/4 hidden lg:block h-screen p-3">

      <SuggestedConection></SuggestedConection>

    </div>
  
  </div >
</div>
</template>

<script>
import { directive as onClickaway } from 'vue-clickaway';
import Post from './Post.vue';
import SuggestedConection from './SuggestedConection.vue';
export default {
    name: 'Feed',
    components: {
      Post,
        SuggestedConection
    },
    directives: {
      onClickaway: onClickaway,
    },
    data() {
      return {
      show: false
      }
    },
    methods: {
        logout: async function (){
            await this.$store.dispatch('LogOut')
            this.$router.push('/login')
        },
        away: function() {
        this.show = false
    }
    }
};
</script>

<style>
#dropBodyMenu{
  animation-duration: .5s;
}
#left-bar::-webkit-scrollbar {
	width: 0px;
	background: transparent; /* make scrollbar transparent */
}
#posts::-webkit-scrollbar {
	width: 0px;
	background: transparent; /* make scrollbar transparent */
}
#right-bar::-webkit-scrollbar {
	width: 0px;
	background: transparent; /* make scrollbar transparent */
}

</style>
