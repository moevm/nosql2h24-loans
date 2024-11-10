<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required />
      </div>
      <Button text="Войти" @click="submitForm" />
    </form>
  </div>
</template>

<script>
import Button from '../components/Button.vue';

export default {
  components: {
    Button
  },
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    submitForm() {
      if (this.email === 'user@example.com' && this.password === '123') {
        localStorage.setItem('authToken', true);
        this.$router.push('/');
      } 
      else {
        alert('Неверный email или пароль');
      }
    }
  }
};
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

form {
  display: flex;
  flex-direction: column;
  max-width: 40%;
  width: 100%;
  padding: 2%;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 2%;
}

label {
  margin-bottom: 1%;
}

input {
  width: 100%;
  padding: 1%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
