<template>
  <div class="mb-5">
    <div v-if="error" class="notification is-danger is-light">
      <button class="delete" @click="error=''"></button>
      {{error}}
    </div>
    <div v-if="waiting">
      <span class="icon is-medium is-size-4">
        <i class="fas fa-spinner fa-pulse"></i>
      </span>
    </div>
    <div v-if="url">
      <div class="mb-1">
        <button v-if="canEdit" class="delete mt-1 is-pulled-right" @click="deleteAttachment"></button>
        <a class="attachment-name" :href="url" :download="attachment.name">{{attachment.name}}</a>
      </div>
      <div v-if="!isImage && iframeSource">
        <iframe class="my-doc" :src="iframeSource"></iframe>
      </div>
      <div v-if="isImage" class="my-image-container">
        <img class="my-image" :src="url" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'attachment',
  props: ['attachmentId', 'canEdit'],
  data () {
    return {
      attachment: null,
      url: null,
      waiting: false,
      error: '',
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    isImage () {
      if (!this.attachment) {
        return false
      }
      var ss = this.attachment.name.split('.')
      var ext = ss[ss.length - 1].toLowerCase()
      if (['png', 'jpg', 'jpeg', 'bmp', '.apng', 'gif'].includes(ext)) {
        return true
      }
      return false
    },
    iframeSource () {
      if (this.url) {
        var encodedUrl = encodeURIComponent(this.url);
        return "https://docs.google.com/gview?url=" + encodedUrl + "&embedded=true"
      }
    },
  },
  watch: {
    attachmentId: function (val) {
      this.getAttachment()
    },
    attachment: function (val) {
      this.getS3DownloadUrl()
    },
  },
  methods: {
    getAttachment () {
      this.waiting = true
      this.$http.get(this.server + '/myapp/get-attachment/' + this.attachmentId + '/').then(resp => {
        this.attachment = resp.body
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    getS3DownloadUrl () {
      this.waiting = true
      var message = {bucket: this.attachment.s3Bucket, key: this.attachment.s3Key}
      this.$http.post(this.server + '/myapp/get-s3-download-url/', message).then(resp => {
        this.url = resp.body.url
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    deleteAttachment () {
      var confirm = {
        title: 'Delete Attachment',
        message: 'Are you sure to delete this attachment?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.deleteAttachmentConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    deleteAttachmentConfirmed () {
      this.$emit('delete-attachment', this.attachmentId)
    }
  },
  mounted () {
    this.getAttachment()
  },
}
</script>

<style lang="scss" scoped>

.attachment-name {
  text-decoration: underline;
  margin-right: 15px;
}

.my-doc {
  width: 100%;
  height: 600px;
}
.my-image-container {
  width: 100%;
  max-height: 600px;

  .my-image {
    max-height: 100%;
    max-width:100%;
  }
}
</style>
