<template>
  <div>
    <h1>Добро пожаловать, user!</h1>
    <h2>Оформление кредита</h2>
    <ul>
      <li><router-link to="/loan-application">Оформить кредит 1</router-link></li>
      <li><router-link to="/loan-application">Оформить кредит 2</router-link></li>
      <li><router-link to="/loan-application">Оформить кредит 3</router-link></li>
      <li><router-link to="/loan-application">Оформить кредит 4</router-link></li>
      <li><router-link to="/loan-application">Оформить кредит 5</router-link></li>
      <li><router-link to="/loan-application">Оформить кредит 6</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Main'
};
</script>

<style scoped>
h1 {
  text-align: center;
}

h2 {
  text-align: center;
}

ul {
  list-style-type: none; /* Убираем маркеры списка */
  padding: 0;
}

li {
  text-align: center; /* Центрируем текст ссылок */
  margin: 10px 0; /* Отступы между ссылками */
}
</style>