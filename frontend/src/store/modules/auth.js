import axios from 'axios';

const state = {
    id: null,
    user: null,
    email: null,
    isFirstLogin: false,
};

const getters = {
    isAuthenticated: state => !!state.user,    
    StateUser: state => state.user,
    isFirstLogin: state => state.isFirstLogin,
    UserId: state => state.id,
};

const actions = {
    async Register({dispatch}, form) {
        await axios.post('/v1/register', form)
        await dispatch('LogIn', form) 
      },

    async LogIn({commit}, User) {
        User = JSON.parse(User)
        let user = await axios.post('/v1/login', JSON.stringify({'email': User['email'], 'password': User['password']}))
        await commit('setUser', user.data)
    },
    
    async LogOut({commit}){
        await axios.delete('/v1/logout')
        commit('LogOut', null)
    },

    async setFirstLogin({commit}, bool){
        commit('isFirstLogin', bool)
    }
};

const mutations = {
    setUser(state, user){
        state.id = user['id'];
        state.user = user['user'];
        state.email = user['email'];
    },

    LogOut(state){
        state.id = null
        state.user = null
        state.email = null
        state.isFirstLogin = null
    },

    isFirstLogin(state, bool){
        state.isFirstLogin = bool
    }
};

export default {
  state,
  getters,
  actions,
  mutations
};