<template>
  <div class="container mt-5 px-2">
    <article class="message is-danger" v-if="!token">
      <div class="message-body">
        You have not signed in yet. Please go back to <a href="/">home page</a> to sign in first.
      </div>
    </article>
    <div v-if="token">
      <div>
        <router-link :to="'/new-invoice/new'" class="button is-pulled-right">
          <span class="icon">
            <i class="fas fa-plus"></i>
          </span>
          <span>New</span>
        </router-link>
        <h1 class="title">Invoices</h1>
      </div>
      <div class="columns mt-4">

        <div class="column field mb-0 pb-0">
          <p class="control has-icons-left">
            <span class="select">
              <select v-model="filter">
                <option :value="'my'">My Invoices</option>
                <option :value="'all'">All Invoices</option>
              </select>
            </span>
            <span class="icon is-small is-left">
              <i class="fas fa-filter"></i>
            </span>
          </p>
        </div>
        <div class="column field  mb-0 pb-0">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Search in invoice#, vendor, subject and tags" v-model="search">
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
                <th class="is-clickable" @click="changeSortOption('invoiceNumber')">
                  <span>Invoice Number</span>
                  <span class="icon" v-if="sortOption.field == 'invoiceNumber'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('vendorName')">
                  <span>Vendor</span>
                  <span class="icon" v-if="sortOption.field == 'vendorName'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('subject')">
                  <span>Subject</span>
                  <span class="icon" v-if="sortOption.field == 'subject'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable has-text-right" @click="changeSortOption('amount')">
                  <span>Amount</span>
                  <span class="icon" v-if="sortOption.field == 'amount'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('status')">
                  <span>Status</span>
                  <span class="icon" v-if="sortOption.field == 'status'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('subsidiary')">
                  <span>Subsidiary</span>
                  <span class="icon" v-if="sortOption.field == 'subsidiary'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('tags')">
                  <span>Tags</span>
                  <span class="icon" v-if="sortOption.field == 'tags'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('createdAt')">
                  <span>Created At</span>
                  <span class="icon" v-if="sortOption.field == 'createdAt'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('createdBy')">
                  <span>Created By</span>
                  <span class="icon" v-if="sortOption.field == 'createBy'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
                <th class="is-clickable" @click="changeSortOption('reviewers')">
                  <span>Reviewer</span>
                  <span class="icon" v-if="sortOption.field == 'reviewers'">
                    <i class="fas" :class="{'fa-sort-up': sortOption.asc, 'fa-sort-down': !sortOption.asc}"></i>
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="is-clickable" v-for="(c, i) in showingCosts" :key="'cost-' + c.id" @click="viewCost(c)">
                <td>{{c.id}}</td>
                <td>{{c.invoiceNumber}}</td>
                <td>{{c.vendorName}}</td>
                <td>{{c.subject}}</td>
                <td class="has-text-right">{{c.amount}}</td>
                <td>
                  <span class="tag is-link" v-if="c.status == 'Open'">Open</span>
                  <span class="tag is-success" v-if="c.status == 'Approved'">Approved</span>
                  <span class="tag is-warning" v-if="c.status == 'Rejected'">Rejected</span>
                  <span class="tag is-dark" v-if="c.status == 'NS Bill Created'">NS Bill Created</span>
                </td>
                <td>{{c.subsidiary}}</td>
                <td>
                  <span v-for="(t, j) in c.tags" :key="'tag-' + i + '-' + j">
                    <span class="tag is-info">{{t}}</span>&nbsp;
                  </span>
                </td>
                <td>{{c.createdAt}}</td>
                <td>{{c.createdBy}}</td>
                <td>{{c.reviewers}}</td>
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
  name: 'Costs',
  data () {
    return {
      error: '',
      waiting: false,
      search: '',
      filter: '',
      costs: []
    }
  },
  computed: {
    server () {
      return this.$store.state.config.server
    },
    token () {
      return this.$store.state.user.token
    },
    searchOption () {
      return this.$store.state.costs.searchOption
    },
    sortOption () {
      return this.$store.state.costs.sortOption
    },
    filterOption () {
      return this.$store.state.costs.filterOption
    },
    showingCosts () {
      var search = this.search.trim().toLowerCase()
      var filteredCosts = this.costs.filter(c => {
        return c.subject.toLowerCase().includes(search)
          || c.tags.toLowerCase().includes(search)
          || c.invoiceNumber.toLowerCase().includes(search)
          || c.vendorName.toLowerCase().includes(search)
      })
      var sort = this.sortOption
      var sortedCosts = filteredCosts.sort((a, b) => {
        var va = a[sort.field]
        var vb = b[sort.field]
        if (sort.field == 'id' || sort.field == 'amount' || sort.field == 'createdAt') {
          return sort.asc ? va - vb : vb - va
        }
        return sort.asc ? va.localeCompare(vb) : vb.localeCompare(va)
      })
      return sortedCosts.map(c => {
        return {
          id: c.id,
          subject: c.subject,
          amount: c.amount,
          status: c.status,
          tags: c.tags.split(',').filter(t => t),
          createdAt: dateFormat(new Date(c.createdAt * 1000), 'mm/dd/yyyy'),
          createdBy: c.createdBy,
          reviewers: c.reviewers,
          invoiceNumber: c.invoiceNumber,
          vendorName: c.vendorName,
          subsidiary: c.subsidiary,
        }
      })
    },
  },
  watch: {
    search: function (val) {
      this.$store.commit('costs/setSearchOption', val)
    },
    filter: function (val) {
      this.$store.commit('costs/setFilterOption', val)
    },
    filterOption: function (val) {
      this.getCosts()
    },
  },
  methods: {
    getCosts () {
      this.waiting = true
      var params = {filterOption: this.filterOption}
      this.$http.get(this.server + '/myapp/get-costs/', {params: params}).then(resp => {
        this.costs = resp.body
        this.waiting = false
      }, err => {
        this.error = err.body
        this.waiting = false
      })
    },
    changeSortOption (field) {
      this.$store.commit('costs/setSortOption', {
        field: field,
        asc: field == this.sortOption.field ? !this.sortOption.asc : true
      })
    },
    viewCost (cost) {
      this.$router.push('/invoice/' + cost.id)
    },
  },
  mounted () {
    this.$nextTick(function () {
      this.getCosts()
    })

    this.search = this.searchOption
    this.filter = this.filterOption
  },
}
</script>
