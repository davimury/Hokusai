<template>
  <div>
    <Header></Header>
    <main class="flex justify-between container h-screen w-full mx-auto">
      <div class="w-1/3 h-screen hidden lg:block"></div>
      <div
        
        class="w-full md:w-4/5 lg:w-3/5 h-screen p-3"
      >
        <div class="w-full flex justify-center gap-5 bg-darkgray sticky top-0">
          <button
            class="text-white border-b-2 hover:border-purple-600 focus:outline-none"
            @click="changeFeedType(1)"
            :class="feedType == 1 ? 'border-purple-500' : 'border-lightergray'"
          >
            Seguindo
          </button>
          <button
            class="text-white border-b-2 hover:border-purple-600 focus:outline-none"
            @click="changeFeedType(2)"
            :class="feedType == 2 ? 'border-purple-500' : 'border-lightergray'"
          >
            Recomendados
          </button>
        </div>
        <div
          v-if="feedType == 1"
          class="overflow-y-scroll w-full flex flex-col posts h-100"
        >
          <Post
            v-for="postData in postsData"
            :key="postData.post_id"
            :postData="postData"
          ></Post>
        </div>
        <div
          v-if="feedType == 2"
          class="overflow-y-scroll w-full flex flex-col posts h-100"
        >
        
          <Post
            v-for="postData in postsData"
            :key="postData.post_id"
            :postData="postData"
          ></Post>
        </div>
      </div>

      <div id="right-bar" class="w-1/3 md:2/4 hidden lg:block h-screen p-3">
        <SuggestedConection></SuggestedConection>
      </div>
    </main>
    <img :src="imgDataUrl" />
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
            <form-wizard @on-complete="onComplete">
              <tab-content
                title="Escolha sua foto de perfil"
                :before-change="crop"
              >
                <vue-croppie
                  ref="croppieRef"
                  :enableExif="true"
                  :enableOrientation="true"
                  :boundary="{ width: 300, height: 300 }"
                  :viewport="{ width: 250, height: 250, type: 'circle' }"
                ></vue-croppie>
                <input type="file" @change="croppie" />
              </tab-content>
              <tab-content title="Escolha categorias que você tem interesse">
                <div class="flex flex-wrap content-center justify-center">
                  <div
                    class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
                    v-for="tag in recomendedTags"
                    :key="tag.id"
                    :id="tag.id"
                    @click="select(tag, $event)"
                  >
                    {{ tag.name }}
                  </div>
                </div>
              </tab-content>
            </form-wizard>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import Post from "./Post.vue";
import { FormWizard, TabContent } from "vue-form-wizard";
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import SuggestedConection from "./SuggestedConection.vue";
import axios from "axios";

import Header from "./Header.vue";
import Footer from "./Footer.vue";
import { mapActions } from "vuex";

export default {
  name: "Feed",
  components: {
    Post,
    SuggestedConection,
    Header,
    Footer,
    FormWizard,
    TabContent,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      feedType: 2,
      croppieImage: "",
      cropped: null,
      show: false,
      params: {
        token: "123456798",
        name: "avatar",
      },
      headers: {
        smail: "*_~",
      },
      imgDataUrl: "", // the datebase64 url of created image
      postsData: [
      ],
      recomendedTags: [],
      selectedTags: [],
    };
  },
  computed: {
    isFirstLogin: function () {
      console.log(this.$store.getters.isFirstLogin);
      return this.$store.getters.isFirstLogin;
    },
  },
  mounted() {
    axios.get("/v1/posts/").then((response) => {
      this.postsData = response["data"];
    });
  },
  methods: {
    ...mapActions(["setFirstLogin"]),
    changeFeedType: function (type) {
      this.feedType = type;
    },
    select: async function (tag, e) {
      this.selectedTags.push(tag.id);
      console.log(this.selectedTags);
      e.target.classList.add("bg-purple-500");
    },
    awayModalPost: function () {
      this.showModalPost = false;
    },
    showPost: function (id) {
      this.showModalPost = true;
      console.log(id);
      //usar id para receber do backend o post relacionado
    },
    croppie(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      var reader = new FileReader();
      reader.onload = (e) => {
        this.$refs.croppieRef.bind({
          url: e.target.result,
        });
      };

      reader.readAsDataURL(files[0]);
    },
    crop() {
      // Options can be updated.
      // Current option will return a base64 version of the uploaded image with a size of 600px X 450px.

      return new Promise((resolve, reject) => {
        let options = {
          type: "base64",
          size: { width: 250, height: 250 },
          format: "jpeg",
        };
        this.$refs.croppieRef.result(options, (output) => {
          this.cropped = this.croppieImage = output;
          if (
            this.croppieImage ==
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAD6APoDAREAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AJ/4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/9k="
          )
            resolve(false);
          else {
            axios.get("/v1/tags/").then((response) => {
              this.recomendedTags = response["data"];
              resolve(true);
            });
          }
        });
      });
    },
    onComplete: async function () {
      axios({
        method: "post",
        url: "/v1/first_login",
        data: {
          image: this.croppieImage,
          tags: this.selectedTags,
        },
      });

      await this.setFirstLogin(false);
    },
  },
  "pt-pt": {
    hint: "Clique ou arraste o arquivo para a janela para carregar",
    loading: "A processar...",
    noSupported:
      "Browser não suportado, por favor utilize o Internet Explorer 10+ ou outro browser",
    success: "Imagem carregada com sucesso",
    fail: "Ocorreu um erro ao carregar a imagem",
    preview: "Pré-visualização",
    btn: {
      off: "Cancelar",
      close: "Fechar",
      back: "Voltar",
      save: "Guardar",
    },
    error: {
      onlyImg: "Por favor envie apenas imagens",
      outOfSize: "A imagem excede o limite de tamanho suportado: ",
      lowestPx: "O tamanho da imagem é muito pequeno. Tamanho mínimo: ",
    },
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
.posts::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
#right-bar::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
</style>
