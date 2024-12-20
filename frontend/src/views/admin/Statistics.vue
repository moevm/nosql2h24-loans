<template>
  <div class="statistics-container">
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="isNotificationVisible"
      @close="closeNotification"
    />
    <main>
      <h1>Статистика</h1>
      <div class="content-wrapper">
        <div class="filters-section">
          <!-- <div class="filter-item">
            <label for="client-type">Тип пользователя</label>
            <select id="client-type" v-model="selectedClientType">
              <option value="admin">Сотрудник</option>
              <option value="client">Клиент</option>
            </select>
          </div> -->
          <!-- <div class="filter-item">
            <label for="name">ФИО</label>
            <input type="text" id="name" v-model="fullName" placeholder="Иванов Иван Иванович" />
          </div> -->
          <div class="filter-item">
            <label for="credit-type">Тип кредита</label>
            <select id="credit-type" v-model="loanName">
              <option value="Молодежный кредит">Молодежный кредит</option>
              <option value="Ипотека">Ипотека</option>
              <option value="Кредит наличными">Кредит наличными</option>
              <option value="Автокредит">Автокредит</option>
              <option value="Рефинансирование">Рефинансирование</option>
              <option value="Кредитная карта">Кредитная карта</option>
            </select>
          </div>
          <div class="filter-item">
            <label for="filter-type">Фильтр</label>
            <select id="filter-type" v-model="filter">
              <!-- <option value="openDate">Дата открытия кредита</option> -->
              <option value="amount">Сумма кредита</option>
              <option value="expiration_time">Срок кредита</option>
              <!-- <option value="monthlyPayment">Ежемесячный платеж</option>
              <option value="creditStatus">Статус кредита</option> -->
            </select>
          </div>
          <div class="build-buttons">
            <Button text="Построить" @click="buildChart" />
          </div>
          <div class="filter-item">
            <label for="file-upload" class="file-input-label">
              <span>{{ fileName || 'Выберите файл' }}</span>
              <input type="file" id="file-upload" @change="handleFileUpload" accept=".json" class="file-input" />
            </label>
          </div>
          <div class="action-buttons">
            <Button text="Импортировать" @click="importData" />
            <Button text="Экспортировать" @click="exportData" />
          </div>
        </div>
        <div class="chart-container">
          <canvas id="creditChart"></canvas>
        </div>
      </div>
    </main>
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
      selectedClientType: '',
      fullName: '',
      loanName: '',
      filter: '',
      measurements: {
        amount: 'рубли',
        expiration_time: 'месяцы',
      },
      notificationMessage: '',
      notificationType: '',
      isNotificationVisible: false,
      reloadFlag: false,
      userName: localStorage.getItem('userName') || 'Пользователь',
      chart: null,
      file: null,
      fileName: '' 
    };
  },
  mounted() {
    document.title = "Статистика";
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
        this.showNotification('Данные успешно экспортированы', 'success');
      } catch (error) {
        this.showNotification('Ошибка при экспорте данных', 'error', error.message);
        console.error('Ошибка при экспорте данных:', error);
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && file.type === 'application/json') {
        this.file = file;
        this.fileName = file.name;
        this.showNotification('Файл успешно загружен', 'success');
      } else {
        this.showNotification('Пожалуйста, выберите файл формата JSON', 'error');
      }
    },

    async importData() {
      if (!this.file) {
        this.showNotification('Пожалуйста, выберите файл для импорта', 'error');
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
        localStorage.setItem('userName', response.data.adminName);
        this.reloadFlag = true;
        this.showNotification('Данные успешно импортированы.', 'success');
      } catch (error) {
        this.showNotification('Ошибка при импорте данных', 'error', error.message);
        console.error('Ошибка при импорте данных:', error);
      }
    },

    async buildChart() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_hist_data', {
          params: {
            // name: this.fullName,
            credit_type: this.loanName,
            filter_type: this.filter
          }
        });
        const data = response.data;
        this.renderChart(data);
      } catch (error) {
        this.showNotification('Ошибка при получении данных для построения графика', 'error', error.message);
        console.error('Ошибка при получении данных для построения графика:', error);
      }
    },

    renderChart(data) {
      const ctx = document.getElementById('creditChart').getContext('2d');
      if (this.chart) {
        this.chart.destroy();
      }
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: this.measurements[this.filter],
            data: data.values,
            backgroundColor: '#E3AFBC',
            borderColor: '#9A1750',
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
      this.showNotification('Статистика успешно получена!', 'success');
    },

    closeNotification() {
      this.isNotificationVisible = false;
      if (this.reloadFlag == true) {
        window.location.reload();
        this.reloadFlag = false;
      }
    },

    showNotification(message, type, error_message = '') {
      this.notificationMessage = message + " " + error_message;
      this.notificationType = type;
      this.isNotificationVisible = true;
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

.content-wrapper {
  display: flex;
  width: 100%;
}

.filters-section {
  display: flex;
  flex-direction: column;
  width: 30%;
  margin-right: 20px;
}

.filter-item {
  margin-top: 20px;
  margin-bottom: 10px;
}

.filter-item label {
  display: block;
  margin-bottom: 5px;
}

.filter-item select {
  padding: 5px;
  width: 100%;
}

.filter-item input {
  padding: 5px;
  width: 97%;
}

.file-input-label {
  display: inline-block;
  padding: 10px 30px;
  background-color: #E3AFBC;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  width: 90%;
}

.file-input-label span {
  display: inline-block;
  margin-right: 10px;
}

.file-input {
  display: none;
}

.build-buttons {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}
.build-buttons button {
  padding: 0.5em 1em;
  font-size: 0.9em;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.action-buttons button {
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
