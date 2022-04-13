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
          <li><router-link :to="'/products'">Products</router-link></li>
          <li class="is-active"><a href="#" aria-current="page">{{productId}}</a></li>
        </ul>
      </nav>
      <div class="mt-3">
        <div v-if="waiting || !product">
          <span class="icon is-medium is-size-4">
            <i class="fas fa-spinner fa-pulse"></i>
          </span>
        </div>
        <div v-else>
          <div class="field mt-3">
            <label class="label">Name</label>
            <div class="control">
              <input class="input" type="text" v-model="product.name" readonly>
            </div>
          </div>
          <div class="field mt-3">
            <label class="label">Model</label>
            <div class="control">
              <input class="input" type="text" v-model="product.model" readonly>
            </div>
          </div>
          <div class="field mt-3">
            <label class="label">Home Depot Item Id</label>
            <div class="control">
              <input class="input" type="text" v-model="product.homeDepotItemId" readonly>
            </div>
          </div>

          <div>
            <h1 class="title is-5 mt-6">Price Table</h1>
            <table class="table is-fullwidth is-striped">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Date</th>
                  <th v-for="(c, i) in channels" :key="'col-header-' + i">
                    {{c.channel.name}}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(d, i) in dates" :key="'row-date-' + i">
                  <td>{{i + 1}}</td>
                  <td class="price-date">{{d}}</td>
                  <td v-for="(c, j) in channels" :key="'row-' + i + '-' + j">
                    <span v-if="datePriceMap[d][c.channel.id]">
                      <span>{{datePriceMap[d][c.channel.id].priceLabel}}</span>&nbsp;
                      <span :class="{'has-text-success': datePriceMap[d][c.channel.id].flag == 'DOWN', 'has-text-danger': datePriceMap[d][c.channel.id].flag == 'UP'}">
                        <i class="fas" :class="{'fa-arrow-up': datePriceMap[d][c.channel.id].flag == 'UP', 'fa-arrow-down': datePriceMap[d][c.channel.id].flag == 'DOWN'}"></i>
                      </span>
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
import dateFormat from 'dateformat'

export default {
  name: 'Product',
  data () {
    return {
      error: '',
      waiting: false,
      product: null,
      channels: null,
      latestPrices: [],
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    token () {
      return this.$store.state.user.token
    },
    productId () {
      return this.$route.params.productId
    },
    channelMap () {
      if (!this.channels) {
        return {}
      }
      var channelMap = {}
      for (var channel of this.channels) {
        channelMap[channel.channel.id] = channel.channel.name
      }
      return channelMap
    },
    datePriceMap () {
      if (!this.product || !this.channels) {
        return []
      }
      var datePriceMap = {}
      for (var channel of this.channels) {
        for (var price of channel.prices) {
          price.priceLabel = '$' + price.price.toLocaleString('en-US', {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2,
            useGrouping: false
          })
          var row = datePriceMap[price.date]
          if (row) {
            row[price.channelId] = price
          } else {
            datePriceMap[price.date] = {}
            datePriceMap[price.date][price.channelId] = price
          }
        }
      }
      for (var price of this.latestPrices) {
        price.priceLabel = '$' + price.price.toLocaleString('en-US', {
          maximumFractionDigits: 2,
          minimumFractionDigits: 2,
          useGrouping: false
        })
        var row = datePriceMap[price.date]
        if (row) {
          row[price.channelId] = price
        } else {
          datePriceMap[price.date] = {}
          datePriceMap[price.date][price.channelId] = price
        }
      }
      return datePriceMap
    },
    dates () {
      if (!this.datePriceMap) {
        return []
      }
      return Object.keys(this.datePriceMap).sort((a, b) => b.localeCompare(a))
    }
  },
  methods: {
    getProduct () {
      this.waiting = true
      this.$http.get(this.server + '/myapp/get-product-with-prices/' + this.productId + '/').then(resp => {
        this.product = resp.body.product
        this.channels = resp.body.channels
        for (const channel of this.channels) {
          this.updateLatestPrice(channel.channel)
        }
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    updateLatestPrice (channel) {
      this.$http.post(this.server + '/myapp/update-product-latest-price/' + this.productId + '/' + channel.id + '/', {}).then(resp => {
        this.latestPrices.push(resp.body)
      }, err => {
        this.error = err.body
      })
    },
  },
  mounted () {
    this.$nextTick(function(){
      this.getProduct()
    })
  },
}
</script>

<style scoped>
.price-date {
  white-space: nowrap;
}
</style>
