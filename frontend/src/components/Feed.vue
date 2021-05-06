<template>
<div class="overflow-hidden ">

    <header class="sticky w-screen z-20 bg-darkgray ">
      <nav class="w-full p-2 px-24 flex justify-between ">
        <div>
          <img class="w-60 inline-block" src="@/assets/img/logo-symb-nobg.svg">
        </div>

        <div class="relative inline-block w-1/4">
            <span  class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center">search</span>
            <input class="block p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500 w-full" placeholder="Pesquisar">
        </div>

        <div class=" text-center text-purple-500   flex">

          <div  class="mr-5 hover:text-purple-600 text-3xl">
            <a href="#"><span class="material-icons">
            notifications
            </span></a>
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
              <button v-on:click="show = !show" class="flex items-center outline-none focus:outline-none">
                <img class="h-8 w-8 rounded-full" src="https://picsum.photos/id/1027/150/150"/>
              </button>
              <!-- Dropdown Body -->
              <transition 
                    mode="out-in"
                    enter-active-class="animate__animated animate__flipInX"
                    leave-active-class="animate__animated animate__flipOutX"
                >

              <div v-if="show" id="dropBodyMenu" class="z-0 absolute right-0 w-40 mt-2 py-2 bg-lightgray border border-lightgray rounded-lg text-white">   
                <ul>
                  <li><a href="#" class=" px-4 py-2">    
                Perfil
                </a></li>
                  <li><a href="#" class=" px-4 py-2">Configurações</a></li>
                  <li><a href="#" class=" px-4 py-2">    
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

    <div id="posts" class="w-2/5 h-screen overflow-y-scroll p-3 ">
      <div class="w-full flex flex-col">

        <div class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white">
          <div class="flex items-center px-4 py-3">
            <img class="h-8 w-8 rounded-full" src="https://picsum.photos/id/1027/150/150"/>
            <div class="ml-3 ">
              <span class="text-sm font-semibold antialiased block leading-tight">8fact</span>
            </div>
          </div>
          <div >
            <carousel :per-page="1" :mouse-drag="true" :centerMode="true" :paginationPosition="'bottom'" :paginationActiveColor="'#8B5CF6'" >
              <slide class="m-auto">
                <img src="https://picsum.photos/id/244/900/900"/>
                
              </slide>
              <slide class="m-auto">
                <img src="https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"/>
                
              </slide>
              <slide class="m-auto">
                <img src="https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80"/>
              </slide>
              <slide class="m-auto">
                Slide 4 Content
              </slide>
              <slide class="m-auto">
                Slide 5 Content
              </slide>
            </carousel>
            
          </div>
          <div class="flex items-center justify-between mx-4 mt-3 mb-2 text-purple-500">
            <div class="flex gap-5">
              
            </div>
            <div class="flex ">
              <span class="material-icons text-3xl">
              bookmark_border
              </span>
            </div>
          </div>
          <div class="font-semibold text-sm mx-4 mt-2 mb-4">92,372 likes</div>
          <div class="mx-4 mt-2 mb-4">
            <span class="text-sm font-semibold antialiased leading-tight">8fact </span>
            <span><span class="text-sm antialiased leading-tight">Testando essa legenda carai 2</span></span>
          </div>
        </div>

      </div>
      
    </div>

    <div id="right-bar" class="w-1/3 hidden lg:block h-screen p-3">

      <div class="bg-lightgray border border-lightgray rounded-lg block w-9/12  text-white float-left ml-3">
        <div class="flex items-center px-4 py-3">
            <img class="h-12 w-12 rounded-full" src="https://picsum.photos/id/1027/150/150"/>
            <div class="ml-3">
              <span class="text-sm font-semibold antialiased block leading-tight">8fact</span>
              <h2>Christiano Mafra</h2>
            </div>
          </div>
          <div class="flex flex-col px-4 py-3 ">
            <h1 class="mb-5">Sugestões de conexão</h1>
            
            <div class="flex items-center mb-3 w-100">
            <img class="h-10 w-10 rounded-full " src="https://picsum.photos/id/1027/150/150"/>
            <div class="ml-3 w-full">
              <span class="text-sm font-semibold antialiased block leading-tight">8fact</span>
              <h2>Christiano Mafra</h2>
              
            </div>
            <div class="text-center w-full">
              <a class="ml-5 text-purple-500 hover:text-purple-600" href="#">Conectar</a>
            </div>
          </div>
            <div class="flex items-center mb-3 w-100">
            <img class="h-10 w-10 rounded-full " src="https://picsum.photos/id/1027/150/150"/>
            <div class="ml-3 w-full">
              <span class="text-sm font-semibold antialiased block leading-tight">8fact</span>
              <h2>Christiano Mafra</h2>
            </div>
            <div class="text-center w-full">
              <a class="ml-5 text-purple-500 hover:text-purple-600" href="#">Conectar</a>
            </div>
          </div>
            <div class="flex items-center mb-3 w-100">
            <img class="h-10 w-10 rounded-full " src="https://picsum.photos/id/1027/150/150"/>
            <div class="ml-3 w-full">
              <span class="text-sm font-semibold antialiased block leading-tight">8fact</span>
              <h2>Christiano Mafra</h2>
              
            </div>
            <div class="text-center w-full">
              <a class="ml-5 text-purple-500 hover:text-purple-600" href="#">Conectar</a>
            </div>
          </div>
          <a href="#" class="mt-2 border-t border-lightergray pt-2">Ver mais</a>
          </div>
      </div>

    </div>
  
  </div >
</div>
</template>

<script>
import { VueFeedbackReaction } from 'vue-feedback-reaction';

export default {
    name: 'Feed',
    components:{
      VueFeedbackReaction
    },
    data() {
      return {
      feedback: null,
      show: false
      }
    },
    methods: {
        logout: async function (){
            await this.$store.dispatch('LogOut')
            this.$router.push('/login')
        },
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
