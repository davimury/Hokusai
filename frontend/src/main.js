import Vue from 'vue'
import App from './App'
import router from './router'
import Vuelidate from 'vuelidate'
import VueCarousel from 'vue-carousel'
import store from './store';
import axios from 'axios';

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/';

import 'animate.css'
import './assets/css/main.css'

Vue.use(Vuelidate)
Vue.use(VueCarousel)
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
