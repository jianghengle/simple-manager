const dev = process.env.NODE_ENV == 'development'

// initial state
export const state = {
  server: dev ? 'http://localhost:8000' : 'https://myapi.vanityart.com',
  vendorList: [],
  subsidiaryList: [],
  vendorSubsidiaryMap: {},
}

// mutations
export const mutations = {
  setVendorSubsidiary (state, data) {
    var vendorSet = new Set()
    var subsidiarySet = new Set()
    var vendorSubsidiaryMap = {}
    data.forEach(item => {
      vendorSet.add(item.vendor)
      subsidiarySet.add(item.subsidiary)
      vendorSubsidiaryMap[item.vendor] = item.subsidiary
    })
    var vendorList = Array.from(vendorSet)
    vendorList.sort((a, b) => {
      var va = a.substr(a.indexOf(' ') + 1).trim()
      var vb = b.substr(b.indexOf(' ') + 1).trim()
      return va.localeCompare(vb)
    })
    state.vendorList = vendorList
    state.subsidiaryList = Array.from(subsidiarySet)
    state.vendorSubsidiaryMap = vendorSubsidiaryMap
  },
}

export default {
  namespaced: true,
  state,
  mutations
}
