<template>
  <nav>
    <ul>
      <li v-if="isClient"><router-link to="/client/main">SCAM-BANK</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/main">SCAM-BANK</router-link></li>
      <li v-if="isClient"><router-link to="/client/credit">Кредиты</router-link></li>
      <!-- <li v-if="isAdmin"><router-link to="/admin/">Cтатистика</router-link></li> -->
      <li v-if="isClient"><router-link to="/client/request">Заявки</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/request">Заявки</router-link></li>
      <!-- <li v-if="isAdmin"><router-link to="/admin/">История</router-link></li> -->
      <li v-if="isClient"><router-link to="/client/profile">Профиль</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin/profile">Профиль</router-link></li>
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
  },
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
}

a:hover {
  text-decoration: underline;
}
</style>
