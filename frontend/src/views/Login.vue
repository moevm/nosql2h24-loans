<template>
    <div>
      <h1>Вход</h1>
      <LoginForm @login="handleLogin" />
    </div>
  </template>
  
  <script>
  import LoginForm from '../components/LoginForm.vue';
  
  export default {
    name: 'Login',
    components: {
      LoginForm
    },
    methods: {
      handleLogin(userData) {
        // Здесь можно добавить логику для обработки входа пользователя
        console.log('Пользователь вошел:', userData);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Добавьте стили для страницы входа, если необходимо */
  </style>