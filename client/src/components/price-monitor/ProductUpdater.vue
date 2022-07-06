<template>
  <div>
    <p class="title is-4">Products Updater for price monitor</p>
    <p class="subtitle is-6">Retrieve <i>model, name, brand, homeDepotItemId, wayfairSku, wayfairOptionName</i> columns from CSV file to update products, deduped by the <i>model</i> column.</p>

    <div class="upload-block">
      <div class="field has-addons">
        <div class="control">
          <div class="file has-name">
            <label class="file-label">
              <input class="file-input" type="file" accept=".csv" @change="onFileChange">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
              </span>
              <span class="file-name">
                {{file ? file.name : 'Choose a CSV file...'}}
              </span>
            </label>
          </div>
        </div>
        <div class="control">
          <button class="button" :class="{'is-loading': waiting}" :disabled="!file" @click="updateProducts">
            Update Products
          </button>
        </div>
      </div>
      <div v-if="error" class="notification is-danger is-light">
        <button class="delete" @click="error=''"></button>
        {{error}}
      </div>
      <div v-if="success" class="notification is-success is-light">
        <button class="delete" @click="success=''"></button>
        {{success}}
      </div>
    </div>
  </div>
</template>

<script>
import { parse } from 'csv-parse/lib/sync'

export default {
  name: 'product-updater',
  data () {
    return {
      file: null,
      waiting: false,
      error: '',
      success: '',
      fieldNames: ['name', 'brand', 'model', 'homeDepotItemId', 'wayfairSku', 'wayfairOptionName']
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
  },
  methods: {
    onFileChange (e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.file = files[0];
    },
    updateProducts () {
      if (!this.file || this.waiting) {
        return
      }
      this.waiting = true
      this.error = ''

      var vm = this
      var reader = new FileReader()
      reader.onload = function () {
        var text = reader.result
        var records = parse(text, {
          columns: true,
        })
        vm.sendUpdates(records)
      }
      reader.readAsText(this.file)
      
    },
    sendUpdates (records) {
      var promises = []
      for (var record of records) {
        if (record['model']) {
          var message = {}
          for (const fieldName of this.fieldNames) {
            if (record[fieldName]) {
              message[fieldName] = record[fieldName].trim()
            }
          }
          promises.push(this.$http.post(this.server + '/myapp/update-product-by-model/', message))
        }
      }
      Promise.all(promises).then(resp => {
        this.success = 'Products have been all updated.'
        this.waiting = false
      }, err => {
        this.error = 'Some updates failed.'
      })
    },
  },
}
</script>
