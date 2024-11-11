<template>
  <div class="client-request">
    <h1>Заявки</h1>
    <p>Здесь можно посмотреть заявки.</p>

    <table>
      <thead>
        <tr>
          <th>Название кредита</th>
          <th>Дата заявки</th>
          <th>Статус</th>
          <th>Сумма</th>
          <th>Ставка</th>
          <th>Срок</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request._id">
          <td>{{ request.loan_name }}</td>
          <td>{{ formatDate(request.request_time) }}</td>
          <td>{{ request.status }}</td>
          <td>{{ request.amount }}</td>
          <td>{{ request.interest_rate }}</td>
          <td>{{ request.expiration_time }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ClientRequest',
  data() {
    return {
      requests: []
    };
  },
  created() {
    this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get(`http://127.0.0.1:5000/credit_request?client_id=${userId}`);
        this.requests = response.data;
      } catch (error) {
        console.error('Ошибка при получении заявок:', error);
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
.client-request {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1, p {
  text-align: center;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #e2e2e2;
}
</style>
