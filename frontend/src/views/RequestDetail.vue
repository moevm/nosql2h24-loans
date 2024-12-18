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
      <div><strong>Залог:</strong> {{ request.deposit }} руб.</div>

      <div v-if="request.co_borrowers && request.co_borrowers.length > 0">
        <br>
        <div><strong>Созаемщики:</strong></div>
        <br>
        <div v-for="co_borrower in request.co_borrowers" :key="co_borrower.name">
          <div><strong>Имя:</strong> {{ co_borrower.name }}</div>
          <div><strong>Место работы:</strong> {{ co_borrower.workplace }}</div>
          <div><strong>Должность:</strong> {{ co_borrower.post }}</div>
          <div><strong>Серия паспорта:</strong> {{ co_borrower.passport_series }}</div>
          <div><strong>Номер паспорта:</strong> {{ co_borrower.passport_number }}</div>
          <div><strong>Телефон:</strong> {{ co_borrower.phone }}</div>
          <br>
        </div>
      </div>
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
      try {
        const requestId = localStorage.getItem('requestId');
        const response = await axios.get('http://127.0.0.1:5000/get_request_details', {
          params: {
            requestId: requestId
          }
        });
        this.request = response.data;
        console.log('Данные заявки получены:', this.request.co_borrowers[0].name);
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
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

div {
  margin-bottom: 10px;
}

strong {
  font-weight: bold;
}

p {
  text-align: center;
  color: #9A1750;
}
</style>
