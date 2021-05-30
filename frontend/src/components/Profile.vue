<template>
  <main class="h-screen">
    <Header></Header>
    <div
      class="bg-lightgray text-white pb-6 w-full justify-center items-center overflow-hidden md:max-w-4xl rounded-lg shadow-sm mx-auto "
    >
      <div class="relative h-40">
        <img
          class="absolute h-full w-full object-cover"
          :src="getHeader"
        />
        <button v-if="this.$route.params.username == this.$store.getters.Username" class="focus:outline-none" v-on:click="modalHeader = !modalHeader">
          <span
            class="material-icons z-10 absolute bottom-2 right-3 text-purple-500 hover:purple-600"
          >
            photo_camera
          </span>
        </button>
      </div>
      <div
        class="relative shadow mx-auto h-24 w-24 -my-12 border-lightgray rounded-full overflow-hidden border-4"
      >
        <img
          class="object-cover w-full h-full"
          :src="getProfilePic"
        />
        
      </div>
      <div class="flex justify-center ml-11 mt-6 relative">
      <button class="focus:outline-none text-center bg-lightgray rounded-full p-1" v-if="this.$route.params.username == this.$store.getters.Username" v-on:click="modalProfile = !modalProfile">
          <span
            class="material-icons text-purple-500 hover:purple-600"
          >
            photo_camera
          </span>
        </button>
      </div>
      <div class="mt-4">
        <h1 class="text-lg text-center font-semibold">{{this.name}}</h1>
        <div class="flex justify-center text-gray-500">
          <p class="mx-1"><span class="font-medium">{{this.postsCounter}}</span> Posts</p>
          <p class="mx-1"><span class="font-medium">150</span> Conexões</p>
        </div>
        <div v-if="this.username != this.$store.getters.Username" class="flex justify-center text-gray-500">
          <button
            @click="requestConnection"
            class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2"
          >
            Conectar
          </button>
          <button
            class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2"
          >
            Mensagem
          </button>
        </div>
      </div>
      <div class="mt-6 pt-3 flex flex-wrap mx-6 border-t border-lightergray">
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:text-purple-600 hover:border-purple-600 cursor-pointer"
          v-for="userTag in userTags"
          :key="userTag"
        >
          {{ userTag }}
        </div>
      </div>
    </div>
    <div
      class="pb-6 mt-6 w-full justify-center items-center overflow-hidden md:max-w-4xl mx-auto grid grid-cols-3 gap-1"
    >
      <div
        v-for="post in posts"
        :key="post.post_id"
        class="bg-lightgray post-card cursor-pointer"
        @click="showPost(post)"
      >
        <img :src="require(`@/assets/img/posts/${post.slides[0]}`)" alt="" class="media" />
      </div>
    </div>

    <transition
      mode="out-in"
      enter-active-class="animate__animated animate__fadeIn"
      leave-active-class="animate__animated animate__fadeOut"
    >
      <div
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-if="modalPost"
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
            class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full  "
            v-on-clickaway="awayModalPost"
          >
            <Post :postData="this.postData"></Post>
          </div>
        </div>
      </div>
    </transition>
    <transition
      mode="out-in"
      enter-active-class="animate__animated animate__fadeIn"
      leave-active-class="animate__animated animate__fadeOut"
    >
      <div
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-if="modalHeader"
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
            class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:w-6/12"
            
          >
          <div
              class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white py-10"
            >
             <vue-dropzone
                  id="dropzone"
                  :options="dropzoneOptions"
                  class="mb-5"
                  @vdropzone-success="croppieHeader"
                  :style="{display: !croppieHeaderState ? 'block' : 'none'}"
                ></vue-dropzone>
            <vue-croppie
                ref="croppieRef"
                :enableExif="true"
                :enableOrientation="true"
                :boundary="{ width: 896, height: 360 }"
                :viewport="{ width: 896, height: 360, type: 'rectangle' }"
                :style="{display: croppieHeaderState ? 'block' : 'none'}"
              ></vue-croppie>
            <button
              class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-4 self-start"
              @click="changeHeader"
            >
              Atualizar
            </button>
          </div>
          </div>
        </div>
      </div>
    </transition>
    <transition
      mode="out-in"
      enter-active-class="animate__animated animate__fadeIn"
      leave-active-class="animate__animated animate__fadeOut"
    >
      <div
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-if="modalProfile"
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
            class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:w-3/12"
            
          >
          <div
              class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white py-10"
            >
            <vue-dropzone
                  ref="headerRef"
                  id="dropzone"
                  :options="dropzoneOptions"
                  class="mb-5"
                  @vdropzone-success="croppieProfile"
                  :style="{display: !croppieProfileState ? 'block' : 'none'}"
                ></vue-dropzone>
            <vue-croppie
                ref="croppieRef"
                :enableExif="true"
                :enableOrientation="true"
                :boundary="{ width: 300, height: 300 }"
                :viewport="{ width: 250, height: 250, type: 'circle' }"
                :style="{display: croppieProfileState ? 'block' : 'none'}"
              ></vue-croppie>
            <button
              class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-4 self-start"
              @click="changeProfile"
            >
              Atualizar
            </button>
          </div>
          </div>
        </div>
      </div>
    </transition>
    <Footer></Footer>
  </main>
</template>

<script>
import Header from "./Header.vue";
import Post from "./Post.vue";
import Footer from "./Footer.vue";
import { directive as onClickaway } from "vue-clickaway";
import vue2Dropzone from "vue2-dropzone";
import "../assets/css/dropzone.css";
import axios from 'axios';

export default {
  name: "Profile",
  components: {
    Header,
    Post,
    Footer,
    vueDropzone: vue2Dropzone,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        thumbnailWidth: 140,
        maxFilesize: 5,
        headers: { "My-Awesome-Header": "header value" },
        dictDefaultMessage:
          "<span class='material-icons text-purple-500 text-4xl'>cloud_upload</span>",
        addRemoveLinks: true,
        dictFileTooBig:
          "Arquivo muito grande. Tamanho máximo {{maxFilesize}}MB",
        dictInvalidFileType: "Arquivo inválido",
        dictRemoveFile: "<span class='material-icons'>close</span>",
        dictMaxFilesExceeded:
          "Número máximo de arquivos permitidos: {{maxFiles}}",
        maxFiles: 10,
      },
      posts: [],
      name: '',
      user_id: '',
      username: this.$route.params.username,
      userTags: [],
      postData: {},
      postsCounter: 0,
      profilePic: '',
      modalPost: false,
      modalProfile: false,
      modalHeader: false,
      croppieImage: "",
      cropped: null,
      croppieHeaderState: false,
      croppieProfileState: false,
      imgDataUrl: "", // the datebase64 url of created image
    };
  },
  mounted() {
    axios.get(`/profile/${this.$route.params.username}/`).then( response => {
      this.posts = response['data']['posts']
      this.userTags = response['data']['tags']
      this.postsCounter = response['data']['posts_count']
      this.name = response['data']['name']
      this.user_id = response['data']['user_id']
    })
  },
  computed : {
    getProfilePic() { 
      try{
        return require('@/assets/img/profile/' + this.user_id + '.jpg')
      } 
      catch{
        return require('@/assets/img/profile/1.jpg')
      }
    },
    getHeader() { 
      try{
        return require('@/assets/img/header/' + this.user_id + '.jpg')
      } 
      catch{
        return require('@/assets/img/header/1.jpg')
      }
    }
  },
  methods: {
    awayModalPost: function () {
      this.modalPost = false;
    },
    awayModalHeader: function () {
      this.modalHeader = false;
      this.coppieState = true;
    },
    awayModalProfile: function () {
      this.modalProfile = false;
      this.coppieState = true;
    },
    showPost: function (post) {
      this.postData = post;
      this.modalPost = true;
    },
    getPostData: function(){
      return this.postData;
    },
    croppieHeader(e) {
      this.$refs.croppieRef.bind({
        url: e.dataURL,
      });
      
      this.croppieHeaderState = true;
    },
    croppieProfile(e) {
      this.$refs.croppieRef.bind({
        url: e.dataURL,
      });
      
      this.croppieProfileState = true;
    },
    changeProfile: async function() {
      let options = {
        type: 'base64',
        size: { width: 250, height: 250 },
        format: 'jpeg'
      };
      await this.$refs.croppieRef.result(options, output => {
        this.cropped = this.croppieImage = output;
      });

      await axios({
        method: "post",
        url: "/profile/image",
        data: {
          base: this.croppieImage,
        },
      });
    },
    changeHeader: async function() {
      let options = {
        type: 'base64',
        size: { width: 896, height: 360 },
        format: 'jpeg'
      };
      await this.$refs.croppieRef.result(options, output => {
        this.cropped = this.croppieImage = output;
      });

      await axios({
        method: "post",
        url: "/profile/header",
        data: {
          base: this.croppieImage,
        },
      });
    },
    requestConnection: async function() {
      await axios({
        method: "post",
        url: `/profile/${this.username}/connect`,
      });
      
    }
  },
};
</script>

<style scoped>
.post-card {
  aspect-ratio: 1/1;
  position: relative;
  width: 100%;
}
.media {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
.animate__animated.animate__fadeIn {
  --animate-duration: 0.3s;
}
.animate__animated.animate__fadeOut {
  --animate-duration: 0.3s;
}
</style>
