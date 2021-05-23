<template>
  <div class="bg-lightgray border border-lightgray rounded-lg block w-full text-white lg:float-left max-w-xs">
        <div class="flex items-center px-4 py-3">
            <img class="h-12 w-12 rounded-full" :src="getProfilePic"/>
            <div class="ml-3">
              <span class="text-sm font-semibold antialiased block leading-tight">{{this.username}}</span>
              <h2>{{this.name}}</h2>
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
</template>

<script>
export default {
  name: 'SuggestedConection',
  data() {
    return {
      name: this.$store.getters.Username,
      username: this.$store.getters.Name,
    }
  },
  computed : {
    getProfilePic() { 
      return require('@/assets/img/profile/' + this.$store.getters.UserId + '.jpg')
    },
    /* getUsername(){
      this.name = this.$store.getters.Username
    },
    getName(){
      this.username = this.$store.getters.Name
    } */
  },
  methods: {
    
  }
}
</script>

<style>

</style>