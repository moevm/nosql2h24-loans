<template>
  <button @click="handleClick">{{ text }}</button>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    }
  },
  methods: {
    handleClick() {
      this.$emit('click');
    }
  }
};
</script>

<style scoped>
button {
  padding: 1.5% 3%; 
  font-size: 1.2em; 
  cursor: pointer;
  border: none;
  background-color: #9A1750; 
  color: white; 
  border-radius: 4px; 
}
</style>