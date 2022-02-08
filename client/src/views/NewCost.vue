<template>
  <div class="container mt-5 px-2">
    <article class="message is-danger" v-if="!token">
      <div class="message-body">
        You have not signed in yet. Please go back to <a href="/">home page</a> to sign in first.
      </div>
    </article>
    <div v-if="token">
      <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
          <li><router-link :to="'/invoices'">Invoices</router-link></li>
          <li class="is-active"><a href="#" aria-current="page">New</a></li>
        </ul>
      </nav>
      <div v-if="error" class="notification is-danger is-light">
        <button class="delete" @click="error=''"></button>
        {{error}}
      </div>
      <div class="mt-3">
        <div v-if="waitings.loading">
          <span class="icon is-medium is-size-4">
            <i class="fas fa-spinner fa-pulse"></i>
          </span>
        </div>
        <div v-else>
          <div v-if="model">

            <div class="field">
              <label class="label">Subject</label>
              <div class="control">
                <input class="input" type="text" placeholder="Subject" v-model="model.subject">
              </div>
            </div>

            <div class="field">
              <label class="label">Description</label>
              <div class="control">
                <textarea class="textarea" placeholder="Description" v-model="model.description"></textarea>
              </div>
            </div>

            <div class="field">
              <label class="label">Attachments</label>
              <div class="control">
                <attachments :attachments="model.attachments" :canEdit="true" @new-attachment-created="addAttachment" @attachment-deleted="removeAttachment" />
              </div>
            </div>

            <div class="field">
              <label class="label">Amount</label>
              <div class="control">
                <input class="input" type="number" v-model.number="model.amount" >
              </div>
            </div>

            <div class="field">
              <label class="label">Reviewer</label>
              <div class="control">
                <div class="select">
                  <select v-model="model.reviewers">
                    <option v-for="(email, i) in emails" :key="'email-option-' + i">
                      {{email}}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Tags</label>
              <div class="control" v-if="model.tags.length">
                <div class="input is-static">
                  <span v-for="(t, i) in model.tags" :key="'model-tag-' + i">
                    <span class="tag is-info is-medium">
                      {{t}}&nbsp;
                      <button class="delete is-small" @click="removeTag(i)"></button>
                    </span>&nbsp;
                  </span>
                </div>
              </div>
              <div class="field has-addons">
                <div class="control">
                  <input class="input" type="text" placeholder="New Tag" v-model="newTag">
                </div>
                <div class="control">
                  <a class="button" @click="addTag">
                    Add
                  </a>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Comment</label>
              <div class="control">
                <textarea class="textarea" placeholder="Comment" v-model="model.comment"></textarea>
              </div>
            </div>

            <div class="field is-grouped">
              <div class="control">
                <button class="button is-link" :class="{'is-loading': waitings.creating}" @click="createCost(true)">
                  Create and Send Email
                </button>
              </div>
              <div class="control">
                <button class="button is-light" :class="{'is-loading': waitings.creating}" @click="createCost(false)">Create Only</button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Attachments from '@/components/attachments/Attachments'

export default {
  name: 'NewCost',
  components: {
    Attachments,
  },
  data () {
    return {
      error: '',
      waitings: {
        loading: false,
        creating: false,
      },
      cost: null,
      model: null,
      newTag: '',
      emails: [],
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    token () {
      return this.$store.state.user.token
    },
    email () {
      return this.$store.state.user.email
    },
    costId () {
      return this.$route.params.costId
    },
    anyWaiting () {
      for (let key in this.waitings) {
        if (this.waitings[key]) {
          return true
        }
      }
      return false
    }
  },
  methods: {
    getCost () {
      this.waitings.loading = true
      this.$http.get(this.server + '/myapp/get-cost/' + this.costId + '/').then(resp => {
        this.cost = resp.body
        this.model = this.costToModel(resp.body)
        this.waitings.loading = false
      }, err => {
        this.error = err.body
        this.waitings.loading = false
      })
    },
    costToModel (cost) {
      var model = {
        subject: cost.subject,
        description: cost.description,
        amount: cost.amount,
        reviewers: cost.reviewers,
        tags: cost.tags.split(',').filter(t => t),
        comment: cost.comment,
        attachments: cost.attachments.split(',').filter(c => c),
      }
      return model
    },
    modelToCost () {
      var cost = {
        createdBy: this.email,
        subject: this.model.subject,
        description: this.model.description,
        status: 'Open',
        closedBy: '',
        reviewers: this.model.reviewers,
        tags: this.model.tags.join(','),
        amount: this.model.amount,
        comment: this.model.comment,
        attachments: this.model.attachments.join(','),
      }
      return cost
    },
    removeTag (i) {
      this.model.tags.splice(i, 1)
    },
    addTag () {
      var newTag = this.newTag.trim()
      if (newTag && !this.model.tags.includes(newTag)) {
        this.model.tags.push(newTag)
      } 
    },
    createCost (sendEmail) {
      if (this.anyWaiting) {
        return
      }
      this.waitings.creating = true
      var message = this.modelToCost(this.model)
      message.sendEmail = sendEmail
      this.$http.post(this.server + '/myapp/create-cost/', message).then(resp => {
        this.$router.push('/invoice/' + resp.body.id)
        this.waitings.creating = false
      }, err => {
        this.error = err.body
        this.waitings.creating = false
      })
    },
    getEmails () {
      this.$http.get(this.server + '/myapp/get-all-emails/').then(resp => {
        this.emails = resp.body
      }, err => {
        this.error = err.body
      })
    },
    addAttachment (attachment) {
      this.model.attachments.push(attachment.id)
    },
    removeAttachment (attachmentId) {
      var index = this.model.attachments.indexOf(attachmentId)
      if (index > -1) {
        this.model.attachments.splice(index, 1)
      }
    },
  },
  mounted () {
    if (this.costId != 'new') {
      this.$nextTick(function () {
        this.getCost()
        this.getEmails()
      })
    } else {
      this.$nextTick(function () {
        this.getEmails()
      })
      this.model = {
        subject: '',
        description: '',
        amount: 0,
        reviewers: '',
        tags: [],
        comment: '',
        attachments: [],
      }
    }
  },
}
</script>
