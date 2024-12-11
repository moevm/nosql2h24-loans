<template>
  <div class="profile-container">
    <Notification
      :message="notificationMessage"
      :type="notificationType"
      :visible="notificationVisible"
      @close="closeNotification"
    />
    <div class="profile-header">
      <h1>Профиль</h1>
      <!-- <div class="profile-photo">
        <img v-if="profile.photo" :src="profile.photo" alt="Profile Photo" class="photo" />
        <input type="file" @change="uploadPhoto" v-if="isEditing" />
      </div> -->
      <Button v-if="!isEditing" @click="startEditing" text="Редактировать" />
      <Button v-if="isEditing" @click="saveProfile" text="Сохранить" />
    </div>
    <form @submit.prevent="saveProfile" class="profile-form">
      <!-- Первый столбец -->
      <div class="profile-column">
        <div class="profile-field">
          <label for="lastName">Фамилия:</label>
          <input type="text" v-model="profile.lastName" :disabled="!isEditing" id="lastName" />
        </div>
        <div class="profile-field">
          <label for="firstName">Имя:</label>
          <input type="text" v-model="profile.firstName" :disabled="!isEditing" id="firstName" />
        </div>
        <div class="profile-field">
          <label for="middleName">Отчество:</label>
          <input type="text" v-model="profile.middleName" :disabled="!isEditing" id="middleName" />
        </div>
        <div class="profile-field">
          <label for="email">E-mail:</label>
          <input type="email" v-model="profile.email" :disabled="!isEditing" id="email" />
        </div>
        <div class="profile-field">
          <label for="contactPhone">Контактный телефон:</label>
          <input type="text" v-model="profile.contactPhone" :disabled="!isEditing" id="contactPhone"/>
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
          <label>Паспортные данные:</label>
          <label for="passportSeries">Серия:</label>
          <input type="text" v-model="profile.passportSeries" :disabled="!isEditing" id="passportSeries" maxlength="4"/>
          <label for="passportNumber">Номер:</label>
          <input type="text" v-model="profile.passportNumber" :disabled="!isEditing" id="passportNumber" maxlength="6"/>
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
          <input type="number" v-model="profile.income" :disabled="!isEditing" id="income" placeholder="В рублях"/>
        </div>
        <div class="profile-field">
          <label for="workplace">Место работы:</label>
          <input type="text" v-model="profile.workplace" :disabled="!isEditing" id="workplace" />
        </div>
        <div class="profile-field">
          <label for="post">Должность:</label>
          <input type="text" v-model="profile.post" :disabled="!isEditing" id="post"/>
        </div>
        <div class="profile-field">
          <label for="incomeSpouse">Доход супруга:</label>
          <input type="number" v-model="profile.incomeSpouse" :disabled="isSpouseFieldsDisabled" id="incomeSpouse" placeholder="В рублях"/>
        </div>
        <div class="profile-field">
          <label for="workplaceSpouse">Место работы супруга:</label>
          <input type="text" v-model="profile.workplaceSpouse" :disabled="isSpouseFieldsDisabled" id="workplaceSpouse" />
        </div>
       
        <div class="profile-field">
          <label for="postSpouse">Должность супруга:</label>
          <input type="text" v-model="profile.postSpouse" :disabled="isSpouseFieldsDisabled" id="postSpouse" />
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
            <Button v-if="isEditing" type="button" text="Удалить" @click="removeProperty(index)" />
          </div>
          <Button v-if="isEditing" type="button" text="Добавить имущество" @click="addProperty" />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Button from "../../components/Button.vue";
import Notification from "../../components/Notification.vue";

export default {
  name: "Profile",
  components: {
    Button,
    Notification
  },
  data() {
    return {
      isEditing: false,
      hasSpouse: false,
      notificationMessage: "",
      notificationType: "",
      notificationVisible: false,
      profile: {
        passportSeries: "",
        passportNumber: "",
        post: "",
        postSpouse: "",
        firstName: "",
        lastName: "",
        middleName: "",
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
        // photo: "",
      },
    };
  },
  computed: {
    isSpouseFieldsDisabled() {
      return this.profile.familyStatus !== "married";
    }
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
        this.saveName();
      } catch (error) {
        console.error("Ошибка при получении профиля:", error);
      }
    },
    startEditing() {
      this.isEditing = true;
    },
    async saveProfile() {
      const userId = localStorage.getItem("userId");
      try {

        const response = await axios.post(`http://127.0.0.1:5000/client_profile_change`, {
          client_id: userId,
          ...this.profile,
        });
        this.isEditing = false;
        this.showNotification("Профиль успешно сохранен!", "success");
        this.getProfile();
      } catch (error) {
        console.error("Ошибка при сохранении профиля:", error);
        this.showNotification("Произошла ошибка при сохранении профиля.", "error", error.response.data.details[0]);
      }
    },
    saveName() {
      const fio = localStorage.getItem('userName');
      let fioParts = null;
      if (fio) {
        fioParts = fio.split(' ');
      }
      if (!fioParts) {
        const fullName = `${this.profile.lastName} ${this.profile.firstName} ${this.profile.middleName}`.trim();
        localStorage.setItem('userName', fullName);
      }
      if ( fioParts.length < 3 || this.profile.lastName == '' || this.profile.firstName == '' || this.profile.middleName == ''){
        return;
      }
      if (fioParts[0] !== this.profile.lastName || fioParts[1] !== this.profile.firstName || fioParts[2] !== this.profile.middleName) {
        const fullName = `${this.profile.lastName} ${this.profile.firstName} ${this.profile.middleName}`.trim();
        localStorage.setItem('userName', fullName);
      }
    },
    addProperty() {
      this.profile.properties.push({ type: "", value: 0, legal: "" });
    },
    removeProperty(index) {
      this.profile.properties.splice(index, 1);
    },
    // uploadPhoto(event) {
    //   const file = event.target.files[0];
    //   const reader = new FileReader();
    //   reader.onload = (e) => {
    //     this.profile.photo = e.target.result;
    //   };
    //   reader.readAsDataURL(file);
    // },
    showNotification(message, type, error_message ='') {
      this.notificationMessage = message + " " + error_message;
      this.notificationType = type;
      this.notificationVisible = true;
    },
    closeNotification() {
      this.notificationVisible = false;
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

/* .profile-photo {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-photo img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
} */

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
  padding-right: 20px;
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
