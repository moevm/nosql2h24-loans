<template>
  <div>
    <h1>Добро пожаловать, {{ userName }}!</h1>
    <h2>Оформление кредита</h2>
    <ul>
      <li><router-link to="/client/loan-application?loanType=Молодежный кредит">Оформить Молодежный кредит</router-link></li>
      <li><router-link to="/client/loan-application?loanType=Ипотека">Оформить Ипотека</router-link></li>
      <li><router-link to="/client/loan-application?loanType=Кредит наличными">Оформить Кредит наличными</router-link></li>
      <li><router-link to="/client/loan-application?loanType=Автокредит">Оформить Автокредит</router-link></li>
      <li><router-link to="/client/loan-application?loanType=Рефинансирование">Оформить Рефинансирование</router-link></li>
      <li><router-link to="/client/loan-application?loanType=Кредитная карта">Оформить Кредитная карта</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Main',
  computed: {
    userName() {
      // Получаем имя пользователя из localStorage
      return localStorage.getItem('userName') || 'Пользователь'; // Если имя не найдено, показываем 'Пользователь'
    }
  }
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
  list-style-type: none;
  padding: 0;
}

li {
  text-align: center;
  margin: 10px 0;
}
</style>
