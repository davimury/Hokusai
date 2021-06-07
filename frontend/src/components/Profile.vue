<template>
  <main class="h-screen" @mousemove="mouseMove">
    <Header></Header>
    <div
      class="bg-lightgray text-white pb-6 w-full justify-center items-center overflow-visible md:max-w-4xl rounded-lg shadow-sm mx-auto"
    >
      <div class="relative h-40">
        <img class="absolute h-full w-full object-cover" :src="getHeader" />
        <button
          v-if="this.$route.params.username == this.$store.getters.Username"
          class="focus:outline-none"
          v-on:click="modalHeader = !modalHeader"
        >
          <span
            class="material-icons z-10 absolute bottom-2 right-3 text-purple-500 hover:text-purple-600"
          >
            photo_camera
          </span>
        </button>
      </div>
      <div
        class="relative shadow mx-auto h-24 w-24 -my-12 border-lightgray rounded-full overflow-hidden border-4"
      >
        <img class="object-cover w-full h-full" :src="getProfilePic" />
      </div>
      <div class="flex justify-center ml-11 mt-6 relative">
        <button
          class="focus:outline-none text-center bg-lightgray rounded-full p-1"
          v-if="this.$route.params.username == this.$store.getters.Username"
          v-on:click="modalProfile = !modalProfile"
        >
          <span class="material-icons text-purple-500 hover:text-purple-600">
            photo_camera
          </span>
        </button>
      </div>
      <div>
        <div class="text-center">
          <h1 class="text-lg text-center font-semibold inline-block">
            {{ this.name }}
          </h1>
          <button
            class="ml-1 -mt-1 absolute text-purple-500 hover:text-purple-600"
          >
            <span class="material-icons text-lg"> edit </span>
          </button>
        </div>
        <div class="flex justify-center text-gray-500">
          <p class="mx-1">
            <span class="font-medium">{{ this.postsCounter }}</span> Posts
          </p>
          <p class="mx-1"><span class="font-medium">150</span> Conexões</p>
        </div>
        <div
          v-if="this.username != this.$store.getters.Username"
          class="flex justify-center text-gray-500"
        >
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
      <div
        class="mt-6 pt-3 flex flex-wrap mx-6 border-t border-lightergray w-100"
      >
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:text-purple-600 hover:border-purple-600 cursor-pointer"
          v-for="userTag in userTags"
          :key="userTag"
        >
          {{ userTag }}
        </div>
        <button
          class="ml-1 -mt-1 text-purple-500 hover:text-purple-600 -mt-3"
          @click="editTags(true)"
        >
          <span class="material-icons text-lg"> edit </span>
        </button>
      </div>
      <transition
        mode="out-in"
        enter-active-class="animate__animated animate__fadeIn"
        leave-active-class="animate__animated animate__fadeOut"
      >
        <div v-if="isEditingTags" class="pt-3 mx-6 w-100 overflow-visible">
          <v-select
            taggable
            multiple
            push-tags
            name="tags"
            label="name"
            @option:created="addTag"
            @input="appendTag"
            :options="recomendedTags"
          ></v-select>
          <div class="flex justify-end mt-2">
            <button
              @click="editTags(false)"
              class="rounded-lg border border-purple-500 hover:border-purple-600 focus:outline-none text-white p-1 px-3 mx-1 mt-2"
            >
              Cancelar
            </button>
            <button
              class="rounded-lg border border-purple-500 hover:border-purple-600 bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-1 px-3 mx-1 mt-2"
              @click="editTags(false)"
            >
              Salvar
            </button>
          </div>
        </div>
      </transition>
    </div>
    <div
      class="pb-6 mt-6 w-full justify-center items-center overflow-hidden md:max-w-4xl mx-auto grid grid-cols-3 gap-1"
      v-if="posts.length > 0"
    >
      <div
        
        v-for="post in posts"
        :key="post.post_id"
        class="bg-lightgray post-card cursor-pointer"
        @click="showPost(post)"
      >
        <img
          :src="require(`@/assets/img/posts/${post.slides[0]}`)"
          alt=""
          class="media"
        />
      </div>
    </div>
    <div
    class="pb-6 mt-6 w-full justify-center items-center overflow-hidden mx-auto text-white text-center md:max-w-4xl mx-auto"
    v-else>
    <div class="box">
  <div id="ghost" class="box__ghost">
    <div class="symbol"></div>
    <div class="symbol"></div>
    <div class="symbol"></div>
    <div class="symbol"></div>
    <div class="symbol"></div>
    <div class="symbol"></div>
    
    <div class="box__ghost-container">
      <div class="box__ghost-eyes" :style="style">
        <div class="box__eye-left"></div>
        <div class="box__eye-right"></div>
      </div>
      <div class="box__ghost-bottom">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <div class="box__ghost-shadow"></div>
  </div>
  
  <div class="box__description">
    <div class="box__description-container">
      <div class="box__description-title">Whoops!</div>
      <div class="box__description-text">Nenhum post foi encontrado!!</div>
    </div>
  </div>
  
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
            class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
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
            class="inline-block align-bottom overflow-hidden transform transition-all  sm:align-middle "
          >
            <div
              class="bg-lightgray border border-lightgray rounded-lg block w-full text-white py-10"
              v-on-clickaway="awayModalHeader"
            >
              
              <vue-croppie
                ref="croppieRef"
                :enableExif="true"
                :enableOrientation="true"
                :boundary="{ width: 896, height: 360 }"
                :viewport="{ width: 896, height: 360, type: 'rectangle' }"
                
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
            class="inline-block align-bottom overflow-hidden transform transition-all  sm:align-middle "
          >
            <div
              class="bg-lightgray border border-lightgray rounded-lg block w-full text-white py-8"
              v-on-clickaway="awayModalProfile"
            >
              <vue-croppie
                ref="croppieRef"
                :enableExif="true"
                :enableOrientation="true"
                :boundary="{ width: 300, height: 300 }"
                :viewport="{ width: 250, height: 250, type: 'circle' }"
                
              ></vue-croppie>
              <input type="file" @change="croppieProfile" />
              <button
                class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mt-4 self-start"
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
import axios from "axios";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

export default {
  name: "Profile",
  components: {
    Header,
    Post,
    Footer,
    vSelect,
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
      name: "",
      user_id: "",
      username: this.$route.params.username,
      userTags: [],
      postData: {},
      postsCounter: 0,
      profilePic: "",
      modalPost: false,
      modalProfile: false,
      modalHeader: false,
      croppieImage: "",
      cropped: null,
      croppieHeaderState: false,
      croppieProfileState: false,
      imgDataUrl: "", // the datebase64 url of created image
      isEditingTags: false,
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      xAxis: 0,
      yAxis: 0,
    };
  },
  mounted() {
    axios.get(`/profile/${this.$route.params.username}/`).then((response) => {
      this.posts = response["data"]["posts"];
      this.userTags = response["data"]["tags"];
      this.postsCounter = response["data"]["posts_count"];
      this.name = response["data"]["name"];
      this.user_id = response["data"]["user_id"];
    });
  },
  computed: {
    getProfilePic() {
      try {
        return require("@/assets/img/profile/" + this.user_id + ".jpg");
      } catch {
        return require("@/assets/img/profile/default.jpg");
      }
    },
    getHeader() {
      try {
        return require("@/assets/img/header/" + this.user_id + ".jpg");
      } catch {
        return require("@/assets/img/header/default.jpg");
      }
    },
    style () {
     return { transform: 'translate('+ this.xAxis +'%,-'+ this.yAxis +'%)'}
    },
  },
  methods: {
    editTags: function (isEditing) {
      this.isEditingTags = isEditing;
    },
    awayModalPost: function () {
      this.modalPost = false;
    },
    awayModalHeader: function () {
      console.log('t')
      this.modalHeader = false;
      this.croppieHeaderState = true;
    },
    awayModalProfile: function () {
      this.modalProfile = false;
      this.croppieProfileState = true;
    },
    showPost: function (post) {
      this.postData = post;
      this.modalPost = true;
    },
    getPostData: function () {
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
    changeProfile: async function () {
      let options = {
        type: "base64",
        size: { width: 250, height: 250 },
        format: "jpeg",
      };
      await this.$refs.croppieRef.result(options, (output) => {
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
    changeHeader: async function () {
      let options = {
        type: "base64",
        size: { width: 896, height: 360 },
        format: "jpeg",
      };
      await this.$refs.croppieRef.result(options, (output) => {
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
    requestConnection: async function () {
      await axios({
        method: "post",
        url: `/profile/${this.username}/connect`,
      });
    },
    mouseMove: function (event) {
      var pageX = this.windowWidth;
      var pageY = this.windowHeight ;
      var mouseY=0;
      var mouseX=0;

      //verticalAxis
      mouseY = event.clientY;
      this.yAxis = (pageY-mouseY)/pageY*100; 
      //horizontalAxis
      mouseX = event.clientX / -pageX;
      this.xAxis = -mouseX * 50 - 50;
    },
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

.box {
  min-height: 350px;
  height: 100%;
  position: relative;
}
.box .box__ghost {
  padding: 15px 25px 25px;
  position: absolute;
  left: 50%;
  top: 30%;
  transform: translate(-50%, -30%);
}
.box .box__ghost .symbol:nth-child(1) {
  opacity: 0.2;
  animation: shine 4s ease-in-out 3s infinite;
}
.box .box__ghost .symbol:nth-child(1):before, .box .box__ghost .symbol:nth-child(1):after {
  content: "";
  width: 12px;
  height: 4px;
  background: #fff;
  position: absolute;
  border-radius: 5px;
  bottom: 65px;
  left: 0;
}
.box .box__ghost .symbol:nth-child(1):before {
  transform: rotate(45deg);
}
.box .box__ghost .symbol:nth-child(1):after {
  transform: rotate(-45deg);
}
.box .box__ghost .symbol:nth-child(2) {
  position: absolute;
  left: -5px;
  top: 30px;
  height: 18px;
  width: 18px;
  border: 4px solid;
  border-radius: 50%;
  border-color: #fff;
  opacity: 0.2;
  animation: shine 4s ease-in-out 1.3s infinite;
}
.box .box__ghost .symbol:nth-child(3) {
  opacity: 0.2;
  animation: shine 3s ease-in-out 0.5s infinite;
}
.box .box__ghost .symbol:nth-child(3):before, .box .box__ghost .symbol:nth-child(3):after {
  content: "";
  width: 12px;
  height: 4px;
  background: #fff;
  position: absolute;
  border-radius: 5px;
  top: 5px;
  left: 40px;
}
.box .box__ghost .symbol:nth-child(3):before {
  transform: rotate(90deg);
}
.box .box__ghost .symbol:nth-child(3):after {
  transform: rotate(180deg);
}
.box .box__ghost .symbol:nth-child(4) {
  opacity: 0.2;
  animation: shine 6s ease-in-out 1.6s infinite;
}
.box .box__ghost .symbol:nth-child(4):before, .box .box__ghost .symbol:nth-child(4):after {
  content: "";
  width: 15px;
  height: 4px;
  background: #fff;
  position: absolute;
  border-radius: 5px;
  top: 10px;
  right: 30px;
}
.box .box__ghost .symbol:nth-child(4):before {
  transform: rotate(45deg);
}
.box .box__ghost .symbol:nth-child(4):after {
  transform: rotate(-45deg);
}
.box .box__ghost .symbol:nth-child(5) {
  position: absolute;
  right: 5px;
  top: 40px;
  height: 12px;
  width: 12px;
  border: 3px solid;
  border-radius: 50%;
  border-color: #fff;
  opacity: 0.2;
  animation: shine 1.7s ease-in-out 7s infinite;
}
.box .box__ghost .symbol:nth-child(6) {
  opacity: 0.2;
  animation: shine 2s ease-in-out 6s infinite;
}
.box .box__ghost .symbol:nth-child(6):before, .box .box__ghost .symbol:nth-child(6):after {
  content: "";
  width: 15px;
  height: 4px;
  background: #fff;
  position: absolute;
  border-radius: 5px;
  bottom: 65px;
  right: -5px;
}
.box .box__ghost .symbol:nth-child(6):before {
  transform: rotate(90deg);
}
.box .box__ghost .symbol:nth-child(6):after {
  transform: rotate(180deg);
}
.box .box__ghost .box__ghost-container {
  background: #fff;
  width: 100px;
  height: 100px;
  border-radius: 100px 100px 0 0;
  position: relative;
  margin: 0 auto;
  animation: upndown 3s ease-in-out infinite;
}
.box .box__ghost .box__ghost-container .box__ghost-eyes {
  position: absolute;
  left: 35%;
  top: 45%;
  height: 12px;
  width: 70px;
}
.box .box__ghost .box__ghost-container .box__ghost-eyes .box__eye-left {
  width: 12px;
  height: 12px;
  background: #332F63;
  border-radius: 50%;
  margin: 0 10px;
  position: absolute;
  left: 0;
}
.box .box__ghost .box__ghost-container .box__ghost-eyes .box__eye-right {
  width: 12px;
  height: 12px;
  background: #332F63;
  border-radius: 50%;
  margin: 0 10px;
  position: absolute;
  right: 0;
}
.box .box__ghost .box__ghost-container .box__ghost-bottom {
  display: flex;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
}
.box .box__ghost .box__ghost-container .box__ghost-bottom div {
  flex-grow: 1;
  position: relative;
  top: -10px;
  height: 20px;
  border-radius: 100%;
  background-color: #fff;
}
.box .box__ghost .box__ghost-container .box__ghost-bottom div:nth-child(2n) {
  top: -12px;
  margin: 0 0px;
  border-top: 15px solid #332F63;
  background: transparent;
}
.box .box__ghost .box__ghost-shadow {
  height: 20px;
  box-shadow: 0 50px 15px 5px #332F63;
  border-radius: 50%;
  margin: 0 auto;
  animation: smallnbig 3s ease-in-out infinite;
}
.box .box__description {
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
}
.box .box__description .box__description-container {
  color: #fff;
  text-align: center;
  width: 200px;
  font-size: 16px;
  margin: 0 auto;
}
.box .box__description .box__description-container .box__description-title {
  font-size: 24px;
  letter-spacing: 0.5px;
}
.box .box__description .box__description-container .box__description-text {
  color: #8C8AA7;
  line-height: 20px;
  margin-top: 20px;
}
.box .box__description .box__button {
  display: block;
  position: relative;
  background: #FF5E65;
  border: 1px solid transparent;
  border-radius: 50px;
  height: 50px;
  text-align: center;
  text-decoration: none;
  color: #fff;
  line-height: 50px;
  font-size: 18px;
  padding: 0 70px;
  white-space: nowrap;
  margin-top: 25px;
  transition: background 0.5s ease;
  overflow: hidden;
  -webkit-mask-image: -webkit-radial-gradient(white, black);
}
.box .box__description .box__button:before {
  content: "";
  position: absolute;
  width: 20px;
  height: 100px;
  background: #fff;
  bottom: -25px;
  left: 0;
  border: 2px solid #fff;
  transform: translateX(-50px) rotate(45deg);
  transition: transform 0.5s ease;
}
.box .box__description .box__button:hover {
  background: transparent;
  border-color: #fff;
}
.box .box__description .box__button:hover:before {
  transform: translateX(250px) rotate(45deg);
}

@keyframes upndown {
  0% {
    transform: translateY(5px);
  }
  50% {
    transform: translateY(15px);
  }
  100% {
    transform: translateY(5px);
  }
}
@keyframes smallnbig {
  0% {
    width: 90px;
  }
  50% {
    width: 100px;
  }
  100% {
    width: 90px;
  }
}
@keyframes shine {
  0% {
    opacity: 0.2;
  }
  25% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.2;
  }
  100% {
    opacity: 0.2;
  }
}
</style>
