<template>
  <div>
    <Header></Header>
    <main class="w-full mt-4">
      <div
        class="h-full md:max-w-4xl mx-auto bg-lightgray rounded-lg flex content-center p-5"
      >
        <div v-if="postType == 2" class="mx-auto my-auto text-center">
          <h1 class="text-white font-bold text-xl mb-5">
            Comece a criar uma nova postagem:
          </h1>
          <div class="text-purple-500">
            <button class="focus:outline-none" @click="choosePostType(0)">
              <span
                class="material-icons p-6 bg-purple-500 bg-opacity-10 hover:bg-opacity-100 hover:text-white rounded-full m-3 mb-1 transition duration-200 ease-in-out"
                >collections</span
              >
              <h2 class="text-white font-medium cursor-default">Imagens</h2>
            </button>
            <button class="focus:outline-none" @click="choosePostType(1)">
              <span
                class="material-icons p-6 bg-purple-500 bg-opacity-10 hover:bg-opacity-100 hover:text-white rounded-full m-3 mb-1 transition duration-200 ease-in-out"
                >format_size</span
              >
              <h2 class="text-white font-medium cursor-default">Texto</h2>
            </button>
          </div>
        </div>

        <div v-if="postType == 0" class="mx-auto w-full">
          <form action="" class="w-3/6">
            <vue-dropzone
              ref="myVueDropzone"
              id="dropzone"
              :options="dropzoneOptions"
              class="mb-5"
            ></vue-dropzone>
            <label class="text-white font-medium" for="description"
              >Descrição</label
            >
            <textarea
              class="bg-lightergray rounded-lg w-full focus:outline-none p-2 text-white"
              name="description"
            ></textarea>

            <button
              class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2"
            >
              Publicar
            </button>
          </form>
        </div>

        <div v-if="postType == 1" class="mx-auto w-full"></div>
      </div>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
export default {
  name: "CreatePost",
  components: {
    Header,
    Footer,
    vueDropzone: vue2Dropzone,
  },
  data: function () {
    return {
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: { "My-Awesome-Header": "header value" },
      },
      postType: 2,
    };
  },
  methods: {
    choosePostType: function (type) {
      this.postType = type;
    },
  },
};
</script>

<style scoped>
main {
  height: 90vh;
}
</style>