<template>
  <div class="main-container">
    <h1>Добро пожаловать, {{ userName }}!</h1>
    <h2>У вас есть непросмотренные заявки!</h2>
    <h2>Вы можете посмотреть их <a href="/admin/request">здесь</a>.</h2>
  </div>
</template>

<script>
export default {
  name: 'AdminMain',
  computed: {
    userName() {
      return localStorage.getItem('userName') || 'Админ'; 
    }
  }
};
</script>

<style scoped>
.main-container {
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: auto;
}

h1, h2, h3, p {
  margin: 10px 0;
}

h1 {
  font-size: 2em;
  color: #333;
}

h2 {
  font-size: 1.5em;
  color: #555;
}
</style>
