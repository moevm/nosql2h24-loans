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
      <Button v-if="!isEditing" @click="startEditing" text="Редактировать" />
      <Button v-if="isEditing" @click="saveProfile" text="Сохранить" />
    </div>
    <form @submit.prevent="saveProfile" class="profile-form">
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
      </div>
      <div class="profile-column">
        <div class="profile-field">
          <label for="email">E-mail:</label>
          <input type="email" v-model="profile.email" :disabled="!isEditing" id="email" />
        </div>
        <div class="profile-field">
          <label for="contactPhone">Контактный телефон:</label>
          <input type="text" v-model="profile.contactPhone" :disabled="!isEditing" id="contactPhone"/>
        </div>
        <div class="profile-field">
          <label for="post">Должность:</label>
          <input type="text" v-model="profile.post" :disabled="true" id="post"/>
        </div>
        <div class="profile-field">
          <label>Паспортные данные:</label>
          <label for="passportSeries">Серия:</label>
          <input type="text" v-model="profile.passportSeries" :disabled="!isEditing" id="passportSeries" maxlength="4"/>
          <label for="passportNumber">Номер:</label>
          <input type="text" v-model="profile.passportNumber" :disabled="!isEditing" id="passportNumber" maxlength="6"/>
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
      notificationMessage: "",
      notificationType: "",
      notificationVisible: false,
      profile: {
        passportSeries: "",
        passportNumber: "",
        post: "",
        firstName: "",
        lastName: "",
        middleName: "",
        email: "",
        gender: "",
        birthdate: "",
        contactPhone: "",
      },
    };
  },
  created() {
    this.getProfile();
  },
  mounted() {
    document.title = "Профиль";
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

        const response = await axios.post(`http://127.0.0.1:5000/admin_profile_change`, {
          admin_id: userId,
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
      const fullName = localStorage.getItem('userName');
      let nameParts = null;
      if (fullName) {
        nameParts = fullName.split(' ');
      }
      if (!nameParts || nameParts.length < 3) {
        const newFullName = `${this.profile.lastName} ${this.profile.firstName} ${this.profile.middleName}`.trim();
        localStorage.setItem('userName', newFullName);
      }
      if (nameParts.length < 3 || this.profile.lastName === '' || this.profile.firstName === '' || this.profile.middleName === '') {
        return;
      }
      if (nameParts[0] !== this.profile.lastName || nameParts[1] !== this.profile.firstName || nameParts[2] !== this.profile.middleName) {
        const newFullName = `${this.profile.lastName} ${this.profile.firstName} ${this.profile.middleName}`.trim();
        localStorage.setItem('userName', newFullName);
      }
    },
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
  appearance: none;
  position: relative;
}
</style>
