<template>
  <div class="container mt-5 px-2">
    <article class="message is-danger" v-if="!token">
      <div class="message-body">
        You have not signed in yet. Please go back to <a href="/">home page</a> to sign in first.
      </div>
    </article>
    <div v-if="token">
      <div>
        <h1 class="title">Products</h1>
      </div>
      <div class="columns mt-4">

        <div class="column field mb-0 pb-0">
          <p class="control has-icons-left">
            <span class="select">
              <select v-model="filter">
                <option :value="'all'">All Products{{filter == 'all' ? ' (' + showingProducts.length + ')' : ''}}</option>
                <option :value="'out of stock'">Out of Stock{{filter == 'out of stock' ? ' (' + showingProducts.length + ')' : ''}}</option>
              </select>
            </span>
            <span class="icon is-small is-left">
              <i class="fas fa-filter"></i>
            </span>
          </p>
        </div>
        <div class="column field  mb-0 pb-0">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Search in product name, model" v-model="search">
            <span class="icon is-small is-left">
              <i class="fas fa-search"></i>
            </span>
          </p>
        </div>
      </div>
      <div class="mt-3">
        <div v-if="waiting">
          <span class="icon is-medium is-size-4">
            <i class="fas fa-spinner fa-pulse"></i>
          </span>
        </div>
        <div v-else>
          <table class="table is-fullwidth is-hoverable is-striped">
            <thead>
              <tr>
                <th class="is-clickable" @click="changeSortOption('id')">
                  <span>Id</span>
                  <span class="icon" v-if="sortOption.field == 'id'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <!--<th class="is-clickable" @click="changeSortOption('name')">
                  <span>Name</span>
                  <span class="icon" v-if="sortOption.field == 'name'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>-->
                <th class="is-clickable" @click="changeSortOption('model')">
                  <span>Model</span>
                  <span class="icon" v-if="sortOption.field == 'model'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable has-text-right" @click="changeSortOption('homeDepotPriceValue')">
                  <span>Home Depot</span>
                  <span class="icon" v-if="sortOption.field == 'homeDepotPriceValue'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable has-text-right" @click="changeSortOption('homeDepotPriceLatestChange')">
                  <span>Change From</span>
                  <span class="icon" v-if="sortOption.field == 'homeDepotPriceLatestChange'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable has-text-right" @click="changeSortOption('wayfairPriceValue')">
                  <span>Wayfair</span>
                  <span class="icon" v-if="sortOption.field == 'wayfairPriceValue'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable has-text-right" @click="changeSortOption('wayfairPriceLatestChange')">
                  <span>Change From</span>
                  <span class="icon" v-if="sortOption.field == 'wayfairPriceLatestChange'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="is-clickable" v-for="(p, i) in showingProducts" :key="'product-' + i" @click="viewProduct(p)">
                <td>{{p.id}}</td>
                <!--<td>
                  <abbr v-if="p.nameAbbr" :title="p.name">{{p.nameAbbr}}</abbr>
                  <span v-if="!p.nameAbbr">{{p.name}}</span>
                </td>-->
                <td>
                  <abbr :title="p.name">{{p.model}}</abbr>
                </td>
                <td class="has-text-right">
                  <span class="tag is-danger" v-if="p.homeDepotPriceFlag == 'Out of Stock'">OOS</span>&nbsp;
                  <span class="is-size-5">{{p.homeDepotPriceLabel}}</span><br/>
                  <span class="is-size-7 has-text-grey">{{p.homeDepotPriceDate}}</span>
                </td>
                <td class="has-text-right">
                  <span v-if="p.homeDepotPriceLatestChange">
                    <span class="is-size-5">{{p.homeDepotPriceLatestChangePriceLabel}}</span>
                    <span class="icon is-size-5" :class="{'has-text-success': p.homeDepotPriceLatestChangeLabels[1] == '-', 'has-text-danger': p.homeDepotPriceLatestChangeLabels[1] == '+'}">
                      <i class="fas" :class="{'fa-arrow-up': p.homeDepotPriceLatestChangeLabels[1] == '+', 'fa-arrow-down': p.homeDepotPriceLatestChangeLabels[1] == '-'}"></i>
                    </span><br/>
                    <span class="is-size-7 has-text-grey">{{p.homeDepotPriceLatestChangeLabels[0]}}</span>
                  </span>
                </td>
                <td class="has-text-right">
                  <span class="tag is-danger" v-if="p.wayfairPriceFlag == 'Out of Stock'">OOS</span>&nbsp;
                  <span class="is-size-5">{{p.wayfairPriceLabel}}</span><br/>
                  <span class="is-size-7 has-text-grey">{{p.wayfairPriceDate}}</span>
                </td>
                <td class="has-text-right">
                  <span v-if="p.wayfairPriceLatestChange">
                    <span class="is-size-5">{{p.wayfairPriceLatestChangePriceLabel}}</span>
                    <span class="icon is-size-5" :class="{'has-text-success': p.wayfairPriceLatestChangeLabels[1] == '-', 'has-text-danger': p.wayfairPriceLatestChangeLabels[1] == '+'}">
                      <i class="fas" :class="{'fa-arrow-up': p.wayfairPriceLatestChangeLabels[1] == '+', 'fa-arrow-down': p.wayfairPriceLatestChangeLabels[1] == '-'}"></i>
                    </span><br/>
                    <span class="is-size-7 has-text-grey">{{p.wayfairPriceLatestChangeLabels[0]}}</span>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
  name: 'Products',
  data () {
    return {
      error: '',
      waiting: false,
      search: '',
      filter: 'all',
      sortOption: { field: 'homeDepotPriceLatestChange', asc: false },
      costs: [],
      products: [],
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    token () {
      return this.$store.state.user.token
    },
    filterOption () {
      return this.$store.state.products.filterOption
    },
    showingProducts () {
      var search = this.search.trim().toLowerCase()
      var filteredProducts = this.products.filter(p => {
        return p.product.name.toLowerCase().includes(search)
          || p.product.model.toLowerCase().includes(search)
      })
      var vm = this
      var transformedProducts = filteredProducts.map(p => {
        var homeDepotPrice = vm.findChannelPrice(p, 'Home Depot')
        var wayfairPrice = vm.findChannelPrice(p, 'Wayfair')
        return {
          id: p.product.id,
          name: p.product.name,
          nameAbbr: p.product.name.length > 40 ? p.product.name.slice(0, 40) + '...' : '',
          model: p.product.model,
          homeDepotPriceValue: homeDepotPrice.value,
          homeDepotPriceLabel: homeDepotPrice.label,
          homeDepotPriceDate: homeDepotPrice.date,
          homeDepotPriceFlag: homeDepotPrice.flag,
          homeDepotPriceLatestChange: homeDepotPrice.latestChange,
          homeDepotPriceLatestChangeLabels: homeDepotPrice.latestChangeLabels,
          homeDepotPriceLatestChangePriceLabel: (homeDepotPrice.latestChangeLabels && homeDepotPrice.latestChangeLabels[2]) ? '$' + homeDepotPrice.latestChangeLabels[2].toLocaleString('en-US', {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2,
            useGrouping: false
          }) : '',
          wayfairPriceValue: wayfairPrice.value,
          wayfairPriceLabel: wayfairPrice.label,
          wayfairPriceDate: wayfairPrice.date,
          wayfairPriceFlag: wayfairPrice.flag,
          wayfairPriceLatestChange: wayfairPrice.latestChange,
          wayfairPriceLatestChangeLabels: wayfairPrice.latestChangeLabels,
          wayfairPriceLatestChangePriceLabel: (wayfairPrice.latestChangeLabels && wayfairPrice.latestChangeLabels[2]) ? '$' + wayfairPrice.latestChangeLabels[2].toLocaleString('en-US', {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2,
            useGrouping: false
          }) : '',
        }
      })

      if (this.filterOption == 'out of stock') {
        transformedProducts = transformedProducts.filter(p => p.homeDepotPriceFlag == 'Out of Stock' || p.wayfairPriceFlag == 'Out of Stock')
      }
      
      var sort = this.sortOption
      var sortedProducts = transformedProducts.sort((a, b) => {
        var va = a[sort.field]
        var vb = b[sort.field]
        if (va == null || vb == null) {
          if (va) {
            return sort.asc ? 1 : -1
          }
          if (vb) {
            return sort.asc ? -1 : 1
          }
          return 0
        }
        if (sort.field == 'id' || sort.field == 'homeDepotPriceValue' || sort.field == 'wayfairPriceValue') {
          return sort.asc ? va - vb : vb - va
        }
        return sort.asc ? va.localeCompare(vb) : vb.localeCompare(va)
      })
      return sortedProducts
    },
  },
  watch: {
    filter: function (val) {
      this.$store.commit('products/setFilterOption', val)
    },
  },
  methods: {
    getProducts () {
      this.waiting = true
      this.$http.get(this.server + '/myapp/get-products-with-latest-prices/').then(resp => {
        this.products = resp.body
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    findChannelPrice (product, channelName) {
      var homeDepotChannel = product.channels.find(c => {
         return c.channel.name == channelName
      })
      if (!homeDepotChannel || !homeDepotChannel.latestPrice) {
        return {}
      }
      var price = homeDepotChannel.latestPrice
      return {
        value: price.price,
        label: '$' + price.price.toLocaleString('en-US', {
          maximumFractionDigits: 2,
          minimumFractionDigits: 2,
          useGrouping: false
        }),
        date: price.date,
        flag: price.flag,
        latestChange: price.latestChange,
        latestChangeLabels: price.latestChange ? price.latestChange.split(',') : [],
      }
    },
    changeSortOption (field) {
      this.sortOption = {
        field: field,
        asc: field == this.sortOption.field ? !this.sortOption.asc : true
      }
    },
    viewProduct (product) {
      this.$router.push('/product/' + product.id)
    },
  },
  mounted () {
     this.getProducts()
     this.filter = this.filterOption
  },
}
</script>

<style scoped>
</style>
