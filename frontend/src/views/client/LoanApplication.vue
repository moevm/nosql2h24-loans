<template>
  <div class="loan-application">
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="notificationVisible"
      @close="closeNotification"
    />
    <p>Заполните информацию в профиле или проверьте ее актуальность!</p>

    <h2>Оформление кредита: {{ loanType }}</h2>

    <form @submit.prevent="submitApplication">
      <div class="form-group">
        <label for="loanAmount">Желаемая сумма кредита:</label>
        <input
          type="number"
          id="loanAmount"
          v-model="loanAmount"
          placeholder="В рублях"
          
        />
        <div class="amount-range">
          <span>Минимальная сумма: {{ minLoanAmount }}</span>
          <span>Максимальная сумма: {{ maxLoanAmount }}</span>
        </div>
      </div>

      <div class="form-group">
        <label for="expirationTime">Срок:</label>
        <select id="expirationTime" v-model="expirationTime">
          <option v-for="term in expirationTerms" :key="term" :value="term">{{ formatTerm(term) }}</option>
        </select>
        <div class="term-range">
          <span>Минимальный срок: {{ minExpirationTime }} месяцев</span>
          <span>Максимальный срок: {{ maxExpirationTime }} месяцев</span>
        </div>
      </div>

      <div class="form-group">
        <label for="deposit">Залог:</label>
        <input type="text" id="deposit" v-model="deposit" placeholder="В рублях" />
      </div>

      <div class="form-group">
        <label>Созаемщики:</label>
        <div v-for="(coBorrower, index) in coBorrowers" :key="index" class="co-borrower-item">
          <label for="fio">ФИО:</label>
          <input type="text" v-model="coBorrower.fio" id="fio" />
          <label for="contactPhone">Контактный телефон:</label>
          <input type="text" v-model="coBorrower.contactPhone" id="contactPhone" />
          <label for="workplace">Место работы:</label>
          <input type="text" v-model="coBorrower.workplace" id="workplace" />
          <label for="post">Должность:</label>
          <input type="text" v-model="coBorrower.post" id="post" />
          <label for="passportSeries">Серия паспорта:</label>
          <input type="text" v-model="coBorrower.passportSeries" id="passportSeries" maxlength="4" />
          <label for="passportNumber">Номер паспорта:</label>
          <input type="text" v-model="coBorrower.passportNumber" id="passportNumber" maxlength="6" />
          <Button type="button" text="Удалить" @click="removeCoBorrower(index)" />
        </div>
        <Button type="button" text="Добавить созаемщика" @click="addCoBorrower" />
      </div>

      <div class="application-summary">
        <h3>Заявка на потребительский кредит</h3>
        <Button text="Оформить" type="submit" />
      </div>
    </form>
  </div>
</template>
<script>
import Button from '../../components/Button.vue';
import Notification from '../../components/Notification.vue';
import axios from 'axios';

export default {
  name: 'ClientLoanApplication',
  components: {
    Button,
    Notification
  },
  data() {
    return {
      loanAmount: '',
      minLoanAmount: 0,
      maxLoanAmount: 0,
      expirationTime: '',
      minExpirationTime: 0,
      maxExpirationTime: 0,
      expirationTerms: [],
      deposit: '',
      clientId: localStorage.getItem('userId') || null,
      coBorrowers: [{ fio: "", contactPhone: "", workplace: "", post: "", passportSeries: "", passportNumber: "" }],
      notificationMessage: '',
      notificationType: '',
      notificationVisible: false
    };
  },
  computed: {
    loanType() {
      return this.$route.query.loanType || 'Кредит наличными';
    }
  },
  created() {
    this.setLoanParameters();
    this.expirationTerms = this.generateExpirationTerms();
  },
  mounted() {
    document.title = "Оформление заявки на кредит";
  },
  methods: {
    setLoanParameters() {
      switch (this.loanType) {
        case 'Молодежный кредит':
          this.minLoanAmount = 10000;
          this.maxLoanAmount = 6000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 25 * 12;
          break;
        case 'Ипотека':
          this.minLoanAmount = 500000;
          this.maxLoanAmount = 30000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 30 * 12;
          break;
        case 'Кредит наличными':
          this.minLoanAmount = 10000;
          this.maxLoanAmount = 30000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 15 * 12;
          break;
        case 'Автокредит':
          this.minLoanAmount = 100000;
          this.maxLoanAmount = 8000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 5 * 12;
          break;
        case 'Рефинансирование':
          this.minLoanAmount = 10000;
          this.maxLoanAmount = 5000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 5 * 12;
          break;
        case 'Кредитная карта':
          this.minLoanAmount = 10000;
          this.maxLoanAmount = 1000000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 12;
          break;
        default:
          this.minLoanAmount = 10000;
          this.maxLoanAmount = 500000;
          this.minExpirationTime = 6;
          this.maxExpirationTime = 36;
          break;
      }
    },
    generateExpirationTerms() {
      const terms = [];
      for (let i = this.minExpirationTime; i <= this.maxExpirationTime; i += 6) {
        terms.push(i);
      }
      return terms;
    },

    validateLoanAmount() {
      const amount = parseFloat(this.loanAmount);

      if (isNaN(amount)) {
        this.showNotification('Введите корректную сумму кредита.', 'error');
        return false;
      }

      if (amount < this.minLoanAmount || amount > this.maxLoanAmount) {
        this.showNotification(`Сумма кредита должна быть от ${this.minLoanAmount} до ${this.maxLoanAmount}.`, 'error');
        return false;
      }

      return true;
    },

    formatTerm(term) {
      const years = Math.floor(term / 12);
      const months = term % 12;
      let termString = '';

      if (years > 0) {
        termString += `${years} ${this.declension(years, ['год', 'года', 'лет'])}`;
        if (months > 0) {
          termString += ` и ${months} ${this.declension(months, ['месяц', 'месяца', 'месяцев'])}`;
        }
      } else {
        termString += `${months} ${this.declension(months, ['месяц', 'месяца', 'месяцев'])}`;
      }

      return termString;
    },
    declension(num, words) {
      num = Math.abs(num) % 100;
      const n = num % 10;
      if (num > 10 && num < 20) return words[2];
      if (n > 1 && n < 5) return words[1];
      if (n === 1) return words[0];
      return words[2];
    },

    async submitApplication() {
      if (!this.validateLoanAmount()) {
        return;
      }

      const loanData = {
        loanType: this.loanType,
        loanAmount: this.loanAmount,
        expirationTime: this.expirationTime,
        coBorrowers: this.coBorrowers,
        deposit: this.deposit,
        clientId: this.clientId
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/create_credit_request', loanData);
        console.log('Заявка на кредит отправлена:', response.data);
        console.log(loanData);
        this.showNotification('Заявка на кредит успешно отправлена!', 'success');
      } catch (error) {
        console.error('Ошибка при отправке заявки на кредит:', error);
        this.showNotification('Произошла ошибка при отправке заявки на кредит.', 'error', error.response.data.details[0]);
      }
    },

    addCoBorrower() {
      this.coBorrowers.push({ fio: "", contactPhone: "", workplace: "", post: "", passportSeries: "", passportNumber: "" });
    },

    removeCoBorrower(index) {
      this.coBorrowers.splice(index, 1);
    },

    showNotification(message, type, error_message ='') {
      this.notificationMessage = message + " " + error_message;
      this.notificationType = type;
      this.notificationVisible = true;
    },

    closeNotification() {
      this.notificationVisible = false;
    }
  }
};
</script>
<style scoped>
.loan-application {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h2, h3 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type='number'],
input[type='text'],
select {
  width: calc(100% - 22px);
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
}

.amount-range,
.term-range {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.application-summary {
  text-align: center;
  margin-top: 20px;
}

.co-borrower-item {
  margin-bottom: 20px;
}
</style>
