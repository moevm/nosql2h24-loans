<template>
  <div class="statistics-container">
    <main>
      <h1>Статистика</h1>
      <div class="filters-and-chart">
        <div class="filters">
          <div class="filter">
            <label for="client">Сотрудник/клиент</label>
            <select id="client" v-model="selectedClientType">
              <option value="employee">Сотрудник</option>
              <option value="client">Клиент</option>
            </select>
          </div>
          <div class="filter">
            <label for="name">ФИО</label>
            <input type="text" id="name" v-model="selectedName">
          </div>
          <div class="filter">
            <label for="credit">Название кредита</label>
            <select id="credit" v-model="selectedCreditType">
              <option value="credit1">Кредит 1</option>
              <option value="credit2">Кредит 2</option>
            </select>
          </div>
          <div class="filter">
            <label for="filter">Фильтр</label>
            <select id="filter" v-model="selectedFilter">
              <option value="all">Все</option>
              <option value="openDate">Дата открытия кредита</option>
              <option value="creditSum">Сумма кредита</option>
              <option value="creditTerm">Срок кредита</option>
              <option value="monthlyPayment">Ежемесячный платеж</option>
              <option value="creditStatus">Статус кредита</option>
            </select>
          </div>
          <div class="buttons">
            <Button text="Экспортировать" @click="exportData" />
            <Button text="Импортировать" @click="importData" />
            <Button text="Построить" @click="buildChart" />
          </div>
        </div>
        <div class="chart-container">
          <canvas id="creditChart"></canvas>
        </div>
      </div>
    </main>
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="showNotification"
      @close="closeNotification"
    />
  </div>
</template>

<script>
import Button from '../../components/Button.vue';
import Notification from '../../components/Notification.vue';
import Chart from 'chart.js/auto';

export default {
  name: 'Statistics',
  components: {
    Button,
    Notification
  },
  data() {
    return {
      selectedClientType: 'employee',
      selectedName: '',
      selectedCreditType: 'credit1',
      selectedFilter: 'all',
      notificationMessage: '',
      notificationType: 'info',
      showNotification: false,
      userName: localStorage.getItem('userName') || 'Пользователь'
    };
  },
  methods: {
    exportData() {
      // Логика экспорта данных
      this.showNotification = true;
      this.notificationMessage = 'Данные экспортированы';
      this.notificationType = 'success';
    },
    importData() {
      // Логика импорта данных
      this.showNotification = true;
      this.notificationMessage = 'Данные импортированы';
      this.notificationType = 'success';
    },
    buildChart() {
      const ctx = document.getElementById('creditChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
          datasets: [{
            label: 'Сумма кредита',
            data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 4],
            backgroundColor: [
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)',
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)',
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)',
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)',
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)',
              'rgba(255, 192, 203, 0.5)',
              'rgba(139, 0, 139, 0.5)'
            ],
            borderColor: [
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)',
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)',
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)',
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)',
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)',
              'rgba(255, 192, 203, 1)',
              'rgba(139, 0, 139, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },
    closeNotification() {
      this.showNotification = false;
    }
  }
};
</script>

<style scoped>
.statistics-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

main {
  padding: 20px;
  width: 100%;
}

h1 {
  margin-top: 0;
}

.filters-and-chart {
  display: flex;
  width: 100%;
}

.filters {
  display: flex;
  flex-direction: column;
  width: 30%;
  margin-right: 20px;
}

.filter {
  margin-bottom: 10px;
}

.filter label {
  display: block;
  margin-bottom: 5px;
}

.filter select, .filter input {
  padding: 5px;
  width: 100%;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.buttons button {
  padding: 0.5em 1em;
  font-size: 0.9em;
}

.chart-container {
  width: 70%;
}

.chart {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>
