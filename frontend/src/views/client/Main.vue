<template>
  <div class="main-container">
    <div class="welcome-message">
      <h2>Добро пожаловать, {{ userName }}!</h2>
    </div>
    <div class="loan-options">
      <div class="loan-card">
        <h3>Молодежный кредит</h3>
        <p>До 6 000 000 ₽</p>
        <p>До 25 лет</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Молодежный кредит')" />
      </div>
      <div class="loan-card">
        <h3>Ипотека</h3>
        <p>До 30 000 000 ₽</p>
        <p>До 30 лет</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Ипотека')" />
      </div>
      <div class="loan-card">
        <h3>Кредит наличными</h3>
        <p>До 30 000 000 ₽</p>
        <p>До 15 лет</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Кредит наличными')" />
      </div>
      <div class="loan-card">
        <h3>Автокредит</h3>
        <p>До 8 000 000 ₽</p>
        <p>До 5 лет</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Автокредит')" />
      </div>
      <div class="loan-card">
        <h3>Рефинансирование</h3>
        <p>До 5 000 000 ₽</p>
        <p>До 5 лет</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Рефинансирование')" />
      </div>
      <div class="loan-card">
        <h3>Кредитная карта</h3>
        <p>До 1 000 000 ₽</p>
        <p>До 12 месяцев</p>
        <Button text="Оформить" buttonType="button" @click.native="navigateToLoanApplication('Кредитная карта')" />
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../../components/Button.vue';

export default {
  name: 'ClientMain',
  components: {
    Button
  },
  computed: {
    userName() {
      return localStorage.getItem('userName') || 'Пользователь';
    }
  },
  methods: {
    navigateToLoanApplication(loanType) {
      this.$router.push({ path: '/client/loan-application', query: { loanType } });
    }
  },
  mounted() {
    document.title = "Главная";
  }
};
</script>

<style scoped>
.main-container {
  text-align: center;
  padding: 20px;
}

h1 {
  font-size: 2em;
  color: #9A1750;
}

nav ul {
  list-style-type: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin: 0 15px;
}

nav ul li a {
  text-decoration: none;
  color: #9A1750;
  font-weight: bold;
}

.welcome-message h2 {
  margin-top: 20px;
}

.loan-options {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 20px;
}

.loan-card {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin: 10px;
  padding: 20px;
  width: 30%; 
  box-sizing: border-box; 
  text-align: center;
}

.loan-card h3 {
  margin-bottom: 10px;
}

.loan-card p {
  margin: 5px 0;
}
</style>
