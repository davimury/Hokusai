<template>
    <section class="min-h-screen flex items-stretch text-white ">
        <div class="lg:flex w-1/2 hidden bg-gray-500 bg-no-repeat bg-cover relative items-center" style="background-image: url(https://images.unsplash.com/photo-1577495508048-b635879837f1?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80);">
            <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
            <div class="w-full px-24 z-10">
                <h1 class="text-5xl font-bold text-left tracking-wide">RSA</h1>
                <p class="text-3xl my-4">Caros amigos, a consulta aos diversos militantes desafia a capacidade de equalização.</p>
            </div>
            <div class="bottom-0 absolute p-4 text-center right-0 left-0 flex justify-center space-x-4"></div>
        </div>

        <div class="lg:w-1/2 w-full flex items-center justify-center text-center md:px-16 px-0 z-0" style="background-color: #161616;">
            <div class="absolute lg:hidden z-10 inset-0 bg-gray-500 bg-no-repeat bg-cover items-center" style="background-image: url(https://images.unsplash.com/photo-1577495508048-b635879837f1?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80);">
                <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
            </div>
            <div class="w-full py-6 z-20">
                <h1 class="my-6 text-6xl">{ logo }</h1>
                <form @submit.prevent="login" class="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
                    <div class="pb-2 pt-4">
                        <input v-model="email" type="email" placeholder="Email" class="block w-full p-4 text-lg rounded-sm bg-black">
                    </div>
                    <div class="pb-2 pt-4">
                        <input v-model="password" class="block w-full p-4 text-lg rounded-sm bg-black" type="password" placeholder="Password">
                    </div>
                    <div class="text-right text-gray-400 hover:underline hover:text-gray-100">
                        <a href="#">Não tem conta? Registre-se</a>
                    </div>
                    <div class="px-4 pb-2 pt-4">
                        <button class="uppercase block w-full p-4 text-lg rounded-full bg-indigo-500 hover:bg-indigo-600 focus:outline-none">Logar-se</button>
                    </div>
                    <div class="p-4 text-center right-0 left-0 flex justify-center space-x-4 mt-16 lg:hidden"></div>
                </form>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Login',
    data: () => {
        return {
            email: null,
            password: null,
        }
    },
    methods: {
        async login() {
            if (this.email === null) 
                return  
            if (this.password === null) 
                return  

            fetch('http://localhost:8000/api/v1/login',
            {
                 method: 'post',
                 body: JSON.stringify({
                   email: this.email,
                   password: this.password
                 }),
                 headers: {"Content-type": "application/json"}
            }).then(response => {
                response.json().then(json => {
                    console.log(json)
                })
            })
       },
    },
}
</script>
