<template>
  <div>
    <div v-for="(a, i) in attachments" :key="'attachment-section-' + i">
      <attachment :attachmentId="a" :canEdit="canEdit" @delete-attachment="deleteAttachment" />
    </div>
    <div class="upload-block" v-if="canEdit">
      <div class="field has-addons">
        <div class="control">
          <div class="file has-name">
            <label class="file-label">
              <input class="file-input" type="file" accept="application/pdf" @change="onFileChange">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label">
                  New Attachment
                </span>
              </span>
              <span class="file-name">
                {{file ? file.name : 'Choose a file...'}}
              </span>
            </label>
          </div>
        </div>
        <div class="control">
          <button class="button" :class="{'is-loading': waiting}" :disabled="!file" @click="upload">
            Upload
          </button>
        </div>
      </div>
      <div v-if="error" class="notification is-danger is-light">
        <button class="delete" @click="error=''"></button>
        {{error}}
      </div>
    </div>
  </div>
</template>

<script>
import Attachment from './Attachment'

export default {
  name: 'attachments',
  components: {
    Attachment,
  },
  props: ['attachments', 'canEdit'],
  data () {
    return {
      file: null,
      waiting: false,
      error: '',
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    email () {
      return this.$store.state.user.email
    },
  },
  methods: {
    onFileChange (e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.file = files[0];
    },
    upload () {
      if (!this.file || this.waiting) {
        return
      }
      this.waiting = true
      this.error = ''
      this.getS3UploadUrl()
    },
    getS3UploadUrl () {
      var message = {filename: this.file.name}
      this.$http.post(this.server + '/myapp/get-s3-upload-url/', message).then(resp => {
        this.uploadFileToS3(resp.body)
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    uploadFileToS3 (uploadUrl) {
      const axios = require('axios')
      var formData = new FormData();
      Object.keys(uploadUrl.fields).forEach((key) => {
        formData.append(key, uploadUrl.fields[key])
      })
      formData.append('file', this.file)
      var vm = this
      axios.post(uploadUrl.url, formData, {'Content-Type': 'multipart/form-data'}).then(resp => {
        vm.createAttachment(uploadUrl)
      }).catch(err => {
        vm.error = err.body
        vm.waiting = false
      })
    },
    createAttachment (uploadUrl) {
      var message = {
        name: this.file.name,
        s3Bucket: uploadUrl.bucket,
        s3Key: uploadUrl.key,
        createdBy: this.email,
      }
      this.$http.post(this.server + '/myapp/create-attachment/', message).then(resp => {
        this.$emit('new-attachment-created', resp.body)
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    deleteAttachment (attachmentId) {
      this.$emit('attachment-deleted', attachmentId)
    },
  },
}
</script>
