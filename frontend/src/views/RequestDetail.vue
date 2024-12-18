<template>
    <div class="request-detail">
      <h1>Детали заявки</h1>
      <div v-if="request">
        <div><strong>Название кредита:</strong> {{ request.loan_name }}</div>
        <div><strong>Дата заявки:</strong> {{ formatDate(request.request_time) }}</div>
        <div><strong>Статус:</strong> {{ request.status }}</div>
        <div><strong>Сумма:</strong> {{ request.amount }} руб.</div>
        <div><strong>Ставка:</strong> {{ request.interest_rate }} %</div>
        <div><strong>Срок:</strong> {{ request.expiration_time }} мес.</div>
        <div><strong>Комментарий:</strong> {{ request.comment || 'Нет комментария' }}</div>
      </div>
      <div v-else>
        <p>Заявка не найдена.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'RequestDetail',
    data() {
      return {
        request: null
      };
    },
    created() {
      this.getRequestDetails();
    },
    methods: {
      async getRequestDetails() {
        const requestId = this.$route.params.id;
        try {
          const response = await axios.get(`http://127.0.0.1:5000/credit_request/${requestId}`);
          this.request = response.data;
        } catch (error) {
          console.log('Ошибка при получении данных заявки:', error);
        }
      },
  
      formatDate(date) {
        const options = {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        };
        return new Date(date).toLocaleString('ru-RU', options);
      }
    }
  };
  </script>
  
  <style scoped>
  .request-detail {
    padding: 20px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  div {
    margin-bottom: 10px;
  }
  
  strong {
    font-weight: bold;
  }
  
  p {
    text-align: center;
    color: red;
  }
  </style>
  