// initial state
export const state = {
  token: localStorage.getItem('token'),
  email: localStorage.getItem('email'),
  superuser: localStorage.getItem('superuser') == 'true',
  staff: localStorage.getItem('staff') == 'true',
}
 
// mutations
export const mutations = {
  setUser (state, user) {
    state.token = user.token
    state.email = user.email
    state.superuser = user.superuser
    state.staff = user.staff
  },


  reset (state) {
    state.token = null
    state.email = null
    state.superuser = false
    state.staff = false
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('superuser')
    localStorage.removeItem('staff')
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
