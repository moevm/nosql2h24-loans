<template>
  <div class="client-request">
    <h1>Заявки</h1>
    <div class="button-container">
      <Button text="Отменить фильтрацию и сортировку" @click="resetFilters" buttonType="button" />
      <Button text="Применить фильтры" @click="applyFilters" buttonType="button" />
    </div>
    <table class="extended-table">
      <thead>
        <tr>
          <th>
            <div class="filter-options">
              <div>
                <input type="checkbox" v-model="loan_name" value="Молодежный кредит" />
                <label>Молодежный кредит</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Ипотека" />
                <label>Ипотека</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Кредит наличными" />
                <label>Кредит наличными</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Автокредит" />
                <label>Автокредит</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Рефинансирование" />
                <label>Рефинансирование</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Кредитная карта" />
                <label>Кредитная карта</label>
              </div>
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
            <div class="filter-options">
              <div>
                <input type="checkbox" v-model="status" value="processing" />
                <label>processing</label>
              </div>
              <div>
                <input type="checkbox" v-model="status" value="approved" />
                <label>approved</label>
              </div>
              <div>
                <input type="checkbox" v-model="status" value="rejected" />
                <label>rejected</label>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.amount_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.amount_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rate_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">%</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rate_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">%</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.term_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">мес.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.term_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">мес.</span>
              </div>
            </div>
          </th>
          <th></th> 
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
          <th>
            Ссылка
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
          <td>
            <button @click="goToRequestDetail(request._id)">🔗</button>
          </td>
        </tr>
      </tbody>
    </table>
    <Notification 
      :message="notificationMessage" 
      :type="notificationType" 
      :visible="isNotificationVisible" 
      @close="closeNotification" />
  </div>
</template>


<script>
import axios from 'axios';
import Button from '../../components/Button.vue';
import Notification from '../../components/Notification.vue';
import SortArrow from '../../components/SortArrow.vue';

export default {
  name: 'ClientRequest',
  components: {
    Button,
    SortArrow,
    Notification
  },
  data() {
    return {
      requests: [],
      loan_name: [],
      status: [],
      filters: {
        loan_name: '',
        date_from: '',
        date_to: '',
        status: '',
        amount_from: '',
        amount_to: '',
        rate_from: '',
        rate_to: '',
        term_from: '',
        term_to: ''
      },
      notificationMessage: '',
      notificationType: 'error',
      isNotificationVisible: false,
      sortDirection: {
        loan_name: 0, 
        request_time: 0,
        status: 0,
        amount: 0,
        interest_rate: 0,
        expiration_time: 0
      },
      sortField: 'loan_name'
    };
  },
  created() {
    this.getRequests();
  },
  mounted() {
    document.title = "Заявки";
  },
  methods: {
    async getRequests() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_credit_requests', {
          params: {
            client_id: userId
          }
        });
        this.requests = response.data;
      } catch (error) {
        console.log('Ошибка при получении заявок:', error);
      }
    },

    resetFilters() {
      this.loan_name = [],
      this.status = [],
      this.filters = {
        loan_name: '',
        date_from: '',
        date_to: '',
        status: '',
        amount_from: '',
        amount_to: '',
        rate_from: '',
        rate_to: '',
        term_from: '',
        term_to: ''
      };
      this.getRequests();
    },

    validateFilters() {
      if (this.filters.amount_from && this.filters.amount_to && this.filters.amount_from > this.filters.amount_to) {
        this.notificationMessage = 'Сумма "от" не может быть больше суммы "до"!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        return false;
      }
      if (this.filters.rate_from && this.filters.rate_to && this.filters.rate_from > this.filters.rate_to) {
        this.notificationMessage = 'Ставка "от" не может быть больше ставки "до"!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        return false;
      }
      if (this.filters.rate_to > 100) {
        this.notificationMessage = 'Ставка не может быть больше 100 %!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        return false;
      }
      if (this.filters.term_from && this.filters.term_to && this.filters.term_from > this.filters.term_to) {
        this.notificationMessage = 'Срок "от" не может быть больше срока "до"!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        return false;
      }
      if (this.filters.date_from && this.filters.date_to && this.filters.date_from > this.filters.date_to) {
        this.notificationMessage = 'Дата начала не может быть больше даты окончания!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        return false;
      }
      return true;
    },

    async applyFilters() {
      if (!this.validateFilters()) {
        return;
      }
      this.filters.loan_name = this.loan_name.join('@');
      this.filters.status = this.status.join('@');
      const filter = this.filters;
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/filter_credit_request', {
          params: {
            client_id: userId,
            ...filter
          }
        });
        this.requests = response.data;
        this.notificationMessage = 'Фильтры успешно применены!';
        this.notificationType = 'success';
        this.isNotificationVisible = true;
      } 
      catch (error) {
        this.notificationMessage = 'Ошибка при применении фильтров!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        console.log('Ошибка при применении фильтров:', error);
      }
    },

    closeNotification() {
      this.isNotificationVisible = false;
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
        this.notificationMessage = 'Ошибка при применении сортировки!';
        this.notificationType = 'error';
        this.isNotificationVisible = true;
        console.log('Ошибка при применении сортировки:', error); 
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
    },
    
    goToRequestDetail(requestId) {
      localStorage.setItem('requestId', requestId);
      this.$router.push('/request');
    }
  }
};
</script>

<style scoped>
.client-request {
  width: 80%;
  max-width: 1600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
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
  border: 1px solid #ddd;
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

th .filter-options div {
  display: flex;
  align-items: center;
}

th .filter-options input {
  margin-right: 8px;
}

th .filter-options span {
  margin: 0 5px;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #e0e0e0;
}

.button-container {
  display: flex;
  justify-content: center; 
  margin-top: 20px; 
}

.button-container Button {
  margin: 0 20px;
}

.filter-options {
  display: flex;
  justify-content: flex-start;
}

.filter-input-wrapper {
  display: flex;
  align-items: center;
}

.filter-input {
  margin-right: 5px;
  width: 100px;
}

.unit {
  margin-left: 5px;
  font-size: 14px;
  white-space: nowrap;
  flex-shrink: 0;
}
</style>