<template >

  <main class="h-screen" @mousemove="mouseMove">
    <div v-if="loading" class="w-screen h-screen fixed flex align-middle z-50 bg-gray-900 bg-opacity-75">
    <fingerprint-spinner
      :animation-duration="1500"
      :size="90"
      color="#8B5CF6"
      class="m-auto "
    />
  </div>
  <div v-if="this.name">
    <Header></Header>
    <div
      class="
        bg-lightgray
        text-white
        pb-6
        w-full
        justify-center
        items-center
        overflow-visible
        md:max-w-4xl
        rounded-lg
        shadow-sm
        mx-auto
      "
    >
      <div class="relative h-40">
        <img class="absolute h-full w-full object-cover" :src="`https://cdn.hokusai.codes/header/${this.user_id}.jpg?${cacheStr}`" @error="$event.target.src = 'https://cdn.hokusai.codes/header/default.jpg'"/>
        <button
          v-if="this.$route.params.username == this.$store.getters.Username"
          class="focus:outline-none"
          v-on:click="modalHeader = !modalHeader"
        >
          <span
            class="
              material-icons
              z-10
              absolute
              bottom-2
              right-3
              text-purple-500
              hover:text-purple-600
            "
          >
            photo_camera
          </span>
        </button>
      </div>
      <div
        class="
          relative
          shadow
          mx-auto
          h-24
          w-24
          -mt-12
          border-lightgray
          rounded-full
          overflow-hidden
          border-4
        "
      >
        <img class="object-cover w-full h-full" :src="`https://cdn.hokusai.codes/profile/${this.user_id}.jpg?${cacheStr}`" @error="$event.target.src = 'https://cdn.hokusai.codes/profile/default.jpg'"/>
      </div>
      <div
      v-if="this.$route.params.username == this.$store.getters.Username" 
      class="flex justify-center ml-11 relative -mt-6">
        <button
          class="focus:outline-none text-center bg-lightgray rounded-full p-1"
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
        </div>
        <div class="flex justify-center text-gray-500">
          <p class="mx-1">
            <span class="font-medium">{{ this.likes7day }}</span> likes (7 dias)
          </p>
          <p class="mx-1">
            <span class="font-medium">{{ this.likesTotal }}</span> likes (Total)
          </p>
        </div>
        <div class="flex justify-center text-gray-500">
          <p class="mx-1">
            <span class="font-medium">{{ this.postsCounter }}</span> Posts
          </p>
          <p
            class="mx-1 cursor-pointer"
            v-on:click="modalConexoes = !modalConexoes; getProfileCards();"
          >
            <span class="font-medium">{{ con_count }}</span> Conexões
          </p>
        </div>
        <div
          v-if="this.username != this.$store.getters.Username"
          class="flex justify-center text-gray-500"
        >
          <button
            v-if="!this.isConnected"
            @click="requestConnection"
            class="
              rounded-lg
              bg-purple-500
              hover:bg-purple-600
              focus:outline-none
              text-white
              p-2
              mx-1
              mt-2
            "
          >
            Conectar
          </button>
          <button
            v-if="this.isConnected && !this.conStatus"
            disabled
            class="
              rounded-lg
              bg-purple-400
              text-white
              p-2
              mx-1
              mt-2
              cursor-not-allowed
            "
          >
            Conexão Pendente
          </button>
          <button
            v-if="this.isConnected && this.conStatus"
            @click="removeConnection()"
            class="
              rounded-lg
              bg-purple-500
              hover:bg-purple-600
              focus:outline-none
              text-white
              p-2
              mx-1
              mt-2
            "
          >
            Remover Conexão
          </button>
          <a href="/chat">

          <button
            v-if="this.isConnected && this.conStatus"
            
            class="
              rounded-lg
              bg-purple-500
              hover:bg-purple-600
              focus:outline-none
              text-white
              p-2
              mx-1
              mt-2
            "
          >
            Mensagem
          </button>
          </a>
        </div>
      </div>
      <div
        class="mt-6 pt-3 flex flex-wrap mx-6 border-t border-lightergray w-100"
      >
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
            hover:text-purple-600
            hover:border-purple-600
            cursor-pointer
          "
          v-for="userTag in userTags"
          :key="userTag['tag_id']"
          :tag_id="userTag['tag_id']"
        >
          <a :href="`/tag/${userTag['name']}`">
            {{ userTag["name"] }}
          </a>
          <span
            v-if="isEditingTags"
            @click="removeTag"
            class="material-icons text-purple-500 hover:text-purple-600 text-sm"
            >clear</span
          >
        </div>
        <button
          class="ml-1 -mt-1 text-purple-500 hover:text-purple-600 -mt-3"
          @click="editTags(true)"
        >
          <span
            v-if="this.$route.params.username == this.$store.getters.Username"
            class="material-icons text-lg"
          >
            edit
          </span>
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
              class="
                rounded-lg
                border border-purple-500
                hover:border-purple-600
                focus:outline-none
                text-white
                p-1
                px-3
                mx-1
                mt-2
              "
            >
              Cancelar
            </button>
            <button
              class="
                rounded-lg
                border border-purple-500
                hover:border-purple-600
                bg-purple-500
                hover:bg-purple-600
                focus:outline-none
                text-white
                p-1
                px-3
                mx-1
                mt-2
              "
              @click="saveTags"
            >
              Salvar
            </button>
          </div>
        </div>
      </transition>
    </div>
    <div
      class="
        pb-6
        mt-6
        w-full
        justify-center
        items-center
        overflow-hidden
        md:max-w-4xl
        mx-auto
        grid grid-cols-3
        gap-1
      "
      v-if="posts.length > 0"
    >
      <div
        v-for="post in posts"
        :key="post.post_id"
        class="bg-lightgray post-card cursor-pointer"
        style="overflow: hidden;"
        @click="showPost(post)"
      >
        <img :src="thumbsData[post['post_id']]" class="media" />
      </div>
    </div>
    <div
      class="
        pb-6
        mt-6
        w-full
        justify-center
        items-center
        overflow-hidden
        mx-auto
        text-white text-center
        md:max-w-4xl
        mx-auto
      "
      v-else
    >
      <NotFoundGhost :xAxis="this.xAxis" :yAxis="this.yAxis"></NotFoundGhost>
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
          class="
            flex
            items-center
            justify-center
            md:min-w-full
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
            style="width: 100%;"
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
          class="
            flex
            items-center
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
              sm:align-middle
            "
          >
            <div
              class="
                bg-lightgray
                border border-lightgray
                rounded-lg
                block
                w-full
                text-white
                py-10
              "
              v-on-clickaway="awayModalHeader"
            >
              <vue-croppie
                ref="croppieRef"
                :enableExif="true"
                :enableOrientation="true"
                :boundary="{
                  width: windowWidth - 34,
                  height: (windowWidth - 34) * 0.42,
                }"
                :viewport="{
                  width: windowWidth - 34,
                  height: (windowWidth - 34) * 0.42,
                  type: 'rectangle',
                }"
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
                  accept="image/png, image/gif, image/jpeg"
                  @change="croppieProfile"
                />
              </div>
              <button
                class="
                  rounded-lg
                  bg-purple-500
                  hover:bg-purple-600
                  focus:outline-none
                  text-white
                  p-2
                  mx-1
                  mt-4
                  self-start
                "
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
          class="
            flex
            items-center
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
              sm:align-middle
            "
          >
            <div
              class="
                bg-lightgray
                border border-lightgray
                rounded-lg
                block
                w-full
                text-white
                py-8
              "
              v-on-clickaway="awayModalProfile"
            >
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
                  accept="image/png, image/gif, image/jpeg"
                  @change="croppieProfile"
                />
              </div>
              <div>
                <button
                  class="
                    rounded-lg
                    bg-purple-500
                    hover:bg-purple-600
                    focus:outline-none
                    text-white
                    p-2
                    mt-4
                    self-start
                  "
                  @click="changeProfile"
                >
                  Atualizar
                </button>
              </div>
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
        class="fixed z-10 inset-0"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-if="modalConexoes"
      >
        <div
          class="
            flex
            items-center
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
              sm:align-middle
              bg-lightgray
              rounded-lg
              p-4
              w-full
              sm:w-3/4
            "
            v-on-clickaway="awayModalConexoes"
          >
            <h1 class="text-white font-semibold mb-4">Conexões</h1>
            <div
              class="flex flex-wrap justify-center overflow-y-auto max-h-70vh"
            >
              <ProfileCard
                v-for="cardData in cardsData"
                :key="cardData.username"
                :cardData="cardData"
              ></ProfileCard>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <Footer></Footer>
  </div>
  </main>
</template>

<script>
import Header from "./Header.vue";
import NotFoundGhost from "./NotFoundGhost.vue";
import Post from "./Post.vue";
import Footer from "./Footer.vue";
import { directive as onClickaway } from "vue-clickaway";
import vue2Dropzone from "vue2-dropzone";
import "../assets/css/dropzone.css";
import axios from "axios";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import * as htmlToImage from "html-to-image";
import ProfileCard from "./ProfileCard.vue";
import { FingerprintSpinner } from "epic-spinners";

export default {
  name: "Profile",
  components: {
    Header,
    Post,
    NotFoundGhost,
    Footer,
    vSelect,
    vueDropzone: vue2Dropzone,
    ProfileCard,
    FingerprintSpinner
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      cardsData: [],
      posts: [],
      recomendedTags: [],
      isConnected: false,
      conStatus: false,
      name: false,
      image: "",
      user_id: "",
      con_count: 0,
      username: this.$route.params.username,
      userTags: [],
      postData: {},
      thumbsData: {},
      selectedTags: [],
      postsCounter: 0,
      likes7day: 0,
      likesTotal: 0,
      profilePic: "",
      modalPost: false,
      modalProfile: false,
      modalHeader: false,
      modalConexoes: false,
      croppieImage: "",
      cropped: null,
      croppieHeaderState: false,
      croppieProfileState: false,
      imgDataUrl: "", // the datebase64 url of created image
      isEditingTags: false,
      windowWidth: window.innerWidth > 1000 ? 1000 : window.innerWidth,
      xAxis: 0,
      yAxis: 0,
      globalSkipCounter: 0,
      globalSkipRate: 5,
      cacheStr: Math.random().toString(36).substring(7),
      loading: true,
    };
  },
  mounted: async function () {
    await axios
      .get(`/user/${this.$route.params.username}`)
      .then(async (response) => {
        if (!response["data"]) {
          window.location = "/not-found";
        } else {
          if (response["data"]["posts"].length > 0)
            await this.generateThumbs(response["data"]["posts"]);

          this.posts = response["data"]["posts"];
          this.userTags = response["data"]["tags"];
          this.postsCounter = response["data"]["posts_count"];
          this.likes7day = response["data"]["likes7day"];
          this.likesTotal = response["data"]["all_likes"];
          this.name = response["data"]["name"];
          this.user_id = response["data"]["user_id"];
          this.con_count = response["data"]["con_count"];
          this.loading = false
        }
      });

    if (this.username != this.$store.getters.Username) {
      axios
        .get(`/connection/${this.$route.params.username}`)
        .then((response) => {
          this.isConnected = response["data"]["is_connected"];
          this.conStatus = response["data"]["con_status"];
        });
    }

    if(this.$route.query.post != undefined){
      this.showPostById(this.$route.query.post)
    }
  },
  methods: {
    removeConnection: function () {
      axios.post('/connection/remove', {user_id: this.user_id})
      .then(() => window.location.reload());
    },
    getProfileCards: async function () {
      await axios
        .get(`/user/details/${this.$route.params.username}`)
        .then(async (response) => {
          let usersDetails = response["data"]["users_details"];

          var cards = []
          usersDetails.forEach((userDetails) => {
            cards.push({
              userId: userDetails.user_id,
              name: userDetails.name,
              username: userDetails.username,
            });
          });

          this.cardsData = cards
        });
    },
    generateThumbs: async function (posts) {
      for (let i = 0; i < posts.length; i++) {
        if (posts[i]["postType"] == 0) {
          try {
            var thumb = `https://cdn.hokusai.codes/posts/${posts[i]["slides"][0]}`
          }
          catch {
            var thumb = `https://cdn.hokusai.codes/posts/default.jpg`
          }
          
          this.thumbsData[
            posts[i]["post_id"]
          ] = thumb;
        } else {
          var div = document.createElement('div');
          div.style.color              = '#fff';
          //div.style.fontSize         = '13px';
          div.style.marginTop          = '-10px';
          div.style.paddingBottom      = '5px';
          div.style.paddingTop         = '10px';
          div.style.paddingLeft        = '10px';
          div.style.paddingRight       = '10px';
          div.style.fontFamily         = 'Roboto, sans-serif';
          div.style.backgroundColor    = '#1e1e1e';
          div.style.overflow           = 'hidden';
          div.innerHTML = posts[i]['body'];
          
          const img = await htmlToImage.toJpeg(div, {width: 300, height: 300})
          this.thumbsData[posts[i]['post_id']] = img
        }
      }
    },
    /* Tags */
    editTags: function (isEditing) {
      axios
        .get("/tags/recommended")
        .then((response) => {
          this.recomendedTags = response["data"];
        })
        .then(() => (this.isEditingTags = isEditing));
    },

    addTag: function (e) {
      axios
        .post("/tag/new", { name: e["name"] })
        .then((res) => (e["id"] = res["data"]["id"]));
    },

    saveTags: function () {
      axios.post("/tags/add", this.selectedTags).then(() => {
        this.selectedTags = [];
        this.editTags(false);
        this.updateTags();
      });
    },

    removeTag(e) {
      axios
        .post("/tags/remove", [{ tag_id: e.path[1].getAttribute("tag_id") }])
        .then(() => this.updateTags());
    },

    updateTags: async function () {
      axios
        .get(`/tags/${this.username}`)
        .then((response) => (this.userTags = response["data"]));

      axios
        .get("/tags/recommended")
        .then((response) => (this.recomendedTags = response["data"]));
    },

    appendTag(e) {
      this.selectedTags = e;
    },

    /* Modal */
    awayModalPost: function () {
      this.modalPost = false;
    },
    awayModalConexoes: function () {
      this.modalConexoes = false;
    },
    awayModalHeader: function () {
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
    showPostById: function (post_id) {
      this.posts.forEach((element) => {
        if(element['post_id'] == post_id){
          this.postData = element;
          this.modalPost = true;
        }
      });
    },
    croppieHeader(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (e) => {
        this.$refs.croppieRef.bind({
          url: e.target.result,
        });
      };

      this.croppieHeaderState = true;
    },
    croppieProfile(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (e) => {
        this.$refs.croppieRef.bind({
          url: e.target.result,
        });
      };

      this.croppieProfileState = true;
    },

    changeProfile: async function () {
      let options = {
        type: "base64",
        size: { width: 250, height: 250 },
        format: "jpeg",
      };

      this.loading = true
      await this.$refs.croppieRef.result(options, (output) => {
        this.cropped = this.croppieImage = output;
      });

      await axios({
        method: "post",
        url: "/user/image",
        data: {
          base: this.croppieImage,
        },
      }).then( () => this.$router.go(this.$router.currentRoute));
    },

    changeHeader: async function () {
      let options = {
        type: "base64",
        size: { width: 896, height: 360 },
        format: "jpeg",
      };

      this.loading = true
      await this.$refs.croppieRef.result(options, (output) => {
        this.cropped = this.croppieImage = output;
      });

      await axios({
        method: "post",
        url: "/user/header",
        data: {
          base: this.croppieImage,
        },
      }).then( () => this.$router.go(this.$router.currentRoute));
    },

    requestConnection: function () {
      axios.post("/connection/new", { username: this.username }).then(() => {
        axios
          .get(`/connection/${this.$route.params.username}`)
          .then((response) => {
            this.isConnected = response["data"]["is_connected"];
            this.conStatus = response["data"]["con_status"];
          });
      });
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
  },
};
</script>

<style>
</style>
