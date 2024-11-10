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
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    background-color: #4CAF50;
    color: white;
  }
  </style>
  