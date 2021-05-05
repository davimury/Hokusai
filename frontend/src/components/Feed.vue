<template>
  <div class="grid grid-cols-12 items-center text-white">

    <header class="fixed w-full">
      <nav class="w-full p-2 px-24 flex justify-between ">
        <div>
          <img class="w-60 inline-block" src="@/assets/img/logo-symb-nobg.svg">
        </div>

        <div class="relative inline-block w-1/4">
            <span  class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center">search</span>
            <input class="block p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500 w-full" placeholder="Pesquisar">
        </div>

        <div class=" text-center text-purple-500  text-3xl flex">

          <div  class="mr-5 hover:text-purple-600">
            <a href="#"><span class="material-icons">
            notifications
            </span></a>
          </div>
          <div  class="mr-5 hover:text-purple-600">
            <a href="#"><span class="material-icons">
            question_answer
            </span></a>
          </div>
          <div  class="mr-5 hover:text-purple-600">
            <a href="#"><span class="material-icons">
            bookmark
            </span></a>
          </div>
          <div class="flex items-center">
            <img class="h-8 w-8 rounded-full" src="https://picsum.photos/id/1027/150/150"/>
          </div>
        </div>
      </nav>
    </header>

    <div class="lg:col-span-4 hidden lg:block">
      1
    </div>
    <div class="lg:col-span-4 col-span-12 p-3">
      
        <div class="bg-lightgray border border-lightgray rounded-lg block w-full">
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
            <span><span class="text-sm antialiased leading-tight">Testando essa legenda carai</span></span>
          </div>
        </div>
      
    </div>
    <div class="lg:col-span-4 hidden lg:block">
      3
    </div>
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
      feedback: null
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

<style></style>
