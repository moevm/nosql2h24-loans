<template>
  <button :type="buttonType">{{ text }}</button>
</template>


<script>
export default {
  name: "Button",
  props: {
    text: {
      type: String,
      required: true
    },
  buttonType: { 
      type: String,
      default: 'submit'
    }
  }
};
</script>

<style scoped>
button {
  padding: 1.5% 3%; 
  font-size: 1.2em; 
  font-family: 'Georgia';
  cursor: pointer;
  border: none;
  background-color: #9A1750; 
  color: white; 
  border-radius: 4px; 
}
</style>