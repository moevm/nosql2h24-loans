<template>
  <nav>
    <ul>
      <li v-if="isClient"><router-link to="/client/main">SCAM-BANK</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/main">SCAM-BANK</router-link></li>
      <li v-if="isClient"><router-link to="/client/credit">Кредиты</router-link></li>
      <li v-if="isClient"><router-link to="/client/request">Заявки</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/statistics">Cтатистика</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/request">Заявки</router-link></li>
      <li v-if="isAdmin"><router-link to="/history">История</router-link></li>
      <li v-if="isClient && !isOnProfilePage"><router-link to="/client/profile">{{ userName }}</router-link></li>
      <li v-if="isAdmin && !isOnProfilePage"><router-link to="/admin/profile">{{ userName }}</router-link></li>
      <li v-if="isClient && isOnProfilePage"><a href="#" @click.prevent="logout">Выход</a></li>
      <li v-if="isAdmin && isOnProfilePage"><a href="#" @click.prevent="logout">Выход</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isClient() {
      return localStorage.getItem('userType') === 'client';
    },
    isAdmin() {
      return localStorage.getItem('userType') === 'admin';
    },
    userName() {
      return localStorage.getItem('userName') || 'Не найдено';
    },
    isOnProfilePage() {
      return this.$route.path === '/client/profile' || this.$route.path === '/admin/profile';
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
nav {
  background-color: #B6B6B6;
  padding: 2%;
}

ul {
  display: flex;
  list-style-type: none;
  gap: 5%;
  justify-content: center;
  width: 100%;
}

li {
  display: inline;
}

a {
  color: #9A1750;
  text-decoration: none;
  font-weight: bold;
  font-size: 25px;
}

a:hover{
  text-decoration: underline;
}
</style>