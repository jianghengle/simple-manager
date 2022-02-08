<template>
  <div id="app" class="mb-6">
    <Header/>
    <router-view/>
    <confirm-modal></confirm-modal>
  </div>
</template>

<script>
import Header from '@/views/Header.vue'
import ConfirmModal from '@/components/modals/ConfirmModal'

export default {
  components: {
    Header,
    ConfirmModal
  }
}

</script>

<style lang="scss">
@import "~bulma";


</style>
