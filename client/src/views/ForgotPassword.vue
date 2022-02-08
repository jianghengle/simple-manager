<template>
  <div class="container">
    <section class="section">
      <h1 class="title is-4">Request Password Reset</h1>
      <div class="field">
         <label class="label">Email</label>
         <div class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="Email" v-model="email">
            <span class="icon is-small is-left">
               <i class="fas fa-envelope"></i>
            </span>
         </div>
      </div>
      <div class="field is-grouped">
        <div class="control">
          <button class="button is-link" :class="{'is-loading': waiting}" @click="sendRequest">Send Request</button>
        </div>
      </div>
      <div v-if="error" class="notification is-danger is-light">
        <button class="delete" @click="error=''"></button>
        {{error}}
      </div>
      <div v-if="success" class="notification is-success is-light">
        The password reset link has been sent to your email box.
      </div>
    </section>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'ForgotPassword',
  data () {
    return {
      email: '',
      success: false,
      error: '',
      waiting: false,
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
  },
  methods: {
    sendRequest () {
      if (this.waiting) {
        return
      }
      this.email = this.email.trim().toLowerCase()
      this.waiting = true
      this.error = ''
      this.success = false
      var message = {email: this.email}
      this.$http.post(this.server + '/myapp/create-password-reset/', message).then(resp => {
        this.success = true
        this.waiting = false
      }, err => {
        this.error = 'Did not find the user with the email!'
        this.waiting = false
      })
    },
  },
}
</script>
