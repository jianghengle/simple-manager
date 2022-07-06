<template>
  <div class="container">
    <article class="message is-danger" v-if="!superuser">
      <div class="message-body">
        You have not signed in yet. Please go back to <a href="/">home page</a> to sign in first.
      </div>
    </article>

    <section class="section" v-if="superuser">
      <h1 class="title is-4">Config</h1>

      <div class="field">
        <label class="label">Approval Receivers</label>
        <div class="field has-addons" v-for="(receiver, i) in approvalReceivers" :key="'approval-receiver-' + i">
          <p class="control has-icons-left">
            <span class="select">
              <select v-model="receiver.email">
                <option v-for="(email, j) in emails" :key="'approval-receiver-' + i + '-email-option-' + j">
                  {{email}}
                </option>
              </select>
              <span class="icon is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </span>
          </p>
          <p class="control">
            <a class="button" @click="removeApprovalReceiver(i)">
              <span class="icon is-small">
                <i class="fas fa-minus"></i>
              </span>
            </a>
          </p>
        </div>

        <div class="field has-addons">
          <div class="control has-icons-left">
            <span class="select">
              <select v-model="newApprovalReceiver">
                <option v-for="(email, i) in emails" :key="'approval-receiver-email-option-' + i">
                  {{email}}
                </option>
              </select>
              <span class="icon is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </span>
          </div>
          <div class="control">
            <a class="button is-success" @click="addApprovalReceiver">
              <span class="icon is-small">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </div>
        </div>
      </div>

      <div class="field">
        <label class="label">Reviewer Mappings</label>
        <div class="field has-addons" v-for="(mapping, i) in reviewMappings" :key="'reviewer-mapping-' + i">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Key" v-model="mapping.key">
            <span class="icon is-left">
              <i class="fas fa-key"></i>
            </span>
          </p>
          <p class="control has-icons-left">
            <span class="select">
              <select v-model="mapping.email">
                <option v-for="(email, j) in emails" :key="'reviewer-mapping-' + i + '-email-option-' + j">
                  {{email}}
                </option>
              </select>
            </span>
            <span class="icon is-left">
              <i class="fas fa-envelope"></i>
            </span>
          </p>
          <p class="control">
            <a class="button" @click="removeReviewerMapping(i)">
              <span class="icon is-small">
                <i class="fas fa-minus"></i>
              </span>
            </a>
          </p>
        </div>
        <div class="field has-addons">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Key" v-model="newReviewerMapping.key">
            <span class="icon is-left">
              <i class="fas fa-key"></i>
            </span>
          </p>
          <p class="control has-icons-left">
            <span class="select">
              <select v-model="newReviewerMapping.email">
                <option v-for="(email, i) in emails" :key="'new-reviewer-mapping-email-option-' + i">
                  {{email}}
                </option>
              </select>
            </span>
            <span class="icon is-left">
              <i class="fas fa-envelope"></i>
            </span>
          </p>
          <p class="control">
            <a class="button is-success" @click="addReviewerMapping">
              <span class="icon is-small">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </p>
        </div>
      </div>

      <div class="field is-grouped mt-4">
        <div class="control">
          <button class="button is-link" :disabled="!myConfigChanged" :class="{'is-loading': waiting}" @click="updateMyConfig">
            Save
          </button>
        </div>
      </div>
      
      <div v-if="myConfigChanged" class="notification is-warning is-light">
        You have unsaved changes!
      </div>

      <hr />

      <product-updater />
    </section>
  </div>
</template>

<script>
import ProductUpdater from '@/components/price-monitor/ProductUpdater'

export default {
  name: 'MyConfig',
  components: {
    ProductUpdater
  },
  data () {
    return {
      waiting: false,
      error: '',
      myConfig: null,
      approvalReceivers: [{email: 'jianghengle@gmail.com'}], // to be initialzied, value here to demo the UI
      newApprovalReceiver: '',
      reviewMappings:[{key: 'NY', email: 'jianghengle@gmail.com'}], // to be initialzied, value here to demo the UI
      newReviewerMapping: {key:'', email: ''},
      emails: [],
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    superuser () {
      return this.$store.state.user.superuser
    },
    canAddApprovalReceiver () {
      return true
    },
    canAddReviewerMapping () {
      return true
    },
    myConfigChanged () {
      return false
    },
  },
  methods: {
    getMyConfig () {
      this.waiting = true
      this.$http.get(this.server + '/myapp/get-my-config/').then(resp => {
        console.log(resp)
        this.myConfig = resp.body
        // initialize approvalReceivers
        // initialize reviewMappings
        console.log('No implementation yet')
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    getEmails () {
      this.$http.get(this.server + '/myapp/get-all-emails/').then(resp => {
        this.emails = resp.body
      }, err => {
        this.error = err.body
      })
    },
    updateMyConfig () {
      // construct myConfig object from approveReceivers and reviewerMappings
      // post to /myapp/get-my-config/ to update the config
      console.log('No implementation yet')
    },
    addApprovalReceiver () {
      console.log('No implementation yet')
    },
    removeApprovalReceiver (i) {
      console.log('No implementation yet')
    },
    addReviewerMapping () {
      console.log('No implementation yet')
    },
    removeReviewerMapping (i) {
      console.log('No implementation yet')
    },
  },
  mounted () {
    if (this.superuser) {
      this.getMyConfig()
      this.getEmails()
    }
  }
}
</script>


