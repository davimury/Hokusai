import Vue from 'vue'
import App from './App'
import router from './router'
import Vuelidate from 'vuelidate'
import VueCarousel from 'vue-carousel'
import store from './store';
import axios from 'axios';
import 'animate.css'
import './assets/css/main.css'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/';

Vue.use(Vuelidate)
Vue.use(VueCarousel)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
