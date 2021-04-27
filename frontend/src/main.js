import Vue from 'vue'
import App from './App'
import router from './router'
import Vuelidate from 'vuelidate'

import 'animate.css'
import './assets/css/main.css'

Vue.use(Vuelidate)
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
