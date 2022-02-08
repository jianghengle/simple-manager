import Vue from 'vue'
import Vuex from 'vuex'
import config from './modules/config'
import user from './modules/user'
import modals from './modules/modals'
import costs from './modules/costs'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    config: config,
    user: user,
    modals: modals,
    costs: costs,
  }
})
