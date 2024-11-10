<template>
  <div id="app">
    <NavBar v-if="!hideNavBar" />
    <router-view />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar
  },
  computed: {
    hideNavBar() {
      return this.$route.meta.hideNavBar;
    }
  }
};
</script>

<style>
</style>