// initial state
export const state = {
   filterOption: 'all'
 }
 
 // mutations
 export const mutations = {
   setFilterOption (state, filterOption) {
     state.filterOption = filterOption
   }
 }
 
 export default {
   namespaced: true,
   state,
   mutations
 }
 