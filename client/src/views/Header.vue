<template>
  <div>
    <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <router-link class="navbar-item is-size-4 has-text-weight-bold" :to="'/'">
            Simple Manager
          </router-link>

          <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false"
            :class="{'is-active': menuActive}" @click="menuActive = !menuActive">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div id="navbarBasicExample" class="navbar-menu"  :class="{'is-active': menuActive}">
          <div class="navbar-start" v-if="token">
            <router-link class="navbar-item" :to="'/invoices'">
              Invoices
            </router-link >
          </div>

          <div class="navbar-end">
            <a class="navbar-item" v-if="staff" target="_blank" :href="adminUrl">
              <span class="icon">
                <i class="fas fa-users-cog"></i>
              </span>
              <span>Admin</span>
            </a>
            <router-link class="navbar-item" v-if="!token" :to="'/'">
              <span class="icon">
                <i class="fas fa-sign-in-alt"></i>
              </span>
              <span>Sign in</span>
            </router-link>
            <a class="navbar-item" v-if="token" @click="signout">
              <span class="icon">
                <i class="fas fa-sign-out-alt"></i>
              </span>
              <span>Sign out</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'Header',
  data () {
    return {
      menuActive: false
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    staff () {
      return this.$store.state.user.staff
    },
    routerPath () {
      return this.$route.path
    },
    server () {
      return this.$store.state.config.server
    },
    adminUrl () {
      return this.server + '/admin'
    },
  },
  methods: {
    signout () {
      var confirm = {
        title: 'Sign Out',
        message: 'Are you sure to sign out?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.signoutConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    signoutConfirmed () {
      delete Vue.http.headers.common['Authorization']
      this.$store.commit('user/reset')
      if (this.routerPath != '/') {
        this.$router.push('/')
      }
    },
  },
  mounted () {
    if (this.token) {
      Vue.http.headers.common['Authorization'] = 'Token ' + this.token
    }
  }
}
</script>