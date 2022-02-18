// initial state
export const state = {
  sortOption: {
    field: 'createdAt',
    isAsc: false,
  },
  searchOption: '',
  filterOption: 'my'
}

// mutations
export const mutations = {
  setSortOption (state, sortOption) {
    state.sortOption = sortOption
  },


  setSearchOption (state, searchOption) {
    state.searchOption = searchOption
  },

  setFilterOption (state, filterOption) {
    state.filterOption = filterOption
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
