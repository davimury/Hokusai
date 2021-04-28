import Vue from 'vue'
import App from './App'
import router from './router'
import Vuelidate from 'vuelidate'
import VueCarousel from 'vue-carousel'

import 'animate.css'
import './assets/css/main.css'

Vue.use(Vuelidate)
Vue.use(VueCarousel)
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
