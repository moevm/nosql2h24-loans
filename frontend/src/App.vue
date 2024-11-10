<template>
  <div id="app">
    <NavBar /> <!-- Ваш компонент навигации -->
    <router-view /> <!-- Здесь будут отображаться компоненты в зависимости от маршрута -->
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'; // Импортируем NavBar

export default {
  name: 'App',
  components: {
    NavBar
  }
};
</script>

<style>
/* Добавьте глобальные стили, если необходимо */
</style>