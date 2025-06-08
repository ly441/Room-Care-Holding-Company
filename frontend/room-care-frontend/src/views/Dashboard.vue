<template>
    <div>
      <h1>Dashboard</h1>
      <div class="stats">
        <div class="stat-card">
          <h3>Total Branches</h3>
          <p>{{ branches.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Employees</h3>
          <p>{{ activeEmployeesCount }}</p>
        </div>
        <div class="stat-card">
          <h3>Upcoming Shifts</h3>
          <p>{{ upcomingShiftsCount }}</p>
        </div>
      </div>
  
      <div class="recent-activity">
        <h2>Recent Activity</h2>
        <ul>
          <li v-for="activity in recentActivities" :key="activity.id">
            {{ activity.message }} - {{ activity.time }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  
  export default {
    setup() {
      const store = useStore()
  
      onMounted(async () => {
        await store.dispatch('fetchBranches')
        await store.dispatch('fetchEmployees')
      })
  
      return {
        branches: computed(() => store.state.branches),
        activeEmployeesCount: computed(() => {
          return store.state.employees.filter(e => e.is_active).length
        }),
        upcomingShiftsCount: computed(() => 0), // Implement shift fetching
        recentActivities: [
          { id: 1, message: 'New branch added', time: '2 hours ago' },
          { id: 2, message: 'Payroll processed', time: '1 day ago' }
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  .stats {
    display: flex;
    gap: 20px;
    margin: 20px 0;
  }
  
  .stat-card {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    text-align: center;
  }
  
  .stat-card h3 {
    margin-top: 0;
  }
  
  .recent-activity {
    margin-top: 30px;
  }
  
  .recent-activity ul {
    list-style: none;
    padding: 0;
  }
  
  .recent-activity li {
    padding: 10px;
    border-bottom: 1px solid #eee;
  }
  </style>