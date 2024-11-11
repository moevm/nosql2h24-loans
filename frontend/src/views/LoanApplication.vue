<template>
  <div class="loan-application">
    <h1>Оформление кредита</h1>
    <p>Заполните информацию в профиле или проверьте ее актуальность!</p>
    
    <h2>Оформление кредита наличными: {{ loanType }}</h2> <!-- Название кредита, переданное из других компонентов -->

    <label for="loanAmount">Желаемая сумма кредита:</label>
    <input 
      type="number" 
      id="loanAmount" 
      v-model="loanAmount" 
      placeholder="Сумма кредита" 
      @input="validateLoanAmount"
    />
    <div class="amount-range">
      <span>Минимальная сумма: {{ minLoanAmount }}</span>
      <span>Максимальная сумма: {{ maxLoanAmount }}</span>
    </div>

    <label for="loanTerm">Срок:</label>
    <select id="loanTerm" v-model="loanTerm">
      <option v-for="term in loanTerms" :key="term" :value="term">{{ term }} месяцев</option>
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
import Button from '../components/Button.vue'; // Импортируем компонент кнопки

export default {
  name: 'LoanApplication',
  components: {
    Button
  },
  data() {
    return {
      loanType: 'Кредит наличными', // Это значение может быть передано из другого компонента
      loanAmount: '',
      minLoanAmount: 10000, // Минимальная сумма кредита
      maxLoanAmount: 500000, // Максимальная сумма кредита
      loanTerm: '',
      loanTerms: [6, 12, 24, 36], // Доступные сроки в месяцах
      minLoanTerm: 6, // Минимальный срок
      maxLoanTerm: 36, // Максимальный срок
      coBorrowers: '',
      collateral: ''
    };
  },
  methods: {
    validateLoanAmount() {
      // Здесь можно добавить валидацию суммы кредита
    },
    submitApplication() {
      // Логика отправки заявки на кредит
      console.log('Заявка на кредит:', {
        loanType: this.loanType,
        loanAmount: this.loanAmount,
        loanTerm: this.loanTerm,
        coBorrowers: this.coBorrowers,
        collateral: this.collateral
      });

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