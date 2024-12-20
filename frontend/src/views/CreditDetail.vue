<template>
  <div class="credit-detail">
    <h1>Детали кредита</h1>
    <div v-if="request">
      <div><strong>Название кредита:</strong> {{ request.loan_name }}</div>
      <div><strong>Дата открытия:</strong> {{ formatDateTime(request.opening_date) }}</div>
      <div><strong>Сумма:</strong> {{ request.amount }} руб.</div>
      <div><strong>Ставка:</strong> {{ request.interest_rate }} %</div>
      <div><strong>Срок:</strong> {{ request.expiration_time }} мес.</div>
      <div><strong>Задолженность:</strong> {{ request.debt }} руб.</div>
      <div><strong>Ежемесячный платеж:</strong> {{ request.monthly_payment }} руб.</div>
      <div><strong>Дата следующего платежа:</strong> {{ formatDate(request.next_payment_date) }}</div>
    </div>
    <div v-else>
      <p>Кредит не найден.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreditDetail',
  data() {
    return {
      request: null
    };
  },
  created() {
    this.getCreditDetails();
  },
  mounted() {
    document.title = "Детали кредита";
  },
  methods: {
    async getCreditDetails() {
      try {
        const creditId = localStorage.getItem('creditId');
        const response = await axios.get('http://127.0.0.1:5000/get_credit_details', {
          params: {
            creditId: creditId
          }
        });
        this.request = response.data;
      } catch (error) {
        console.log('Ошибка при получении данных кредита:', error);
      }
    },
    formatDateTime(date) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      };
      return new Date(date).toLocaleString('ru-RU', options);
    },
    formatDate(date) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      };
      return new Date(date).toLocaleString('ru-RU', options);
    }
  }
};
</script>

<style scoped>
.credit-detail {
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