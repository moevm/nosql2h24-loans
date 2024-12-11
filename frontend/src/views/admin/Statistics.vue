<template>
  <div class="statistics-container">
    <main>
      <h1>Статистика</h1>
      <div class="filters-and-chart">
        <div class="filters">
          <!-- <div class="filter">
            <label for="client">Сотрудник/клиент</label>
            <select id="client" v-model="selectedClientType">
              <option value="employee">Сотрудник</option>
              <option value="client">Клиент</option>
            </select>
          </div>
          <div class="filter">
            <label for="name">ФИО</label>
            <input type="text" id="name" v-model="selectedName" placeholder="Введите ФИО" />
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
          </div> -->
          <div class="filter">
            <input type="file" id="fileInput" @change="handleFileUpload" accept=".json" />
          </div>
          <div class="buttons">
            <Button text="Экспортировать" @click="exportData" />
            <Button text="Импортировать" @click="importData" />
            <!-- <Button text="Построить" @click="buildChart" /> -->
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
import axios from 'axios';
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
      userName: localStorage.getItem('userName') || 'Пользователь',
      chartData: {
        labels: [],
        datasets: []
      },
      file: null
    };
  },
  methods: {
    async exportData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/database_export', {
          responseType: 'blob'
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'exported_data.json');
        document.body.appendChild(link);
        link.click();

        this.showNotification = true;
        this.notificationMessage = 'Данные успешно экспортированы';
        this.notificationType = 'success';
      } catch (error) {
        this.showNotification = true;
        this.notificationMessage = 'Ошибка при экспорте данных';
        this.notificationType = 'error';
        console.error('Ошибка при экспорте данных:', error);
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && file.type === 'application/json') {
        this.file = file;
        this.showNotification = true;
        this.notificationMessage = 'Файл успешно загружен';
        this.notificationType = 'success';
      } else {
        this.showNotification = true;
        this.notificationMessage = 'Пожалуйста, выберите файл формата JSON';
        this.notificationType = 'error';
      }
    },
    async importData() {
      if (!this.file) {
        this.showNotification = true;
        this.notificationMessage = 'Пожалуйста, выберите файл для импорта';
        this.notificationType = 'error';
        return;
      }
      const formData = new FormData();
      const userId = localStorage.getItem("userId");
      formData.append('file', this.file);
      formData.append('user_id', userId);
      try {
        const response = await axios.post('http://127.0.0.1:5000/database_import', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        localStorage.setItem('userType', response.data.userType);
        localStorage.setItem('userName', response.data.userName);
        this.showNotification = true;
        this.notificationMessage = 'Данные успешно импортированы';
        this.notificationType = 'success';

      } catch (error) {
        this.showNotification = true;
        this.notificationMessage = 'Ошибка при импорте данных';
        this.notificationType = 'error';
        console.error('Ошибка при импорте данных:', error);
      }
    },

    async buildChart() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/statistics', {
          params: {
            clientType: this.selectedClientType,
            name: this.selectedName,
            creditType: this.selectedCreditType,
            filter: this.selectedFilter
          }
        });

        const data = response.data;

        this.chartData = {
          labels: data.labels,
          datasets: [{
            label: 'Сумма кредита',
            data: data.values,
            backgroundColor: 'rgba(139, 0, 139, 0.5)',
            borderColor: 'rgba(139, 0, 139, 1)',
            borderWidth: 1
          }]
        };

        this.renderChart();
      } catch (error) {
        this.showNotification = true;
        this.notificationMessage = 'Ошибка при получении данных для построения графика';
        this.notificationType = 'error';
        console.error('Ошибка при получении данных для построения графика:', error);
      }
    },

    renderChart() {
      const ctx = document.getElementById('creditChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: this.chartData,
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