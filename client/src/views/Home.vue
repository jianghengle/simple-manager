<template>
  <div class="container">
    <section class="section">
      <h1 class="title">Welcome to Simple Manager!</h1>
      <h2 class="subtitle">
        A simple tool to manage your workflows.
      </h2>

      <div v-if="token">
        <article class="message is-success">
          <div class="message-body">
            Please click the menu to access the tools.
          </div>
        </article>
      </div>
      <div v-else>
        <div class="field">
          <label class="label">Email</label>
          <div class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="Email" v-model="email">
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">Password</label>
          <div class="control has-icons-left has-icons-right">
            <input class="input" type="password" placeholder="Password" v-model="password" @keyup.enter="signin">
            <span class="icon is-small is-left">
              <i class="fas fa-key"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox" v-model="rememberMe">
              Remember me
            </label>
          </div>
        </div>

        <div class="field is-grouped">
          <div class="control">
            <button class="button is-link" :class="{'is-loading': waiting}" @click="signin">Sign in</button>
          </div>
        </div>

        <div v-if="error" class="notification is-danger is-light">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>

        <div>
          <router-link :to="'/forgot-password'">
            Forgot your password?
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'Home',
  data () {
    return {
      email: '',
      password: '',
      rememberMe: true,
      error: '',
      waiting: false,
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    token () {
      return this.$store.state.user.token
    }
  },
  methods: {
    signin () {
      this.email = this.email.trim().toLowerCase()
      this.waiting = true
      var message = {username: this.email, password: this.password}
      this.$http.post(this.server + '/myapp/api-token-auth/', message).then(resp => {
        if (resp.body) {
          var user = resp.body
          Vue.http.headers.common['Authorization'] = 'Token ' + user.token
          this.$store.commit('user/setUser', user)
          if (this.rememberMe) {
            localStorage.setItem('token', user.token)
            localStorage.setItem('email', user.email)
            localStorage.setItem('superuser', user.superuser ? 'true' : 'false')
            localStorage.setItem('staff', user.staff ? 'true' : 'false')
          }
          this.email = ''
          this.password = ''
          this.$router.push('/invoices')
        } else {
          this.error = 'Failed to sign in!'
          this.$store.commit('user/reset')
        }
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
  },
}
</script>
