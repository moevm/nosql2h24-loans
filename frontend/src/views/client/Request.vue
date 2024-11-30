<template>
  <div class="client-request">
    <h1>Заявки</h1>
    <p>Здесь можно посмотреть заявки.</p>

    <table class="extended-table">
      <thead>
        <tr>
          <th>
            <label>Название кредита</label>
            <div class="filter-options">
              <input type="checkbox" v-model="filters.loan_name.option1" /> Молодежный кредит
              <input type="checkbox" v-model="filters.loan_name.option2" /> Ипотека
              <input type="checkbox" v-model="filters.loan_name.option3" /> Кредит наличными
              <input type="checkbox" v-model="filters.loan_name.option4" /> Автокредит
              <input type="checkbox" v-model="filters.loan_name.option5" /> Рефинансирование
              <input type="checkbox" v-model="filters.loan_name.option6" /> Кредитная карта
            </div>
          </th>
          <th>
            <label>Дата заявки</label>
            <div class="filter-options">
              <input type="date" v-model="filters.date_from" />
              <span>—</span>
              <input type="date" v-model="filters.date_to" />
            </div>
          </th>
          <th>
            <label>Статус</label>
            <div class="filter-options">
              <input type="checkbox" v-model="filters.status.status1" /> Статус 1
              <input type="checkbox" v-model="filters.status.status2" /> Статус 2
              <input type="checkbox" v-model="filters.status.status3" /> Статус 3
            </div>
          </th>
          <th>
            <label>Сумма</label>
            <div class="filter-options">
              <input type="number" v-model="filters.amount_from" placeholder="от" />
              <span>—</span>
              <input type="number" v-model="filters.amount_to" placeholder="до" />
            </div>
          </th>
          <th>
            <label>Ставка</label>
            <div class="filter-options">
              <input type="number" v-model="filters.rate_from" placeholder="от" />
              <span>—</span>
              <input type="number" v-model="filters.rate_to" placeholder="до" />
            </div>
          </th>
          <th>
            <label>Срок</label>
            <div class="filter-options">
              <input type="number" v-model="filters.term_from" placeholder="от" />
              <span>—</span>
              <input type="number" v-model="filters.term_to" placeholder="до" />
            </div>
          </th>
        </tr>
        <tr>
          <th @click="sortRequests('loan_name')">
            Название кредита
            <SortArrow :sortDirection="sortDirection.loan_name" />
          </th>
          <th @click="sortRequests('request_time')">
            Дата заявки
            <SortArrow :sortDirection="sortDirection.request_time" />
          </th>
          <th @click="sortRequests('status')">
            Статус
            <SortArrow :sortDirection="sortDirection.status" />
          </th>
          <th @click="sortRequests('amount')">
            Сумма
            <SortArrow :sortDirection="sortDirection.amount" />
          </th>
          <th @click="sortRequests('interest_rate')">
            Ставка
            <SortArrow :sortDirection="sortDirection.interest_rate" />
          </th>
          <th @click="sortRequests('expiration_time')">
            Срок
            <SortArrow :sortDirection="sortDirection.expiration_time" />
          </th>
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
    <button @click="applyFilters" class="filter-button">Применить фильтры</button>
  </div>
</template>

<script>
import axios from 'axios';
import SortArrow from '../../components/SortArrow.vue';

export default {
  name: 'ClientRequest',
  components: {
    SortArrow
  },
  data() {
    return {
      requests: [],
      sortDirection: {
        loan_name: 0, 
        request_time: 0,
        status: 0,
        amount: 0,
        interest_rate: 0,
        expiration_time: 0
      },
      filters: {
        loan_name: {
          option1: false,
          option2: false,
          option3: false,
          option4: false,
          option5: false,
          option6: false,
        },
        date_from: '',
        date_to: '',
        status: {
          status1: false,
          status2: false,
          status3: false,
        },
        amount_from: '',
        amount_to: '',
        rate_from: '',
        rate_to: '',
        term_from: '',
        term_to: ''
      },
      sortField: 'loan_name'
    };
  },
  created() {
    this.getRequests();
  },
  methods: {
    async getRequests() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/credit_request', {
          params: {
            client_id: userId,
          }
        });
        this.requests = response.data; 
      } catch (error) {
        console.error('Ошибка при получении заявок:', error); 
      }
    },
    async applyFilters() {
      const userId = localStorage.getItem('userId');
      const name = "Автокредит"
      try {
        const response = await axios.get('http://127.0.0.1:5000/filter_credit_request', {
          params: {
            client_id: userId,
            loan_name: name
          }
        });
        this.requests = response.data;
      } catch (error) {
        console.error('Ошибка при применении фильтров:', error);
      }
    },
    async fetchRequests() {
      const userId = localStorage.getItem('userId');
      const sortDirection = this.sortDirection;
      const sortField = this.sortField;
      try {
        const response = await axios.get('http://127.0.0.1:5000/sort_credit_request', {
          params: {
            client_id: userId, 
            sort_field: sortField, 
            sort_direction: sortDirection[sortField]
          }
        });
        this.requests = response.data;
      } catch (error) {
        console.error('Ошибка при получении заявок:', error); 
      }
    },
    sortRequests(field) {
      const previousSortDirection = this.sortDirection[field];
      if (this.sortField === field) {
        this.sortDirection[field] = previousSortDirection === 1 ? -1 : 1;
      } else {
        this.sortField = field;
        this.sortDirection[field] = 1;
      }
      Object.keys(this.sortDirection).forEach(key => {
        if (key !== field) {
          this.sortDirection[key] = 0;
        }
      });
      this.fetchRequests();
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
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

table.extended-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ccc;
  padding: 15px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  cursor: pointer;
}

th label {
  font-size: 14px;
  font-weight: bold;
}

th .filter-options {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

th .filter-options input {
  margin-bottom: 5px;
}

th .filter-options span {
  margin: 0 5px;
}

.filter-button {
  padding: 15px 25px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.filter-button:hover {
  background-color: #45a049;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #e2e2e2;
}

span {
  padding: 0 5px;
}
</style>
