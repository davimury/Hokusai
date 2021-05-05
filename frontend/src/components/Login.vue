<template>
    <section class="min-h-screen flex items-stretch text-white ">
        <div class="w-1/2"> 
        <carousel :per-page="1" :loop="true" :autoplay="true" :autoplay-timeout="9000" :mouse-drag="true" :paginationEnabled="false" > 
            <slide>
           <div class="lg:flex w-full bg-no-repeat bg-cover relative items-center" style="height: 50.6vw;" v-bind:style="{ backgroundImage: 'url(' + image1 + ')' }">
                    <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
                    <div class="w-full px-24 z-10">
                        <!-- <h1 class="text-5xl font-bold text-left tracking-wide">Hokusai</h1> -->
                        <img src="@/assets/img/logo-nobg.svg">
                        <p class="text-xl my-4">Ejiri na Província de Suruga.</p>
                    </div>
                    <div class="bottom-0 absolute p-4 text-center right-0 left-0 flex justify-center space-x-4"></div>
                </div>
            </slide>
            <slide>
                 <div class="lg:flex w-full bg-no-repeat bg-cover relative items-center" style="height: 50.6vw;" v-bind:style="{ backgroundImage: 'url(' + image2 + ')' }">
                    <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
                    <div class="w-full px-24 z-10">
                        <img src="@/assets/img/logo-nobg.svg">
                        <p class="text-xl my-4">A Grande Onda de Kanagawa. </p>
                    </div>
                    <div class="bottom-0 absolute p-4 text-center right-0 left-0 flex justify-center space-x-4"></div>
                </div>
            </slide>
            <slide>
                 <div class="lg:flex w-full bg-no-repeat bg-cover relative items-center" style="height: 50.6vw;" v-bind:style="{ backgroundImage: 'url(' + image3 + ')' }">
                    <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
                    <div class="w-full px-24 z-10">
                        <img src="@/assets/img/logo-nobg.svg">
                        <p class="text-xl my-4">Fuji Vermelho de Katsushika.</p>
                    </div>
                    <div class="bottom-0 absolute p-4 text-center right-0 left-0 flex justify-center space-x-4"></div>
                </div>
            </slide>
        </carousel>
        </div>

        <div class="lg:w-1/2 w-full flex items-center justify-center text-center md:px-16 px-0 z-0 bg-darkgray overflow-hidden">
            <div class="absolute lg:hidden z-10 inset-0 bg-gray-900 bg-no-repeat bg-cover items-center" style="background-image: url(http://localhost:8080/assets/img/bg.png);">
                <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
            </div>
            <div class="w-full py-6 z-20 content-center">
                <img class="m-auto my-16 w-96" src="@/assets/img/logo-symb-nobg.svg">
                <!-- <h1 class="my-6 text-6xl">{ logo }</h1> -->
                <transition 
                    mode="out-in"
                    enter-active-class="animate__animated animate__fadeInLeft"
                    leave-active-class="animate__animated animate__fadeOutRight"
                >
                    <form v-if="loginDiv" @submit.prevent="login" class="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
                        <div class="pb-2 pt-4">
                            <input v-model.trim="emailLogIn" @input="delayTouch($v.emailLogIn)"  type="text" placeholder="Email" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 " :class="validateStyle($v.emailLogIn.$invalid, $v.emailLogIn.$dirty)">
                            <div v-if="$v.emailLogIn.$invalid && $v.emailLogIn.$dirty" class="text-red-700 text-left "><small>Insira um email válido</small></div>
                        </div>
                            
                        <div class="pb-2 pt-4 relative">
                            <span @click="swapVisibility" class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center">{{passwordIcon}}</span>
                            <input v-model.trim="passwordLogIn" @input="delayTouch($v.passwordLogIn)" :class="validateStyle($v.passwordLogIn.$invalid, $v.passwordLogIn.$dirty)" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500" :type="passwordType" placeholder="Senha">
                        </div>
                        <div v-if="$v.passwordLogIn.$invalid && $v.passwordLogIn.$dirty" class="text-red-700 text-left -mt-1.5"><small>Senha é obrigatoria</small></div>
                        <div @click="swapLoginRegister('sendLink')" class="text-right text-amber-400 hover:text-amber-100 font-medium">
                            <a href="#">Esqueceu a senha?</a>
                        </div>
                        <div class=" pb-2 pt-4">
                            <button class="block w-full p-2 text-lg rounded-lg bg-indigo-800 hover:bg-indigo-700 focus:outline-none">Log In</button>
                        </div>
                        <div class="p-4 text-center right-0 left-0 flex justify-center space-x-4 mt-16 lg:hidden"></div>
                        <div v-on:click="swapLoginRegister('register')" class="mt-3 text-center text-gray-400 hover:text-gray-100 font-medium">
                            <a href="#">Ainda não tem uma conta? <span class="text-indigo-800 hover:text-indigo-700">Cadastre-se</span></a>
                        </div>
                    </form>
                </transition>
                <transition 
                    mode="out-in"
                    enter-active-class="animate__animated animate__fadeInLeft"
                    leave-active-class="animate__animated animate__fadeOutRight"
                >
                    <form v-if="registerDiv" @submit.prevent="register" class="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
                        <div class="pb-2 pt-4">
                            <input v-model.trim="nameSignUp" @input="delayTouch($v.nameSignUp)" :class="validateStyle($v.nameSignUp.$invalid, $v.nameSignUp.$dirty)" type="text" placeholder="Nome" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500">
                            <div v-if="$v.nameSignUp.$invalid && $v.nameSignUp.$dirty" class="text-red-700 text-left "><small>Qual o seu nome?</small></div>
                        </div>
                        <div class="pb-2 pt-4">
                            <input v-model.trim="usernameSignUp" @input="delayTouch($v.usernameSignUp)" :class="validateStyle($v.usernameSignUp.$invalid, $v.usernameSignUp.$dirty)" type="text" placeholder="Username" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500">
                            <div v-if="$v.usernameSignUp.$invalid && $v.usernameSignUp.$dirty" class="text-red-700 text-left "><small>Username é obrigatório e deve ser único</small></div>
                        </div>
                        <div class="pb-2 pt-4">
                            <input v-model.trim="emailSignUp" @input="delayTouch($v.emailSignUp)" :class="validateStyle($v.emailSignUp.$invalid, $v.emailSignUp.$dirty)" type="email" placeholder="Email" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500">
                            <div v-if="$v.emailSignUp.$invalid && $v.emailSignUp.$dirty" class="text-red-700 text-left "><small>Insira um email válido</small></div>
                        </div>
                        <div class="pb-2 pt-4 relative">
                            <span @click="swapVisibility" class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center">{{passwordIcon}}</span>
                            <input v-model.trim="passwordSignUp" @input="delayTouch($v.passwordSignUp)" :class="validateStyle($v.passwordSignUp.$invalid, $v.passwordSignUp.$dirty)" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500" :type="passwordType" placeholder="Senha">
                        </div>
                        <div v-if="$v.passwordSignUp.$invalid && $v.passwordSignUp.$dirty" class="text-red-700 text-left -mt-1.5"><small>Senha é obrigatoria</small></div>
                        <div class=" pb-2 pt-4">
                            <button class="block w-full p-2 text-lg rounded-lg bg-indigo-800 hover:bg-indigo-700 focus:outline-none">Cadastrar</button>
                        </div>
                        <div class="p-4 text-center right-0 left-0 flex justify-center space-x-4 mt-16 lg:hidden"></div>
                        <div v-on:click="swapLoginRegister('login')" class="mt-3 text-center text-gray-400 hover:text-gray-100 font-medium">
                            <a href="#">Já tem uma conta? <span class="text-indigo-800 hover:text-indigo-700">Log In</span></a>
                        </div>
                    </form>
                </transition>
                <transition 
                    mode="out-in"
                    enter-active-class="animate__animated animate__fadeInLeft"
                    leave-active-class="animate__animated animate__fadeOutRight"
                >
                <div v-if="forgotPasswordDiv">
                    <form  @submit.prevent="sendLink" class="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
                    <h1 class="text-2xl font-semibold m-4">Problemas para logar?</h1>
                    <h2 class="text-base">Insira seu e-mail abaixo e enviaremos um link para você voltar a ter acesso a sua conta.</h2>
                        <div class="pb-2 pt-4">
                            <input v-model.trim="emailLink" @input="delayTouch($v.emailLink)" :class="validateStyle($v.emailLink.$invalid, $v.emailLink.$dirty)" type="email" placeholder="Email" class="block w-full p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500">
                            <div v-if="$v.emailLink.$invalid && $v.emailLink.$dirty" class="text-red-700 text-left "><small>Insira um email válido</small></div>
                        </div>
                        <div class="p-4 text-center right-0 left-0 flex justify-center space-x-4 mt-16 lg:hidden"></div>
                        <div class=" pb-2 pt-4">
                            <button class="block w-full p-2 text-lg rounded-lg bg-indigo-500 hover:bg-indigo-600 focus:outline-none">Enviar Link</button>
                        </div>
                    </form>
                    
                    <div v-on:click="swapLoginRegister('register')" class="mt-3 text-center text-gray-400 hover:text-gray-100 font-medium">
                        <a href="#">Criar Nova Conta</a>
                    </div>
                    <div v-on:click="swapLoginRegister('login')" class="mt-3 text-center text-gray-400 hover:text-gray-100 font-medium">
                        <a href="#">Voltar Para <span class="text-indigo-500 hover:text-indigo-400">Log In</span></a>
                    </div>
                </div>
                </transition>
            </div>
        </div>
    </section>
</template>

<script>
import bg3 from "../assets/img/bg3.png"
import bg2 from "../assets/img/bg5.png"
import bg1 from "../assets/img/bg4.png"
import logo from "../assets/img/logo.svg"
import { Carousel, Slide } from 'vue-carousel';
import { mapActions } from "vuex";
import {  required,  maxLength,  email,} from "vuelidate/lib/validators";

const touchMap = new WeakMap()
export default {
    name: 'Login',
    components: {
        Carousel,
        Slide
    },
    data() {
        return {
            image1: bg1,
            image2: bg3,
            image3: bg2,
            logo: logo,
            emailLogIn: null,
            emailSignUp: null,
            emailLink: null,
            passwordLogIn: null,
            passwordSignUp: null, 
            nameSignUp: null, 
            usernameSignUp: null,
            registerDiv: false,
            loginDiv: true,
            hidePassword: true,
            passwordIcon: "visibility",
            passwordType: "password",
            forgotPasswordDiv: false
        }
    },
    methods: {
        ...mapActions(["Register", "LogIn"]),
        register: async function () {
            try {
                await this.Register(JSON.stringify(
                    {
                        name: this.nameSignUp,
                        email: this.emailSignUp,
                        username: this.usernameSignUp,
                        password: this.passwordSignUp
                    }
                ));
                this.$router.push('/');
                this.showError = false
            } catch (error) {
                this.showError = true
            }
        },
        login: async function () {
            try {
                await this.LogIn(JSON.stringify({email: this.emailLogIn, password: this.passwordLogIn}));
                this.$router.push('/');
                this.showError = false
            } catch (error) {
                this.showError = true
            }
        },
        logout: async function (){
            await this.$store.dispatch('LogOut')
            this.$router.push('/login')
        },
        /* login: async function() {
            fetch('http://localhost:8000/v1/login',
            {
                 method: 'post',
                 credentials: 'include',
                 body: JSON.stringify({
                   email: this.emailLogIn,
                   password: this.passwordLogIn
                 }),
                 headers: {"Content-type": "application/json"}
            }).then(response => {
                if (response.status == 200)
                    this.$router.push('/')

                else if (response.status == 401)
                    alert('Error username ou email duplicado')
            })
        }, */
        /* register: async function() {
            fetch('http://localhost:8000/v1/register',
            {
                method: 'post',
                body: JSON.stringify({
                    name: this.nameSignUp,
                    email: this.emailSignUp,
                    username: this.usernameSignUp,
                    password: this.passwordSignUp
                }),
                headers: {"Content-type": "application/json"}
            }).then(response => {
                if (response.status == 200)
                    this.swapLoginRegister('login');

                else if (response.status == 409)
                    alert('Error username ou email duplicado')
            })
        }, */
        swapLoginRegister: function(content) {
           if (content == 'login'){
               this.registerDiv = false
               this.forgotPasswordDiv = false
               setTimeout(()=>{  this.loginDiv = true}, 501);
               
           }
           if (content == 'register'){
               this.forgotPasswordDiv = false
               this.loginDiv = false
               setTimeout(()=>{  this.registerDiv = true}, 501);   
           }
           if (content == 'sendLink'){
               this.loginDiv = false
               setTimeout(()=>{  this.forgotPasswordDiv = true}, 501);   
           }
        },
        swapVisibility: function(){
           this.hidePassword = this.hidePassword ? false : true
           this.passwordIcon = this.hidePassword ? "visibility" : "visibility_off"
           this.passwordType = this.hidePassword ? "password" : "text"
        },
        delayTouch($v) {
            $v.$reset()
            if (touchMap.has($v)) {
                clearTimeout(touchMap.get($v))
            }
            touchMap.set($v, setTimeout($v.$touch, 500))
        },
        validateStyle: function(isInvalid, isDirty){
            return isInvalid && isDirty ? 'ring-1 ring-red-700 focus:ring-red-700' : 'focus:ring-indigo-500'
        }
    },
    validations: {
    emailLogIn: {
      required,
      email,
    },
    emailSignUp: {
      required,
      email,
    },
    emailLink: {
      required,
      email,
    },
    nameSignUp: {
      required,
      maxLength: maxLength(50),
    },
    usernameSignUp: {
      required,
      maxLength: maxLength(15),
    },
    passwordLogIn: {
      required
    },
    passwordSignUp: {
      required,
    },
  }
}
</script>
<style scoped>
.animate__animated {
  --animate-duration: .5s;
}
</style>