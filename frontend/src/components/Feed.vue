<template>
  <div 
  class="h-screen"
  @mousemove="mouseMove"
  >
    <Header></Header>
    <main
      class="flex justify-center mx-auto h-screen w-full md:max-w-4xl pb-96"
      
    >
      <div class="w-full md:w-4/5 lg:w-3/5 h-screen p-3">
        <div class="w-full flex justify-center gap-5 bg-darkgray sticky top-0">
          <button
            class="
              text-white
              border-b-2
              hover:border-purple-600
              focus:outline-none
            "
            @click="changeFeedType(1)"
            :class="feedType == 1 ? 'border-purple-500' : 'border-lightergray'"
          >
            Seguindo
          </button>
          <button
            class="
              text-white
              border-b-2
              hover:border-purple-600
              focus:outline-none
            "
            @click="changeFeedType(2)"
            :class="feedType == 2 ? 'border-purple-500' : 'border-lightergray'"
          >
            Recomendados
          </button>
        </div>
        <div class="w-full flex flex-col posts h-100">
          <div v-if="feedType == 1">
            <Post
              v-for="postData in followPosts"
              :key="postData.post_id"
              :postData="postData"
              class="my-4"
            ></Post>
            <infinite-loading :identifier="infiniteId" @infinite="loadMoreCon">
              <div slot="no-more" class="pb-20 text-white">
                Você já viu todos os posts!
              </div>
              <div slot="no-results" class="pb-20">
                <NotFoundGhost
                  :xAxis="this.xAxis"
                  :yAxis="this.yAxis"
                ></NotFoundGhost>
              </div>
            </infinite-loading>
          </div>
        </div>
        <div class="w-full flex flex-col posts h-100">
          <div v-if="feedType == 2">
            <Post
              v-for="postData in recPosts.slice()"
              :key="postData.post_id"
              :postData="postData"
              class="my-4"
            ></Post>
            <infinite-loading :identifier="infiniteId" @infinite="loadMoreRec">
              <div slot="no-more" class="pb-20 text-white">
                Você já viu todos os posts!
              </div>
              <div slot="no-results" class="pb-20">
                <NotFoundGhost
                  :xAxis="this.xAxis"
                  :yAxis="this.yAxis"
                ></NotFoundGhost>
              </div>
            </infinite-loading>
          </div>
        </div>
      </div>

      <div id="right-bar" class="w-1/3 md:2/4 hidden lg:block h-screen p-3">
        <SuggestedConection class="mb-4"></SuggestedConection>

        <TrendingTags></TrendingTags>
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
        class="
          flex
          items-end
          justify-center
          min-h-screen
          pt-4
          px-4
          pb-20
          text-center
          sm:block
          sm:p-0
        "
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
          class="
            inline-block
            align-bottom
            overflow-hidden
            transform
            transition-all
            sm:my-8
            sm:align-middle
            sm:max-w-lg
            sm:w-full
          "
          v-on-clickaway="awayModalPost"
        >
          <div
            class="
              bg-lightgray
              border border-lightgray
              rounded-lg
              block
              w-full
              mb-16
              text-white
            "
          >
            <form-wizard
              @on-complete="onComplete"
              :title="''"
              :subtitle="''"
              :color="'#8B5CF6'"
              :errorColor="'#B91C1C'"
              :finishButtonText="'Finalizar'"
              :nextButtonText="'Avançar'"
              :backButtonText="'Voltar'"
              :stepSize="'sm'"
            >
              <tab-content :before-change="crop">
                <h2 class="text-center mb-4 font-semibold">
                  Escolha sua foto de perfil
                </h2>
                <vue-croppie
                  ref="croppieRef"
                  :enableExif="true"
                  :enableOrientation="true"
                  :boundary="{ width: 300, height: 300 }"
                  :viewport="{ width: 250, height: 250, type: 'circle' }"
                ></vue-croppie>
                <div>
                  <label
                    for="croppieProfile"
                    class="
                      border border-purple-500
                      hover:border-purple-600
                      focus:outline-none
                      text-white
                      p-2
                      rounded-lg
                      text-base
                      cursor-pointer
                    "
                    >Escolher imagem</label
                  >
                  <input
                    class="hidden"
                    type="file"
                    id="croppieProfile"
                    name="croppieProfile"
                    @change="croppie"
                  />
                </div>
              </tab-content>
              <tab-content>
                <div class="flex flex-wrap content-center justify-center">
                  <h2 class="text-center mb-4 font-semibold w-full">
                    Escolha categorias que você tem interesse
                  </h2>
                  <div
                    class="
                      text-xs
                      mr-2
                      my-1
                      uppercase
                      tracking-wider
                      border
                      px-2
                      text-purple-500
                      border-purple-500
                      hover:bg-purple-500
                      hover:text-purple-600
                      cursor-default
                    "
                    v-for="tag in recomendedTags"
                    :key="tag.tag_id"
                    :id="tag.tag_id"
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
import NotFoundGhost from "./NotFoundGhost.vue";
import { FormWizard, TabContent } from "vue-form-wizard";
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import SuggestedConection from "./SuggestedConection.vue";
import TrendingTags from "./TrendingTags.vue";
import axios from "axios";
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import { mapActions } from "vuex";
import InfiniteLoading from "vue-infinite-loading";

export default {
  name: "Feed",
  components: {
    Post,
    SuggestedConection,
    Header,
    Footer,
    NotFoundGhost,
    FormWizard,
    TabContent,
    TrendingTags,
    InfiniteLoading,
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
      infiniteId: +new Date(),
      params: {
        token: "123456798",
        name: "avatar",
      },
      headers: {
        smail: "*_~",
      },
      imgDataUrl: "", // the datebase64 url of created image
      followPosts: [],
      recPosts: [],
      recQuerys: 0,
      conQuerys: 0,
      recomendedTags: [],
      selectedTags: [],
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      xAxis: 0,
      yAxis: 0,
      globalSkipCounter: 0,
      globalSkipRate: 5
    };
  },
  computed: {
    isFirstLogin: function () {
      return this.$store.getters.isFirstLogin;
    },
  },
  methods: {
    ...mapActions(["setFirstLogin"]),
    changeFeedType: function (type) {
      this.feedType = type;
      this.infiniteId += 1;
      console.log(this.infiniteId);
      /* console.log(this.busyCon)
      console.log(this.busyRec)
      if (type == 1){
        this.busyCon = false
        this.busyRec = true
      } else {
        this.busyRec = false
        this.busyCon = true
      } */
    },
    select: async function (tag, e) {
      this.selectedTags.push({ tag_id: tag["tag_id"] });
      e.target.classList.add("bg-purple-500");
    },
    awayModalPost: function () {
      this.showModalPost = false;
    },
    showPost: function (id) {
      this.showModalPost = true;
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
            axios.get("/tags/recommended").then((response) => {
              this.recomendedTags = response["data"];
              resolve(true);
            });
          }
        });
      });
    },
    onComplete: async function () {
      axios.post("/user/image", { base: this.croppieImage });
      axios.post("/tags/add", this.selectedTags);
      await this.setFirstLogin(false);
    },
    mouseMove: function (event) {
      let pageX = window.innerWidth;
      let pageY = window.innerHeight;
      let mouseY = 0;
      let mouseX = 0;

      if (this.globalSkipCounter >= this.globalSkipRate){
        //verticalAxis
        mouseY = event.clientY;
        this.yAxis = ((pageY - mouseY) / pageY) * 100;

        //horizontalAxis
        mouseX = event.clientX / -pageX;
        this.xAxis = -mouseX * 50 - 50;

        this.globalSkipCounter = 0;
      } else {
        this.globalSkipCounter += 1;
      }
    },
    loadMoreRec: async function ($state) {
      await axios
        .get(`/posts/recommended/${this.recQuerys}`)
        .then((response) => {
          if (response["data"] != undefined) {
            this.recQuerys = this.recQuerys + 1;
            this.recPosts = this.recPosts.concat(response["data"]);

            setTimeout(function () {
              $state.loaded();
            }, 2000);
          } else {
            $state.complete();
          }
        });
    },
    loadMoreCon: async function ($state) {
      await axios
        .get(`/posts/connections/${this.conQuerys}`)
        .then((response) => {
          if (response["data"] != undefined) {
            this.conQuerys = this.conQuerys + 1;
            this.followPosts = this.followPosts.concat(
              response["data"].sort(function (a, b) {
                if (a["created_at"] > b["created_at"]) return 1;
                if (a["created_at"] < b["created_at"]) return -1;
              })
            );
            setTimeout(function () {
              $state.loaded();
            }, 2000);
          } else $state.complete();
        });
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
.stepTitle {
  color: #3b3b3b;
  line-height: 1.2rem;
  margin-top: 0.7rem;
}
.vue-form-wizard .wizard-icon-circle {
  background-color: #1e1e1e;
  color: white;
}
</style>
