import Vue from 'vue'
import App from './App'
import router from './router'
import Vuelidate from 'vuelidate'
import VueCarousel from 'vue-carousel'
import VueCroppie from 'vue-croppie';
import 'croppie/croppie.css' // import the croppie css manually
import store from './store';
import axios from 'axios';
import CKEditor from '@ckeditor/ckeditor5-vue2';
import 'animate.css'
import './assets/css/main.css'


axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/';

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
  
        originalRequest._retry = true;
        store.dispatch('LogOut')
        return router.push('/login')
    }
  }
})

Vue.use( CKEditor );
Vue.use(Vuelidate)
Vue.use(VueCarousel)
Vue.use(VueCroppie);
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
