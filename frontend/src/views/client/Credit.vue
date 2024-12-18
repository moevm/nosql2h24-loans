<template>
  <div class="client-request">
    <h1>Активные кредиты</h1>
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
            <div class="filter-options">
              <input type="date" v-model="filters.opening_date_from" />
              <span>—</span>
              <input type="date" v-model="filters.opening_date_to" />
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
                <input type="number" v-model="filters.monthly_payment_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.monthly_payment_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <input type="date" v-model="filters.next_payment_date_from" />
              <span>—</span>
              <input type="date" v-model="filters.next_payment_date_to" />
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.debt_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.debt_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">руб.</span>
              </div>
            </div>
          </th>
          <th>
            <div class="filter-options">
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.payments_overdue_from" placeholder="от" class="filter-input" :min="0"/>
                <span class="unit">платежей</span>
              </div>
              <span>—</span>
              <div class="filter-input-wrapper">
                <input type="number" v-model="filters.payments_overdue_to" placeholder="до" class="filter-input" :min="0"/>
                <span class="unit">платежей</span>
              </div>
            </div>
          </th>
          <th></th> 
        </tr>
        <tr>
          <th @click="sortCredits('loan_name')">
            Название кредита
            <SortArrow :sortDirection="sortDirection.loan_name" />
          </th>
          <th @click="sortCredits('opening_date')">
            Дата открытия
            <SortArrow :sortDirection="sortDirection.opening_date" />
          </th>
          <th @click="sortCredits('amount')">
            Сумма
            <SortArrow :sortDirection="sortDirection.amount" />
          </th>
          <th @click="sortCredits('interest_rate')">
            Ставка
            <SortArrow :sortDirection="sortDirection.interest_rate" />
          </th>
          <th @click="sortCredits('expiration_time')">
            Срок
            <SortArrow :sortDirection="sortDirection.expiration_time" />
          </th>
          <th @click="sortCredits('monthly_payment')">
            Ежемесячный платеж
            <SortArrow :sortDirection="sortDirection.monthly_payment" />
          </th>
          <th @click="sortCredits('next_payment_date')">
            Дата следующего платежа
            <SortArrow :sortDirection="sortDirection.next_payment_date" />
          </th>
          <th @click="sortCredits('debt')">
            Задолженность
            <SortArrow :sortDirection="sortDirection.debt" />
          </th>
          <th @click="sortCredits('payments_overdue')">
            Просрочено
            <SortArrow :sortDirection="sortDirection.payments_overdue" />
          </th>
          <th>
            Ссылка
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request._id">
          <td>{{ request.loan_name }}</td>
          <td>{{ formatDate(request.opening_date) }}</td>
          <td>{{ request.amount }}</td>
          <td>{{ request.interest_rate }}</td>
          <td>{{ request.expiration_time }}</td>
          <td>{{ request.monthly_payment }}</td>
          <td>{{ formatDate(request.next_payment_date) }}</td>
          <td>{{ request.debt }}</td>
          <td>{{ request.payments_overdue }}</td>
          <td>
            <button @click="goToCreditDetail(request._id)">🔗</button>
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
  name: 'ClientCredit',
  components: {
    Button,
    SortArrow,
    Notification
  },
  data() {
    return {
      requests: [],
      loan_name: [],
      filters: {
        opening_date_from: '',
        opening_date_to: '',
        amount_from: '',
        amount_to: '',
        interest_rate_from: '',
        interest_rate_to: '',
        expiration_time_from: '',
        expiration_time_to: '',
        monthly_payment_from: '',
        monthly_payment_to: '',
        next_payment_date_from: '',
        next_payment_date_to: '',
        debt_from: '',
        debt_to: '',
        payments_overdue_from: '',
        payments_overdue_to: ''
      },
      notificationMessage: '',
      notificationType: 'error',
      isNotificationVisible: false,
      sortDirection: {
        loan_name: 0,
        opening_date: 0,
        amount: 0,
        interest_rate: 0,
        expiration_time: 0,
        monthly_payment: 0,
        next_payment_date: 0,
        debt: 0,
        payments_overdue: 0
      },
      sortField: 'loan_name'
    };
  },
  created() {
    this.getCredits();
  },
  mounted() {
    document.title = "Кредиты";
  },
  methods: {
    async getCredits() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_active_credits', {
          params: {
            client_id: userId
          }
        });
        this.requests = response.data;
      } catch (error) {
        console.error('Ошибка при получении заявок:', error);
      }
    },

    resetFilters() {
      this.loan_name = [];
      this.filters = {
        opening_date_from: '',
        opening_date_to: '',
        amount_from: '',
        amount_to: '',
        interest_rate_from: '',
        interest_rate_to: '',
        expiration_time_from: '',
        expiration_time_to: '',
        monthly_payment_from: '',
        monthly_payment_to: '',
        next_payment_date_from: '',
        next_payment_date_to: '',
        debt_from: '',
        debt_to: '',
        payments_overdue_from: '',
        payments_overdue_to: ''
      };
      this.getCredits();
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

      if (this.filters.opening_date_from && this.filters.opening_date_to && this.filters.opening_date_from > this.filters.opening_date_to) {
        this.showNotification('Дата начала не может быть больше даты окончания!', 'error');
        return false;
      }

      if (this.filters.monthly_payment_from && this.filters.monthly_payment_to && this.filters.monthly_payment_from > this.filters.monthly_payment_to) {
        this.showNotification('Ежемесячный платеж "от" не может быть больше платежа "до"!', 'error');
        return false;
      }

      if (this.filters.debt_from && this.filters.debt_to && this.filters.debt_from > this.filters.debt_to) {
        this.showNotification('Задолженность "от" не может быть больше задолженности "до"!', 'error');
        return false;
      }

      if (this.filters.payments_overdue_from && this.filters.payments_overdue_to && this.filters.payments_overdue_from > this.filters.payments_overdue_to) {
        this.showNotification('Количество просроченных платежей "от" не может быть больше "до"!', 'error');
        return false;
      }

      const numericFilters = [
        'amount_from', 'amount_to', 'interest_rate_from', 'interest_rate_to',
        'expiration_time_from', 'expiration_time_to', 'monthly_payment_from',
        'monthly_payment_to', 'debt_from', 'debt_to', 'payments_overdue_from', 'payments_overdue_to'
      ];

      for (const filter of numericFilters) {
        if (this.filters[filter] && isNaN(this.filters[filter])) {
          this.showNotification(`${filter.replace('_', ' ')} должно быть числом!`, 'error');
          return false;
        }
      }

      return true;
    },

    async applyFilters() {
      if (!this.validateFilters()) return;
      const filter = {
        loan_name: this.loan_name.join('@'),
        ...this.filters
      };
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/filter_active_credits', {
          params: {
            client_id: userId,
            ...filter
          }
        });
        this.requests = response.data;
        this.showNotification('Фильтры успешно применены!', 'success');
      } catch (error) {
        this.showNotification('Ошибка при применении фильтров!', 'error');
        console.error('Ошибка при применении фильтров:', error);
      }
    },

    closeNotification() {
      this.isNotificationVisible = false;
    },

    async fetchCredits() {
      const userId = localStorage.getItem('userId');
      try {
        const response = await axios.get('http://127.0.0.1:5000/sort_active_credits', {
          params: {
            client_id: userId,
            sort_field: this.sortField,
            sort_direction: this.sortDirection[this.sortField]
          }
        });
        this.requests = response.data;
      } catch (error) {
        this.showNotification('Ошибка при применении сортировки!', 'error');
        console.error('Ошибка при применении сортировки:', error);
      }
    },

    sortCredits(field) {
      this.sortDirection[field] = this.sortDirection[field] === 1 ? -1 : 1;
      this.sortField = field;
      this.fetchCredits();
    },

    showNotification(message, type) {
      this.notificationMessage = message;
      this.notificationType = type;
      this.isNotificationVisible = true;
    },

    formatDate(date) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      };
      return new Date(date).toLocaleDateString('ru-RU', options);
    },
    
    goToCreditDetail(creditId) {
      localStorage.setItem('creditId', creditId);
      this.$router.push('/credit');
    }
  }
};

</script>

<style scoped>
.client-request {
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