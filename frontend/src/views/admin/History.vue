<template>
  <div class="admin-history">
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="isNotificationVisible"
      @close="closeNotification"
    />
    <h1>История взаимодействия</h1>
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
            <div class="filter-options">
              <input type="date" v-model="filters.request_time_from" />
              <span>—</span>
              <input type="date" v-model="filters.request_time_to" />
            </div>
          </th>
          <th>
            <div class="filter-options">
              <input type="date" v-model="filters.processing_date_from" />
              <span>—</span>
              <input type="date" v-model="filters.processing_date_to" />
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
                <input type="number" v-model="filters.interest_rate_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">%</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.interest_rate_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">%</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.expiration_time_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">мес.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.expiration_time_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">мес.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rating_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit"></span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.rating_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit"></span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div>
                <input type="checkbox" v-model="decision" value="true" />
                <label>Одобрено</label>
              </div>
              <div>
                <input type="checkbox" v-model="decision" value="false" />
                <label>Отказано</label>
              </div>
            </div>
          </th>
        </tr>
        <tr>
          <th @click="sortHistory('fio')">
            ФИО клиента
            <SortArrow :sortDirection="sortDirection.fio" />
          </th>
          <th @click="sortHistory('loan_name')">
            Название кредита
            <SortArrow :sortDirection="sortDirection.loan_name" />
          </th>
          <th @click="sortHistory('request_time')">
            Дата заявки
            <SortArrow :sortDirection="sortDirection.request_time" />
          </th>
          <th @click="sortHistory('processing_date')">
            Дата обработки
            <SortArrow :sortDirection="sortDirection.processing_date" />
          </th>
          <th @click="sortHistory('amount')">
            Сумма
            <SortArrow :sortDirection="sortDirection.amount" />
          </th>
          <th @click="sortHistory('interest_rate')">
            Ставка
            <SortArrow :sortDirection="sortDirection.interest_rate" />
          </th>
          <th @click="sortHistory('expiration_time')">
            Срок
            <SortArrow :sortDirection="sortDirection.expiration_time" />
          </th>
          <th @click="sortHistory('rating')">
            Рейтинг
            <SortArrow :sortDirection="sortDirection.rating" />
          </th>
          <th @click="sortHistory('decision')">
            Решение
            <SortArrow :sortDirection="sortDirection.decision" />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="history in histories" :key="history._id">
          <td><router-link :to="{ path: '/client_credit_history', query: { client_id: history.client_id } }">{{ history.fio }}</router-link></td>
          <td>{{ history.loan_name }}</td>
          <td>{{ formatDateTime(history.request_time) }}</td>
          <td>{{ formatDateTime(history.processing_date) }}</td>
          <td>{{ history.amount }}</td>
          <td>{{ history.interest_rate }}</td>
          <td>{{ history.expiration_time }}</td>
          <td>{{ history.rating }}</td>
          <td>{{ formatDecision(history.decision) }}</td>
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
  name: 'History',
  components: {
    Button,
    SortArrow,
    Notification
  },
  data() {
    return {
      loan_name: [],
      histories: [],
      decision: [],
      filters: {
        fio: '',
        request_time_from: '',
        request_time_to: '',
        processing_date_from: '',
        processing_date_to: '',
        amount_from: '',
        amount_to: '',
        interest_rate_from: '',
        interest_rate_to: '',
        expiration_time_from: '',
        expiration_time_to: '',
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
        processing_date: 0,
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
    this.getHistory();
  },
  mounted() {
    document.title = "История взаимодействия";
  },
  methods: {
    async getHistory() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_interactions', {
          params: {
            admin_id: userId
          }
        });
        this.histories = response.data;
      } catch (error) {
        this.showNotification('Ошибка при получении истории заявок!', 'error');
        console.error('Ошибка при получении истории заявок:', error);
      }
    },

    resetFilters(flag=true) {
      this.loan_name = [];
      this.decision = [];
      this.filters = {
        fio: '',
        request_time_from: '',
        request_time_to: '',
        processing_date_from: '',
        processing_date_to: '',
        amount_from: '',
        amount_to: '',
        interest_rate_from: '',
        interest_rate_to: '',
        expiration_time_from: '',
        expiration_time_to: '',
        rating_from: '',
        rating_to: ''
      };
      if (flag) {
        this.getHistory();
      }
    },

    validateFilters() {
      if (this.filters.amount_from && this.filters.amount_to && this.filters.amount_from > this.filters.amount_to) {
        this.showNotification('Сумма "от" не может быть больше суммы "до"!', 'error');
        return false;
      }

      if (this.filters.interest_rate_from && this.filters.interest_rate_to && this.filters.interest_rate_from > this.filters.interest_rate_to) {
        this.showNotification('Ставка "от" не может быть больше ставки "до"!', 'error');
        return false;
      }

      if (this.filters.interest_rate_to > 100) {
        this.showNotification('Ставка не может быть больше 100 %!', 'error');
        return false;
      }

      if (this.filters.expiration_time_from && this.filters.expiration_time_to && this.filters.expiration_time_from > this.filters.expiration_time_to) {
        this.showNotification('Срок "от" не может быть больше срока "до"!', 'error');
        return false;
      }

      if (this.filters.request_time_from && this.filters.request_time_to && new Date(this.filters.request_time_from) > new Date(this.filters.request_time_to)) {
        this.showNotification('Дата запроса "от" не может быть больше даты запроса "до"!', 'error');
        return false;
      }

      if (this.filters.processing_date_from && this.filters.processing_date_to && new Date(this.filters.processing_date_from) > new Date(this.filters.processing_date_to)) {
        this.showNotification('Дата обработки "от" не может быть больше даты обработки "до"!', 'error');
        return false;
      }

      if (this.filters.rating_from && this.filters.rating_to && this.filters.rating_from > this.filters.rating_to) {
        this.showNotification('Рейтинг "от" не может быть больше рейтинга "до"!', 'error');
        return false;
      }

      return true;
    },

    async applyFilters() {
      if (!this.validateFilters()) {
        return;
      }
      this.filters.loan_name = this.loan_name.join('@');
      this.filters.decision = this.decision.join('@');
      const filter = this.filters;
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/filter_interaction_history', {
          params: {
            admin_id: userId,
            ...filter
          }
        });
        this.histories = response.data;
        if (!this.isNotificationVisible) {
          this.showNotification('Фильтры успешно применены!', 'success');
        }
      } catch (error) {
        if (!this.isNotificationVisible) {
          this.showNotification('Ошибка при применении фильтров!', 'error');
        }
        console.error('Ошибка при применении фильтров:', error);
      }
    },

    showNotification(message, type, error_message = '') {
      this.notificationMessage = message + " " + error_message;
      this.notificationType = type;
      this.isNotificationVisible = true;
    },

    closeNotification() {
      this.isNotificationVisible = false;
    },

    async fetchHistory() {
      const userId = localStorage.getItem('userId');
      const sortDirection = this.sortDirection;
      const sortField = this.sortField;
      try {
        const response = await axios.get('http://127.0.0.1:5000/sort_interaction_history', {
          params: {
            admin_id: userId,
            sort_field: sortField,
            sort_direction: sortDirection[sortField]
          }
        });
        this.histories = response.data;
        this.resetFilters(false);
      } catch (error) {
        this.showNotification('Ошибка при применении сортировки!', 'error');
        console.error('Ошибка при применении сортировки:', error);
      }
    },

    sortHistory(field) {
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
      this.fetchHistory();
    },

    formatDecision(decision) {
      if (decision) {
        return 'Одобрено';
      }
      return 'Отказано';  
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
    }
  }
};
</script>

<style scoped>
.admin-history {
  width: 100%;
  max-width: 2000px;
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

.table-container {
  overflow-x: auto;
  width: 100%;
}

table.extended-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  table-layout: auto;
}

th, td {
  border: 1px solid #ddd;
  padding: 15px;
  text-align: left;
  word-wrap: break-word;
  white-space: nowrap;
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
