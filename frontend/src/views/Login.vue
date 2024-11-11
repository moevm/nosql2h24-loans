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
      <Button text="Войти" />
    </form>
  </div>
</template>

<script>
import Button from '../components/Button.vue';
import axios from 'axios';

export default {
  name: 'Login',
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
    async submitForm() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        });
        
        if (response.data.token) {
          localStorage.setItem('authToken', true);
          localStorage.setItem('userId', response.data.userId);
          localStorage.setItem('userType', response.data.userType);
          this.$router.push(`/${response.data.userType}/main`);
        }
      } 
      catch (error) {
        if (error.response && error.response.status === 401) {
          alert('Неверный email или пароль'); 
        } 
        else {
          alert('Произошла ошибка. Пожалуйста, попробуйте позже.');
          console.log(error);
        }
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
