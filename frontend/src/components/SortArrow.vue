<template>
    <div class="sort-arrow">
      <div 
        class="triangle-up" 
        :class="{ active: sortDirection === 1, inactive: sortDirection === 0 }" 
      ></div>
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
    margin-left: 10px; 
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
  }
  
  .triangle-up {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 6px solid #e3afbc; 
  }
  
  .triangle-down {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e3afbc;
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
  