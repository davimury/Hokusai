import axios from 'axios';

const state = {
    user: null,
    firstlogin: true,
};

const getters = {
    isAuthenticated: state => !!state.user,    
    StateUser: state => state.user,
    isFirstLogin: state => state.firstlogin,
};

const actions = {
    async Register({dispatch}, form) {
        await axios.post('/v1/register', form)
        await dispatch('LogIn', form) 
      },

    async LogIn({commit}, User) {
        User = JSON.parse(User)
        await axios.post('/v1/login', JSON.stringify({'email': User['email'], 'password': User['password']}))
        await commit('setUser', User['email'])
    },
    
    async LogOut({commit}){
        await axios.delete('/v1/logout')
        commit('LogOut', null)
    }
};

const mutations = {
    setUser(state, username){
        state.user = username
    },

    LogOut(state){
        state.user = null
    },
};

export default {
  state,
  getters,
  actions,
  mutations
};