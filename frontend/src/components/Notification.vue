<template>
    <div v-if="visible" class="notification-container">
      <div class="notification" :class="type">
        <p>{{ message }}</p>
        <button @click="closeNotification">Ок</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Notification",
    props: {
      message: {
        type: String,
        required: true,
      },
      type: {
        type: String,
        default: "info",
      },
      visible: {
        type: Boolean,
        default: false,
      },
    },
    methods: {
      closeNotification() {
        this.$emit("close");
      },
    },
  };
  </script>
  
  
  <style scoped>
  .notification-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 1000;
  }
  
  .notification {
    background-color: #f9f9f9;
    padding: 20px 30px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    max-width: 90%;
    width: 400px;
    font-family: Arial, sans-serif;
    color: #5d001e;
    font-size: 25px; 
  }
  
  .notification.success {
    border: 2px solid #e3afbc;
  }
  
  .notification.error {
    border: 2px solid #5d001e;
  }
  
  .notification button {
    margin-top: 20px;
    padding: 12px 25px;
    background-color: #5d001e;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
  }
  
  .notification button:hover {
    background-color: #e3afbc;
    color: #5d001e;
  }
  </style>
  