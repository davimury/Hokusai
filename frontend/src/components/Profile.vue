<template>
  <main class="h-screen overflow-x-hidden">
    <Header></Header>
    <div
      class="bg-lightgray text-white pb-6 w-full justify-center items-center overflow-hidden md:max-w-4xl rounded-lg shadow-sm mx-auto"
    >
      <div class="relative h-40">
        <img
          class="absolute h-full w-full object-cover"
          src="https://images.unsplash.com/photo-1448932133140-b4045783ed9e?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
        />
      </div>
      <div
        class="relative shadow mx-auto h-24 w-24 -my-12 border-purple-500 rounded-full overflow-hidden border-4"
      >
        <img
          class="object-cover w-full h-full"
          src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=200&q=80"
        />
      </div>
      <div class="mt-16">
        <h1 class="text-lg text-center font-semibold">Cassie</h1>
        <div class="flex justify-center text-gray-500">
          <p class="mx-1"><span class="font-medium">35</span> Posts</p>
          <p class="mx-1"><span class="font-medium">150</span> Conexões</p>
        </div>
        <div class="flex justify-center text-gray-500">
          <button class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2">Conectar</button>
          <button class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2">Mensagem</button>
        </div>
      </div>
      <div class="mt-6 pt-3 flex flex-wrap mx-6 border-t border-lightergray">
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
        >
          User experience
        </div>
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
        >
          VueJS
        </div>
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
        >
          TailwindCSS
        </div>
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
        >
          React
        </div>
        <div
          class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:bg-purple-500 hover:text-purple-600 cursor-default"
        >
          Painting
        </div>
      </div>
    </div>
    <div
      class="pb-6 mt-6 w-full justify-center items-center overflow-hidden md:max-w-4xl mx-auto grid grid-cols-3 gap-1"
    >
      <div class="bg-lightgray post-card cursor-pointer">
        <img
          src="https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
          alt=""
          class="media"
        />
      </div>
      <div class="bg-lightgray post-card cursor-pointer">
        <img
          src="https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80"
          alt=""
          class="media"
        />
      </div>
      <div class="bg-lightgray post-card"></div>
      <div class="bg-lightgray post-card"></div>
      <div class="bg-lightgray post-card"></div>
      <div class="bg-lightgray post-card"></div>
      <div class="bg-lightgray post-card"></div>
    </div>
  </main>
</template>

<script>
import Header from "./Header.vue";
export default {
  name: "Feed",
  components: {
    Header,
  },
};
</script>

<style>
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
</style>
