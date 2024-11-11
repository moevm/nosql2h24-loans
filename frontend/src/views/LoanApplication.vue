<template>
  <div class="loan-application">
    <h1>Оформление кредита</h1>
    <p>Заполните информацию в профиле или проверьте ее актуальность!</p>

    <h2>Оформление кредита наличными: {{ loanType }}</h2>

    <label for="loanAmount">Желаемая сумма кредита:</label>
    <input
      type="number"
      id="loanAmount"
      v-model="loanAmount"
      placeholder="Сумма кредита"
    />
    <div class="amount-range">
      <span>Минимальная сумма: {{ minLoanAmount }}</span>
      <span>Максимальная сумма: {{ maxLoanAmount }}</span>
    </div>

    <label for="loanTerm">Срок:</label>
    <select id="loanTerm" v-model="loanTerm">
      <option v-for="term in loanTerms" :key="term" :value="term">{{ formatTerm(term) }}</option>
    </select>
    <div class="term-range">
      <span>Минимальный срок: {{ minLoanTerm }} месяцев</span>
      <span>Максимальный срок: {{ maxLoanTerm }} месяцев</span>
    </div>

    <label for="coBorrowers">Созаемщики:</label>
    <input
      type="text"
      id="coBorrowers"
      v-model="coBorrowers"
      placeholder="Контактный телефон 1, контактный телефон 2, ..."
    />

    <label for="collateral">Залог:</label>
    <input
      type="text"
      id="collateral"
      v-model="collateral"
      placeholder="Сумма залога"
    />

    <div class="application-summary">
      <h3>Заявка на потребительский кредит</h3>
      <Button text="Оформить" @click="submitApplication" />
    </div>
  </div>
</template>

<script>
import Button from '../components/Button.vue';
import axios from 'axios';

export default {
  name: 'LoanApplication',
  components: {
    Button
  },
  data() {
    return {
      loanType: 'Кредит наличными',
      loanAmount: '',
      minLoanAmount: 10000,
      maxLoanAmount: 500000,
      loanTerm: '',
      minLoanTerm: 6,
      maxLoanTerm: 36,
      loanTerms: [],
      coBorrowers: '',
      collateral: ''
    };
  },
  created() {
    this.loanTerms = this.generateLoanTerms();
  },
  methods: {
    generateLoanTerms() {
      const terms = [];
      for (let i = this.minLoanTerm; i <= this.maxLoanTerm; i += 6) {
        terms.push(i);
      }
      return terms;
    },

    validateLoanAmount() {
      const amount = parseFloat(this.loanAmount);

      if (isNaN(amount)) {
        alert('Введите корректную сумму кредита.');
        return false;
      }

      if (amount < this.minLoanAmount || amount > this.maxLoanAmount) {
        alert(`Сумма кредита должна быть от ${this.minLoanAmount} до ${this.maxLoanAmount}.`);
        return false;
      }

      return true;
    },

    formatTerm(term) {
      const years = Math.floor(term / 12);
      const months = term % 12;
      let termString = '';
      if (years > 0) {
        termString += `${years} ${years === 1 ? 'год' : 'года'}`;
        if (months > 0) {
          termString += ` ${months} ${months === 1 ? 'месяц' : 'месяца'}`;
        }
      } else {
        termString += `${months} ${months === 1 ? 'месяц' : 'месяца'}`;
      }
      return termString;
    },

    async submitApplication() {
      if (!this.validateLoanAmount()) {
        return;
      }

      const loanData = {
        loanType: this.loanType,
        loanAmount: this.loanAmount,
        loanTerm: this.loanTerm,
        coBorrowers: this.coBorrowers,
        collateral: this.collateral
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/credit_request', loanData);
        console.log('Заявка на кредит отправлена:', response.data);
        alert('Заявка на кредит успешно отправлена!');
      } catch (error) {
        console.error('Ошибка при отправке заявки на кредит:', error);
        alert('Произошла ошибка при отправке заявки на кредит.');
      }
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
}

label {
  margin-top: 10px;
}

input[type='number'],
input[type='text'],
select {
  margin-top: 5px;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.amount-range,
.term-range {
  display: flex;
  justify-content: space-between;
}

.application-summary {
  margin-top: 20px;
}
</style>
