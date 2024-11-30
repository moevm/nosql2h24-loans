<template>
    <div class="sort-arrow">
      <!-- Стрелка вверх -->
      <div 
        class="triangle-up" 
        :class="{ active: sortDirection === 1, inactive: sortDirection === 0 }" 
      ></div>
      
      <!-- Стрелка вниз -->
      <div 
        class="triangle-down" 
        :class="{ active: sortDirection === -1, inactive: sortDirection === 0 }" 
      ></div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SortArrow',
    props: {
      sortDirection: {
        type: Number,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .sort-arrow {
    display: inline-flex;
    flex-direction: column; /* Стрелки будут располагаться одна над другой */
    align-items: center;
    justify-content: center;
    gap: 5px; /* Расстояние между стрелками */
    position: absolute; /* Расположение стрелок относительно родительского элемента */
    margin-left: 10px; /* Отступ от текста */
    top: 50%; /* Выравнивание по вертикали на середину текста */
    transform: translateY(-50%); /* Центрирование по вертикали */
    z-index: 10; /* Убедитесь, что стрелки будут наверху */
  }
  
  /* Стрелка вверх */
  .triangle-up {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 6px solid #e3afbc; /* Розовая стрелка вверх */
  }
  
  /* Стрелка вниз */
  .triangle-down {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e3afbc; /* Розовая стрелка вниз */
  }
  
  .triangle-up.active {
    border-bottom-color: #5d001e;
  }
  .triangle-down.active {
    border-top-color: #5d001e;
  }
  .triangle-up.inactive {
    border-bottom-color: #e3afbc;
  }
  .triangle-down.inactive {
    border-top-color: #e3afbc;
  }
  </style>
  