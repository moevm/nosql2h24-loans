<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="email">Email:</label>
      <input type="email" v-model="email" required />
    </div>
    <div>
      <label for="password">Password:</label>
      <input type="password" v-model="password" required />
    </div>
    <button type="submit">Login</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    submitForm() {
      this.$emit('login', { email: this.email, password: this.password });
    }
  }
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: 0 auto;
}

input {
  margin: 10px 0;
  padding: 8px;
}
</style>
