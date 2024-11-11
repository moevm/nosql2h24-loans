<template>
  <nav>
    <ul>
      <li><router-link to="/">SCAM-BANK</router-link></li>
      <li><router-link to="/credit">Кредиты</router-link></li>
      <li><router-link to="/request">Заявки</router-link></li>
      <li><router-link to="/profile">Профиль</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
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
}

a:hover {
  text-decoration: underline;
}
</style>