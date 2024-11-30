<template>
  <div class="form-container">
    <div class="header">
      <img src="../../public/favicon.png" class="logo" />
      <h1 class="title">SCAM-BANK</h1>
    </div>
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
    <div class="link-to-register">
      Еще нет аккаунта? 
      <router-link to="/register">Зарегистрируйтесь</router-link>
    </div>

    <Notification
      ref="notification"
      :message="notificationMessage"
      :type="notificationType"
      :visible="notificationVisible"
      @close="onNotificationClose"
    />
  </div>
</template>

<script>
import Button from '../components/Button.vue';
import axios from 'axios';
import Notification from '../components/Notification.vue';

export default {
  name: 'Login',
  components: {
    Button,
    Notification
  },
  data() {
    return {
      email: '',
      password: '',
      notificationMessage: '',
      notificationType: 'info',
      notificationVisible: false,
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
          localStorage.setItem('authToken', response.data.token);
          localStorage.setItem('userId', response.data.userId);
          localStorage.setItem('userType', response.data.userType);
          localStorage.setItem('userName', response.data.userName);

          this.$router.push(`/${response.data.userType}/main`);
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.showNotification('Неверный email или пароль', 'error');
        } else {
          this.showNotification('Произошла ошибка. Пожалуйста, попробуйте позже.', 'error');
          console.log(error);
        }
      }
    },

    showNotification(message, type) {
      this.notificationMessage = message;
      this.notificationType = type;
      this.notificationVisible = true;
    },

    onNotificationClose() {
      this.notificationVisible = false;
    },
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.logo {
  width: 60px;
  height: auto;
}

.title {
  font-size: 3rem;
  font-weight: bold;
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

.link-to-register {
  margin-top: 10px;
  text-align: center;
}

.link-to-register a {
  color: #9A1750;
  text-decoration: none;
}

.link-to-register a:hover {
  text-decoration: underline;
}
</style>
