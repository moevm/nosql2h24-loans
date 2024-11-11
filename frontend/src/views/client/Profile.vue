<template>
  <div>
    <h1>Профиль</h1>
    <p>Здесь будет информация о вашем профиле.</p>
    <Button text="Выход" @click="logout" />
  </div>
</template>

<script>
import Button from '../../components/Button.vue';

export default {
  name: 'ClientProfile',
  components: {
    Button
  },
  methods: {
    logout() {
      localStorage.setItem('authToken', false);
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
</style>