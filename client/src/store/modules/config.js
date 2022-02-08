const dev = process.env.NODE_ENV == 'development'

// initial state
export const state = {
   server: dev ? 'http://localhost:8000' : 'https://myapi.vanityart.com',
}

export default {
  namespaced: true,
  state,
}
