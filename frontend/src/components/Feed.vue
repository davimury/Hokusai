<template>
  <div>
    <Header></Header>
    <main class="flex justify-between container h-screen w-full mx-auto">
      
      <div class="w-1/3 h-screen hidden lg:block"></div>
      <div
        id="posts"
        class="w-full md:w-4/5 lg:w-3/5 h-screen overflow-y-scroll p-3"
      >
      </div>

      <div id="right-bar" class="w-1/3 md:2/4 hidden lg:block h-screen p-3">
        <SuggestedConection></SuggestedConection>
      </div>
    </main>
    
    <!-- <my-upload field="img"
      @crop-success="cropSuccess"
      @crop-upload-success="cropUploadSuccess"
      @crop-upload-fail="cropUploadFail"
      v-model="show"
      :width="100"
      :height="100"
      langType="pt-br"
      url="/upload"
      :params="params"
      :headers="headers"
      img-format="png"></my-upload> -->
    <img :src="imgDataUrl">
    <div
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-if="isFirstLogin"
      >
      <div
          class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
        >
          <div
            class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
            aria-hidden="true"
          ></div>

          <span
            class="hidden sm:inline-block sm:align-middle sm:h-screen"
            aria-hidden="true"
            >&#8203;</span
          >
          <div
            class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
            v-on-clickaway="awayModalPost"
          >
          <div
            class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white"
          >
          <div
            class="relative shadow mx-auto h-24 w-24 border-purple-500 rounded-full overflow-hidden border-4"
          >
            <img
              class="object-cover w-full h-full"
              src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=200&q=80"
            />
          </div>
          <a class="btn" @click="toggleShow">set avatar</a>
          </div>
        </div>
    </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
//import myUpload from 'vue-image-crop-upload/upload-2.vue';
import Post from "./Post.vue";
import SuggestedConection from "./SuggestedConection.vue";
import axios from 'axios';

import Header from "./Header.vue";
import Footer from "./Footer.vue";
export default {
  name: "Feed",
  components: {
    Post,
    SuggestedConection,
    Header,
    Footer,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      show: false,
			params: {
				token: '123456798',
				name: 'avatar'
			},
			headers: {
				smail: '*_~'
			},
			imgDataUrl: '', // the datebase64 url of created image
      postsData: []
    };
  },
  computed : {
    isFirstLogin : function(){ 
      console.log(this.$store.getters.isFirstLogin)
      return this.$store.getters.isFirstLogin
      }
  },
  mounted () {
    axios.get('/v1/posts/').then( response => {
      this.postsData = response['data']
    })
  },
  methods: {
    logout: async function () {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    },
    awayModalPost: function () {
      this.showModalPost = false;
    },
    showPost: function (id) {
      this.showModalPost = true;
      console.log(id);
      //usar id para receber do backend o post relacionado
    },
    toggleShow() {
				this.show = !this.show;
			},
    cropSuccess(imgDataUrl, field){
				console.log('-------- crop success --------');
				this.imgDataUrl = imgDataUrl;
			},
			/**
			 * upload success
			 *
			 * [param] jsonData  server api return data, already json encode
			 * [param] field
			 */
			cropUploadSuccess(jsonData, field){
				console.log('-------- upload success --------');
				console.log(jsonData);
				console.log('field: ' + field);
			},
			/**
			 * upload fail
			 *
			 * [param] status    server api return error status, like 500
			 * [param] field
			 */
			cropUploadFail(status, field){
				console.log('-------- upload fail --------');
				console.log(status);
				console.log('field: ' + field);
			}
  },
  'pt-pt': {
		hint: 'Clique ou arraste o arquivo para a janela para carregar',
		loading: 'A processar...',
		noSupported: 'Browser não suportado, por favor utilize o Internet Explorer 10+ ou outro browser',
		success: 'Imagem carregada com sucesso',
		fail: 'Ocorreu um erro ao carregar a imagem',
		preview: 'Pré-visualização',
		btn: {
			off: 'Cancelar',
			close: 'Fechar',
			back: 'Voltar',
			save: 'Guardar'
		},
		error: {
			onlyImg: 'Por favor envie apenas imagens',
			outOfSize: 'A imagem excede o limite de tamanho suportado: ',
			lowestPx: 'O tamanho da imagem é muito pequeno. Tamanho mínimo: '
		}
	},
};
</script>

<style>
#dropBodyMenu {
  animation-duration: 0.5s;
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
