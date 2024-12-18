<template>
  <div class="admin-request">
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="isNotificationVisible"
      @close="closeNotification"
    />
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
                <label for="fio">ФИО:</label>
                <input type="text" v-model="filters.fio" id="fio" required />
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div>
                <input type="checkbox" v-model="loan_name" value="Молодежный кредит" id="loan_name_youth" />
                <label for="loan_name_youth">Молодежный кредит</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Ипотека" id="loan_name_mortgage" />
                <label for="loan_name_mortgage">Ипотека</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Кредит наличными" id="loan_name_cash" />
                <label for="loan_name_cash">Кредит наличными</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Автокредит" id="loan_name_auto" />
                <label for="loan_name_auto">Автокредит</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Рефинансирование" id="loan_name_refinance" />
                <label for="loan_name_refinance">Рефинансирование</label>
              </div>
              <div>
                <input type="checkbox" v-model="loan_name" value="Кредитная карта" id="loan_name_card" />
                <label for="loan_name_card">Кредитная карта</label>
              </div>
            </div>
          </th>
          <th>
            <label for="date_from">Дата заявки</label>
            <div class="filter-options">
              <input type="date" v-model="filters.date_from" id="date_from" />
              <span>—</span>
              <input type="date" v-model="filters.date_to" id="date_to" />
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.amount_from" placeholder="от" class="filter-input" id="amount_from" :min="0" />
                <span class="unit">руб.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.amount_to" placeholder="до" class="filter-input" id="amount_to" :min="0" />
                <span class="unit">руб.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rate_from" placeholder="от" class="filter-input" id="rate_from" :min="0"/>
                <span class="unit">%</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rate_to" placeholder="до" class="filter-input" id="rate_to" :min="0"/>
                <span class="unit">%</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.term_from" placeholder="от" class="filter-input" id="term_from" :min="0" />
                <span class="unit">мес.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.term_to" placeholder="до" class="filter-input" id="term_to" :min="0" />
                <span class="unit">мес.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rating_from" placeholder="от" class="filter-input" id="rating_from" :min="0" />
                <span class="unit"></span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rating_to" placeholder="до" class="filter-input" id="rating_to" :min="0" />
                <span class="unit"></span>
              </div>
            </div>
          </th>
          <th></th>
        </tr>
        <tr>
          <th @click="sortRequests('fio')">
            ФИО
            <SortArrow :sortDirection="sortDirection.fio" />
          </th>
          <th @click="sortRequests('loan_name')">
            Название кредита
            <SortArrow :sortDirection="sortDirection.loan_name" />
          </th>
          <th @click="sortRequests('request_time')">
            Дата заявки
            <SortArrow :sortDirection="sortDirection.request_time" />
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
          <th @click="sortRequests('rating')">
            Рейтинг
            <SortArrow :sortDirection="sortDirection.rating" />
          </th>
          <th @click="sortRequests('decision')">
            Решение
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.request_id">
          <td>{{ request.fio }}</td>
          <td>{{ request.loan_name }}</td>
          <td>{{ formatDate(request.request_time) }}</td>
          <td>{{ request.amount }}</td>
          <td>{{ request.interest_rate }}</td>
          <td>{{ request.expiration_time }}</td>
          <td>{{ request.rating }}</td>
          <td class="decision-button-container"> 
            <Button text="✓" @click="requestDecision(request.request_id, true)" buttonType="button" class="decision-button" />
            <Button text="✗" @click="requestDecision(request.request_id, false)" buttonType="button" class="decision-button" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import Button from '../../components/Button.vue';
import Notification from '../../components/Notification.vue';
import SortArrow from '../../components/SortArrow.vue';

export default {
  name: 'AdminRequest',
  components: {
    Button,
    SortArrow,
    Notification
  },
  data() {
    return {
      loan_name: [],
      requests: [],
      filters: {
        fio: '',
        loan_name:'',
        date_from: '',
        date_to: '',
        amount_from: '',
        amount_to: '',
        rate_from: '',
        rate_to: '',
        term_from: '',
        term_to: '',
        rating_from: '',
        rating_to: ''
      },
      notificationMessage: '',
      notificationType: 'error',
      isNotificationVisible: false,
      sortDirection: {
        fio: 0,
        loan_name: 0,
        request_time: 0,
        amount: 0,
        interest_rate: 0,
        expiration_time: 0,
        rating: 0,
        decision: 0
      },
      sortField: 'fio'
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
        const response = await axios.get('http://127.0.0.1:5000/admins_request');
        this.requests = response.data;
        console.log(this.requests);
      } catch (error) {
        this.showNotification('Ошибка при получении заявок!', 'error');
        console.error('Ошибка при получении заявок:', error);
      }
    },
    async requestDecision(requestId, decision) {
      const userId = localStorage.getItem('userId');
      try {
        console.log(requestId, decision);
        const response = await axios.get('http://127.0.0.1:5000/credit_request_decision', {
          params: {
            admin_id: userId,
            request_id: requestId,
            decision: decision
          }
        });
        console.log("Данные ответа", response.data);
        this.showNotification('Заявка успешно обработана!', 'success');
        this.applyFilters();
      } catch (error) {
        this.showNotification('Ошибка при обработке заявки!', 'error');
        console.error('Ошибка при получении заявок:', error);
      }
    },

    resetFilters() {
      this.loan_name = [];
      this.filters = {
        fio: '',
        loan_name: [],
        date_from: '',
        date_to: '',
        amount_from: '',
        amount_to: '',
        rate_from: '',
        rate_to: '',
        term_from: '',
        term_to: '',
        rating_from: '',
        rating_to: ''
      };
      this.getRequests();
    },

    validateFilters() {
      if (this.filters.amount_from && this.filters.amount_to && this.filters.amount_from > this.filters.amount_to) {
        this.showNotification('Сумма "от" не может быть больше суммы "до"!', 'error');
        return false;
      }
      if (this.filters.rate_from && this.filters.rate_to && this.filters.rate_from > this.filters.rate_to) {
        this.showNotification('Ставка "от" не может быть больше ставки "до"!', 'error');
        return false;
      }
      if (this.filters.rate_to > 100) {
        this.showNotification('Ставка не может быть больше 100 %!', 'error');
        return false;
      }
      if (this.filters.term_from && this.filters.term_to && this.filters.term_from > this.filters.term_to) {
        this.showNotification('Срок "от" не может быть больше срока "до"!', 'error');
        return false;
      }
      if (this.filters.date_from && this.filters.date_to && this.filters.date_from > this.filters.date_to) {
        this.showNotification('Дата начала не может быть больше даты окончания!', 'error');
        return false;
      }
      return true;
    },

    async applyFilters() {
      if (!this.validateFilters()) {
        return;
      }
      this.filters.loan_name = this.loan_name.join('@');
      const filter = this.filters;
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/filter_admins_request', {
          params: {
            client_id: userId,
            ...filter
          }
        });
        this.requests = response.data;
        if (!this.isNotificationVisible){
          this.showNotification('Фильтры успешно применены!', 'success');
        }
      } catch (error) {
        if (!this.isNotificationVisible){
          this.showNotification('Ошибка при применении фильтров!', 'error');
        }
        console.error('Ошибка при применении фильтров:', error);
      }
    },

    showNotification(message, type, error_message ='') {
      this.notificationMessage = message + " " + error_message;
      this.notificationType = type;
      this.isNotificationVisible = true;
    },

    closeNotification() {
      this.isNotificationVisible = false;
    },

    async fetchRequests() {
      const userId = localStorage.getItem('userId');
      const sortDirection = this.sortDirection;
      const sortField = this.sortField;
      try {
        const response = await axios.get('http://127.0.0.1:5000/sort_admins_request', {
          params: {
            client_id: userId,
            sort_field: sortField,
            sort_direction: sortDirection[sortField]
          }
        });
        this.requests = response.data;
      } catch (error) {
        this.showNotification('Ошибка при применении сортировки!', 'error');
        console.error('Ошибка при применении сортировки:', error);
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
.admin-request {
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
.decision-button-container {
  display: flex;
  align-items: center;
}

.decision-button {
  width: 30px; 
  height: 30px;
  margin-right: 10px;
}

.decision-button:last-child {
  margin-right: 0;
}

</style>
