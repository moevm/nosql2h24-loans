<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>Профиль</h1>
      <div class="profile-photo">
        <img v-if="profile.photo" :src="profile.photo" alt="Profile Photo" class="photo" />
        <input type="file" @change="uploadPhoto" v-if="isEditing" />
      </div>
      <Button v-if="!isEditing" @click="startEditing" text="Редактировать" />
      <Button v-if="isEditing" @click="saveProfile" text="Сохранить" />
    </div>
    <form @submit.prevent="saveProfile" class="profile-form">
      <!-- Первый столбец -->
      <div class="profile-column">
        <div class="profile-field">
          <label for="fio">ФИО:</label>
          <input type="text" v-model="profile.fio" :disabled="!isEditing" id="fio" />
        </div>
        <div class="profile-field">
          <label for="email">E-mail:</label>
          <input type="email" v-model="profile.email" :disabled="!isEditing" id="email" />
        </div>
        <div class="profile-field">
          <label for="workplace">Место работы:</label>
          <input type="text" v-model="profile.workplace" :disabled="!isEditing" id="workplace" />
        </div>
        <div class="profile-field">
          <label for="gender">Пол:</label>
          <select v-model="profile.gender" :disabled="!isEditing" id="gender" class="full-width">
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
          </select>
        </div>
        <div class="profile-field">
          <label for="birthdate">Дата рождения:</label>
          <input
            type="date"
            v-model="profile.birthdate"
            :disabled="!isEditing"
            id="birthdate"
            @focus="$event.target.showPicker()"
            class="full-width date-input"
          />
        </div>
        <div class="profile-field">
          <label for="contactPhone">Контактный телефон:</label>
          <input type="text" v-model="profile.contactPhone" :disabled="!isEditing" id="contactPhone" @blur="validatePhone" />
          <span v-if="phoneError" class="error">Некорректный номер телефона</span>
        </div>
      </div>

      <!-- Второй столбец -->
      <div class="profile-column">
        <div class="profile-field">
          <label for="familyStatus">Семейное положение:</label>
          <select v-model="profile.familyStatus" :disabled="!isEditing" id="familyStatus" class="full-width">
            <option value="single">Не женат/не замужем</option>
            <option value="married">Женат/Замужем</option>
            <option value="divorced">Разведен</option>
            <option value="widowed">Вдовец/Вдова</option>
          </select>
        </div>
        <div class="profile-field">
          <label for="childrenCount">Количество детей:</label>
          <input type="number" v-model="profile.childrenCount" :disabled="!isEditing" id="childrenCount" />
        </div>
        <div class="profile-field">
          <label for="income">Доход:</label>
          <input type="number" v-model="profile.income" :disabled="!isEditing" id="income" />
        </div>
        <div class="profile-field">
          <label for="incomeSpouse">Доход супруга:</label>
          <input type="number" v-model="profile.incomeSpouse" :disabled="!isEditing" id="incomeSpouse" />
        </div>
        <div class="profile-field">
          <label for="workplaceSpouse">Место работы супруга:</label>
          <input type="text" v-model="profile.workplaceSpouse" :disabled="!isEditing" id="workplaceSpouse" />
        </div>
      </div>

      <!-- Третий столбец -->
      <div class="profile-column">
        <div class="profile-field">
          <label>Имущество:</label>
          <div v-for="(property, index) in profile.properties" :key="index" class="property-item">
            <input
              type="text"
              v-model="property.type"
              :disabled="!isEditing"
              placeholder="Тип актива"
            />
            <input
              type="number"
              v-model="property.value"
              :disabled="!isEditing"
              placeholder="Стоимость"
            />
            <input
              type="text"
              v-model="property.legal"
              :disabled="!isEditing"
              placeholder="Правовые аспекты"
            />
            <Button v-if="isEditing" text="Удалить" @click="removeProperty(index)" />
          </div>
          <Button v-if="isEditing" text="Добавить имущество" @click="addProperty" />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Button from "../../components/Button.vue";

export default {
  name: "Profile",
  components: {
    Button,
  },
  data() {
    return {
      isEditing: false,
      phoneError: false,
      profile: {
        fio: "",
        email: "",
        workplace: "",
        gender: "",
        birthdate: "",
        contactPhone: "",
        familyStatus: "",
        childrenCount: "",
        income: "",
        incomeSpouse: "",
        workplaceSpouse: "",
        properties: [{ type: "", value: 0, legal: "" }],
        photo: "",
      },
    };
  },
  created() {
    this.getProfile();
  },
  methods: {
    async getProfile() {
      const userId = localStorage.getItem("userId");
      const userType = localStorage.getItem("userType");
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_profile', {
          params: {
            userId: userId,
            userType: userType
          }
        });
        this.profile = response.data;
      } catch (error) {
        console.error("Ошибка при получении профиля:", error);
      }
    },
    startEditing() {
      this.isEditing = true;
    },
    async saveProfile() {
      if (this.phoneError) {
        alert("Исправьте номер телефона перед сохранением.");
        return;
      }
      const userId = localStorage.getItem("userId");
      try {
        await axios.post(`http://127.0.0.1:5000/client_profile_change`, {
          client_id: userId,
          ...this.profile,
        });
        this.isEditing = false;
        alert("Профиль успешно сохранен!");
        this.getProfile()
      } catch (error) {
        console.error("Ошибка при сохранении профиля:", error);
        alert("Произошла ошибка при сохранении профиля.");
      }
    },
    validatePhone() {
      const phoneRegex = /^\+?[1-9]\d{1,14}$/;
      this.phoneError = !phoneRegex.test(this.profile.contactPhone);
    },
    addProperty() {
      this.profile.properties.push({ type: "", value: 0, legal: "" });
    },
    removeProperty(index) {
      this.profile.properties.splice(index, 1);
    },
    uploadPhoto(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profile.photo = e.target.result;
      };
      reader.readAsDataURL(file);
    },
  },
};
</script>
<style scoped>
.profile-container {
  width: 80%;
  max-width: 1400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.profile-photo {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-photo img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-form {
  display: flex;
  justify-content: space-between;
  gap: 50px; 
}

.profile-column {
  flex: 1;
}

.profile-field {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input:disabled,
select:disabled {
  background-color: #f0f0f0;
}

.date-input {
  -webkit-appearance: none;
  -moz-appearance: textfield;
  appearance: none;
  position: relative;
  padding-right: 20px; /* Добавляем отступ для иконки календаря */
}

.date-input::-webkit-calendar-picker-indicator {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  opacity: 0.6;
  cursor: pointer;
}

.property-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 10px;
}

.property-item input {
  flex: 1;
}

.error {
  color: red;
  font-size: 0.9em;
}
</style>
