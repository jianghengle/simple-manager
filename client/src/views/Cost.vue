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
          <li class="is-active"><a href="#" aria-current="page">{{costId}}</a></li>
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

            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Created By</p>
                  <p class="title is-6">{{model.createdBy}}</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Created At</p>
                  <p class="title is-6">{{model.createdAt}}</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Updated At</p>
                  <p class="title is-6">{{model.updatedAt}}</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Status</p>
                  <p>
                    <span class="tag is-link is-medium" v-if="model.status == 'Open'">Open</span>
                    <span class="tag is-success is-medium" v-if="model.status == 'Approved'">Approved</span>
                    <span class="tag is-warning is-medium" v-if="model.status == 'Rejected'">Rejected</span>
                    <span class="tag is-dark is-medium" v-if="model.status == 'NS Bill Created'">NS Bill Created</span>
                  </p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">
                    <span v-if="cost.status == 'Open'">Closed By</span>
                    <span v-if="cost.status == 'Approved'">Approved By</span>
                    <span v-if="cost.status == 'Rejected'">Rejected By</span>
                  </p>
                  <p class="title is-6">{{model.closedBy}}</p>
                </div>
              </div>
            </nav>

            <div class="field">
              <label class="label">Subject</label>
              <div class="control">
                <input class="input" type="text" placeholder="Subject" v-model="model.subject" :readonly="!canEdit">
              </div>
            </div>

            <div class="field">
              <label class="label">Description</label>
              <div class="control">
                <textarea class="textarea" placeholder="Description" v-model="model.description" :readonly="!canEdit"></textarea>
              </div>
            </div>

            <div class="field">
              <label class="label">Attachments</label>
              <div class="control">
                <attachments :attachments="model.attachments" :canEdit="canEdit" @new-attachment-created="addAttachment" @attachment-deleted="removeAttachment" />
              </div>
            </div>

            <div class="field">
              <label class="label">Amount</label>
              <div class="control">
                <input class="input" type="number" v-model.number="model.amount" :readonly="!canEdit">
              </div>
            </div>

            <div class="field">
              <label class="label">Reviewer</label>
              <div class="control">
                <div class="select">
                  <select v-model="model.reviewers" :disabled="!canEdit">
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
              <div class="field has-addons" v-if="canEdit">
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
                <textarea class="textarea" placeholder="Comment" v-model="model.comment" :readonly="!canEdit"></textarea>
              </div>
            </div>

            <div class="field">
              <label class="label">Invoice Number</label>
              <div class="control">
                <input class="input" type="text" placeholder="Invoice Number" v-model="model.invoiceNumber" :readonly="!canEdit">
              </div>
            </div>

            <div class="field">
              <label class="label">Vendor</label>
              <div class="field has-addons">
                <div class="control">
                  <span class="select">
                    <select v-model="model.vendorNameMode" :disabled="!canEdit">
                      <option>Select</option>
                      <option>New</option>
                    </select>
                  </span>
                </div>
                <div class="control is-expanded model-select-container" v-if="model.vendorNameMode == 'Select'">
                  <model-select :options="vendorOptions" v-model="model.selectedVendorName" :isDisabled="!canEdit"/>
                </div>
                <div class="control is-expanded" v-if="model.vendorNameMode == 'New'">
                  <input class="input" type="text" placeholder="Input new vendor" v-model="model.newVendorName" :readonly="!canEdit">
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Subsidiary</label>
              <div class="field has-addons">
                <div class="control">
                  <span class="select">
                    <select v-model="model.subsidiaryMode" :disabled="!canEdit">
                      <option>Select</option>
                      <option>New</option>
                    </select>
                  </span>
                </div>
                <div class="control is-expanded" v-if="model.subsidiaryMode == 'Select'">
                  <span class="select">
                    <select v-model="model.selectedSubsidiary" :disabled="!canEdit">
                      <option v-for="(so, i) in subsidiaryList" :key="'subsidiary-option-' + i">{{so}}</option>
                    </select>
                  </span>
                </div>
                <div class="control is-expanded" v-if="model.subsidiaryMode == 'New'">
                  <input class="input" type="text" placeholder="Input new subsidiary" v-model="model.newSubsidiary" :readonly="!canEdit">
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Expense Account</label>
              <div class="control">
                <input class="input" type="text" placeholder="Expense Account" v-model="model.expenseAccount" :readonly="!canEdit">
              </div>
            </div>
            
            <div class="field is-grouped mt-5" v-if="cost.status == 'Open'">
              <div class="control" v-if="canEdit">
                <button class="button is-link" :disabled="!costChanged" :class="{'is-loading': waitings.saving}" @click="saveCost">
                  Save
                </button>
              </div>
              <div class="control">
                <button class="button is-light" :class="{'is-loading': waitings.sendingEmail}" @click="sendEmail">Send Email</button>
              </div>
            </div>
            
            <div v-if="costChanged" class="notification is-warning is-light">
              You have unsaved changes!
            </div>

            <hr/>

            <div class="field is-grouped">
              <div class="control" v-if="canClose">
                <button class="button is-success" :class="{'is-loading': waitings.approving}" :disabled="!canApprove" @click="approveCost">
                  Approve
                </button>
              </div>
              <div class="control" v-if="canSubmit">
                <button class="button is-dark" :class="{'is-loading': waitings.submitting}" @click="submitCost">
                  Submit NS Bill
                </button>
              </div>
              <div class="control" v-if="canClose">
                <button class="button is-warning" :class="{'is-loading': waitings.rejecting}" @click="rejectCost">Reject</button>
              </div>
              <div class="control" v-if="canEdit">
                <button class="button is-danger" :class="{'is-loading': waitings.deleting}" @click="deleteCost">Delete</button>
              </div>
              <div class="control">
                <router-link :to="'/new-invoice/' + costId" class="button is-light">Copy to New</router-link>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dateFormat from 'dateformat'
import Attachments from '@/components/attachments/Attachments'
import { ModelSelect } from 'vue-search-select'

export default {
  name: 'Cost',
  components: {
    Attachments,
    ModelSelect,
  },
  data () {
    return {
      error: '',
      waitings: {
        loading: false,
        saving: false,
        sendingEmail: false,
        approving: false,
        rejecting: false,
        deleting: false,
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
    vendorList () {
      return this.$store.state.config.vendorList
    },
    vendorOptions () {
      return this.vendorList.map(item => {
        return {value: item, text: item}
      })
    },
    subsidiaryList () {
      return this.$store.state.config.subsidiaryList
    },
    modelVendorName () {
      if (this.model) {
        return this.model.vendorNameMode == 'New' ? this.model.newVendorName : this.model.selectedVendorName
      }
    },
    vendorSubsidiaryMap () {
      return this.$store.state.config.vendorSubsidiaryMap
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
    costChanged () {
      if (this.cost.subject != this.model.subject
          || this.cost.description != this.model.description
          || this.cost.amount != this.model.amount
          || this.cost.comment != this.model.comment
          || this.cost.reviewers != this.model.reviewers
          || this.cost.invoiceNumber != this.model.invoiceNumber
          || this.cost.expenseAccount != this.model.expenseAccount) {
        return true
      }
      if (this.cost.tags != this.model.tags.join(',')) {
        return true
      }
      if (this.cost.attachments != this.model.attachments.join(',')) {
        return true
      }
      var vendorName = this.model.vendorNameMode == 'New' ? this.model.newVendorName : this.model.selectedVendorName
      if (this.cost.vendorName != vendorName) {
        return true
      }
      var subsidiary = this.model.subsidiaryMode == 'New' ? this.model.newSubsidiary : this.model.selectedSubsidiary
      if (this.cost.subsidiary != subsidiary) {
        return true
      }
      return false
    },
    anyWaiting () {
      for (let key in this.waitings) {
        if (this.waitings[key]) {
          return true
        }
      }
      return false
    },
    canEdit () {
      if (!this.cost) {
        return false
      }
      if (this.cost.status != 'Open') {
        return false
      }
      if (this.cost.createdBy == this.email || this.cost.reviewers.includes(this.email)) {
        return true
      }
      return false
    },
    canClose () {
      if (!this.cost) {
        return false
      }
      if (this.cost.status != 'Open') {
        return false
      }
      if (this.cost.reviewers.includes(this.email)) {
        return true
      }
      return false
    },
    canApprove () {
      if (!this.canClose) {
        return false
      }
      var cost = this.modelToCost()
      if (!cost.invoiceNumber || !cost.vendorName || !cost.subsidiary) {
        return false
      }
      return true
    },
    canSubmit () {
      if (!this.cost) {
        return false
      }
      if (this.cost.status != 'Approved') {
        return false
      }
      if (this.cost.createdBy == this.email || this.cost.reviewers.includes(this.email)) {
        return true
      }
      return false
    },
  },
  watch: {
    costId: function (val) {
      this.getCost()
    },
    modelVendorName: function (val) {
      if (this.model.subsidiaryMode == 'Select') {
        var subsidiary = this.vendorSubsidiaryMap[val]
        if (subsidiary) {
          this.model.selectedSubsidiary = subsidiary
        }
      }
    },
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
        createdAt: dateFormat(new Date(cost.createdAt * 1000), 'mm/dd/yyyy h:MM TT'),
        updatedAt: dateFormat(new Date(cost.updatedAt * 1000), 'mm/dd/yyyy h:MM TT'),
        createdBy: cost.createdBy,
        status: cost.status,
        closedBy: cost.closedBy || 'Not yet',
        reviewers: cost.reviewers,
        tags: cost.tags.split(',').filter(t => t),
        comment: cost.comment,
        attachments: cost.attachments.split(',').filter(a => a),
        invoiceNumber: cost.invoiceNumber,
        selectedVendorName: this.vendorList.includes(cost.vendorName) ? cost.vendorName : '',
        vendorNameMode: this.vendorList.includes(cost.vendorName) || !cost.vendorName ? 'Select' : 'New',
        newVendorName: this.vendorList.includes(cost.vendorName) ? '' : cost.vendorName,
        selectedSubsidiary: this.subsidiaryList.includes(cost.subsidiary) ? cost.subsidiary : '',
        subsidiaryMode: this.subsidiaryList.includes(cost.subsidiary) || !cost.subsidiary ? 'Select' : 'New', 
        newSubsidiary: this.subsidiaryList.includes(cost.subsidiary) ? '' : cost.subsidiary,
        expenseAccount: cost.expenseAccount,
      }
      return model
    },
    modelToCost () {
      var cost = {
        id: this.costId,
        createdBy: this.model.createdBy,
        subject: this.model.subject,
        description: this.model.description,
        status: this.cost.status,
        closedBy: this.cost.closedBy,
        reviewers: this.model.reviewers,
        tags: this.model.tags.join(','),
        amount: this.model.amount,
        comment: this.model.comment,
        attachments: this.model.attachments.join(','),
        invoiceNumber: this.model.invoiceNumber,
        vendorName: this.model.vendorNameMode == 'New' ? this.model.newVendorName : this.model.selectedVendorName,
        subsidiary: this.model.subsidiaryMode == 'New' ? this.model.newSubsidiary : this.model.selectedSubsidiary,
        expenseAccount: this.model.expenseAccount,
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
    saveCost () {
      if (this.anyWaiting || !this.costChanged) {
        return
      }
      this.waitings.saving = true
      var message = this.modelToCost(this.model)
      this.$http.post(this.server + '/myapp/update-cost/' + this.costId + '/', message).then(resp => {
        this.getCost()
        this.waitings.saving = false
      }, err => {
        this.error = err.body
        this.waitings.saving = false
      })
    },
    approveCost () {
      if (!this.canApprove) {
        return
      }
      var confirm = {
        title: 'Approve Invoice',
        message: 'Are you sure to approve this invoice?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.approveCostConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    approveCostConfirmed () {
      if (this.anyWaiting || this.cost.status != 'Open') {
        return
      }
      this.waitings.approving = true
      var message = this.modelToCost(this.model)
      message.status = 'Approved'
      message.closedBy = this.email
      this.$http.post(this.server + '/myapp/update-cost/' + this.costId + '/', message).then(resp => {
        this.getCost()
        this.waitings.approving = false
      }, err => {
        this.error = err.body
        this.waitings.approving = false
      })
    },
    submitCost () {
      var confirm = {
        title: 'Submit Invoice',
        message: 'Are you sure this invoice has been created in NetSuite?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.submitCostConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    submitCostConfirmed () {
      if (this.anyWaiting || !this.canSubmit) {
        return
      }
      this.waitings.submitting = true
      var message = this.modelToCost(this.model)
      message.status = 'NS Bill Created'
      this.$http.post(this.server + '/myapp/update-cost/' + this.costId + '/', message).then(resp => {
        this.getCost()
        this.waitings.submitting = false
      }, err => {
        this.error = err.body
        this.waitings.submitting = false
      })
    },
    rejectCost () {
      var confirm = {
        title: 'Reject Invoice',
        message: 'Are you sure to reject this invoice?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.rejectCostConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    rejectCostConfirmed () {
      if (this.anyWaiting || this.cost.status != 'Open') {
        return
      }
      this.waitings.rejecting = true
      var message = this.modelToCost(this.model)
      message.status = 'Rejected'
      message.closedBy = this.email
      this.$http.post(this.server + '/myapp/update-cost/' + this.costId + '/', message).then(resp => {
        this.getCost()
        this.waitings.approving = false
      }, err => {
        this.error = err.body
        this.waitings.approving = false
      })
    },
    deleteCost () {
      var confirm = {
        title: 'Delete Invoice',
        message: 'Are you sure to delete this invoice? You CANNOT restore it after the deletion.',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.deleteCostConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    deleteCostConfirmed () {
      if (this.anyWaiting) {
        return
      }
      this.waitings.deleting = true
      this.$http.post(this.server + '/myapp/delete-cost/' + this.costId + '/').then(resp => {
        this.$router.push('/invoices')
        this.waitings.deleting = false
      }, err => {
        this.error = err.body
        this.waitings.deleting = false
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
    sendEmail () {
      if (this.anyWaiting) {
        return
      }
      this.waitings.sendingEmail = true
      this.$http.post(this.server + '/myapp/send-email-for-cost/' + this.costId + '/').then(resp => {
        this.waitings.sendingEmail = false
      }, err => {
        this.error = err.body
        this.waitings.sendingEmail = false
      })
    },
  },
  mounted () {
    this.$nextTick(function () {
      this.getCost()
      this.getEmails()
    })
  },
}
</script>

<style scoped lang="scss">
 .model-select-container {
   .ui {
     height: 100%;
   }
 }
</style>
