
<template>
    <div class="shift-calendar">
      <div class="calendar-header">
        <h3>Shift Schedule: {{ currentMonth }} {{ currentYear }}</h3>
        <div class="controls">
          <button @click="previousMonth">←</button>
          <button @click="nextMonth">→</button>
          <button @click="$emit('add-shift')">Add Shift</button>
        </div>
      </div>
      
      <div class="calendar-grid">
        <div class="day-header" v-for="day in days" :key="day">{{ day }}</div>
        <template v-for="(week, weekIndex) in weeks" :key="weekIndex">
          <div 
            v-for="day in week" 
            :key="day.date"
            class="day-cell"
            :class="{
              'current-month': day.isCurrentMonth,
              'today': day.isToday
            }"
          >
            <div class="day-number">{{ day.date.getDate() }}</div>
            <div class="shifts">
              <div 
                v-for="shift in getShiftsForDay(day.date)" 
                :key="shift.shift_id"
                class="shift"
                @click="$emit('edit-shift', shift)"
              >
                <span class="employee">{{ getEmployeeName(shift.employee_id) }}</span>
                <span class="time">{{ formatTime(shift.start_time) }} - {{ formatTime(shift.end_time) }}</span>
                <span v-if="!shift.is_approved" class="pending">Pending</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue'
  
  export default {
    props: {
      shifts: {
        type: Array,
        default: () => []
      },
      employees: {
        type: Array,
        default: () => []
      }
    },
    
    setup() {
      const today = new Date()
      const currentDate = ref(new Date())
      
      const currentMonth = computed(() => {
        return currentDate.value.toLocaleString('default', { month: 'long' })
      })
      
      const currentYear = computed(() => {
        return currentDate.value.getFullYear()
      })
      
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      
      const weeks = computed(() => {
        const year = currentDate.value.getFullYear()
        const month = currentDate.value.getMonth()
        
        // Get first day of month
        const firstDay = new Date(year, month, 1)
        // Get last day of month
        const lastDay = new Date(year, month + 1, 0)
        
        const startDay = firstDay.getDay()
        const endDay = lastDay.getDate()
        
        const weeks = []
        let week = []
        
        // Add empty days for start of month
        for (let i = 0; i < startDay; i++) {
          week.push({
            date: new Date(year, month, i - startDay + 1),
            isCurrentMonth: false
          })
        }
        
        // Add days of month
        for (let day = 1; day <= endDay; day++) {
          const date = new Date(year, month, day)
          week.push({
            date,
            isCurrentMonth: true,
            isToday: date.toDateString() === today.toDateString()
          })
          
          if (week.length === 7) {
            weeks.push(week)
            week = []
          }
        }
        
        // Add empty days for end of month
        if (week.length > 0) {
          const remaining = 7 - week.length
          for (let i = 1; i <= remaining; i++) {
            week.push({
              date: new Date(year, month + 1, i),
              isCurrentMonth: false
            })
          }
          weeks.push(week)
        }
        
        return weeks
      })
      
      function previousMonth() {
        currentDate.value = new Date(
          currentDate.value.getFullYear(),
          currentDate.value.getMonth() - 1,
          1
        )
      }
      
      function nextMonth() {
        currentDate.value = new Date(
          currentDate.value.getFullYear(),
          currentDate.value.getMonth() + 1,
          1
        )
      }
      
      function formatTime(timeString) {
        const [hours, minutes] = timeString.split(':')
        const hour = parseInt(hours)
        return `${hour % 12 || 12}:${minutes} ${hour >= 12 ? 'PM' : 'AM'}`
      }
      
      return {
        currentDate,
        currentMonth,
        currentYear,
        days,
        weeks,
        previousMonth,
        nextMonth,
        formatTime
      }
    },
    
    methods: {
      getShiftsForDay(date) {
        const dateStr = date.toISOString().split('T')[0]
        return this.shifts.filter(shift => shift.shift_date === dateStr)
      },
      
      getEmployeeName(employeeId) {
        const employee = this.employees.find(e => e.employee_id === employeeId)
        return employee ? `${employee.first_name} ${employee.last_name.charAt(0)}.` : 'Unknown'
      }
    }
  }
  </script>
  
  <style scoped>
  .shift-calendar {
    margin-top: 20px;
  }
  
  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .controls {
    display: flex;
    gap: 10px;
  }
  
  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
  }
  
  .day-header {
    padding: 10px;
    text-align: center;
    background-color: #f0f0f0;
    font-weight: bold;
  }
  
  .day-cell {
    min-height: 100px;
    border: 1px solid #ddd;
    padding: 5px;
    background-color: #fff;
  }
  
  .day-cell.current-month {
    background-color: #fff;
  }
  
  .day-cell:not(.current-month) {
    background-color: #f9f9f9;
    color: #999;
  }
  
  .day-cell.today {
    background-color: #e6f7ff;
    border: 2px solid #1890ff;
  }
  
  .day-number {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .shifts {
    max-height: 80px;
    overflow-y: auto;
  }
  
  .shift {
    background-color: #e6f7ff;
    border-left: 3px solid #1890ff;
    padding: 3px 5px;
    margin-bottom: 3px;
    font-size: 0.8rem;
    cursor: pointer;
  }
  
  .shift:hover {
    background-color: #bae7ff;
  }
  
  .employee {
    display: block;
    font-weight: bold;
  }
  
  .time {
    display: block;
    font-size: 0.7rem;
  }
  
  .pending {
    display: inline-block;
    background-color: #ffccc7;
    padding: 0 3px;
    border-radius: 3px;
    font-size: 0.7rem;
    margin-top: 2px;
  }
  </style>