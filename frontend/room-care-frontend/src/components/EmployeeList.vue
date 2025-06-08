

<template>
    <div class="employee-list">
      <div class="list-header">
        <h3>Employees</h3>
        <div class="actions">
          <input v-model="searchQuery" placeholder="Search employees..." @input="filterEmployees">
          <button @click="$emit('add-employee')">Add Employee</button>
        </div>
      </div>
      
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>Hourly Rate</th>
            <th>Branch</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in filteredEmployees" :key="employee.employee_id">
            <td>{{ employee.employee_id }}</td>
            <td>{{ employee.first_name }} {{ employee.last_name }}</td>
            <td>{{ employee.role }}</td>
            <td>${{ employee.hourly_rate.toFixed(2) }}</td>
            <td>{{ getBranchName(employee.branch_id) }}</td>
            <td :class="employee.is_active ? 'active' : 'inactive'">
              {{ employee.is_active ? 'Active' : 'Inactive' }}
            </td>
            <td>
              <button @click="$emit('edit-employee', employee)">Edit</button>
              <button @click="$emit('toggle-status', employee)">
                {{ employee.is_active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredEmployees.length === 0" class="empty-state">
        No employees found
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue'
  
  export default {
    props: {
      employees: {
        type: Array,
        default: () => []
      },
      branches: {
        type: Array,
        default: () => []
      }
    },
    
    setup(props) {
      const searchQuery = ref('')
      
      const filteredEmployees = computed(() => {
        if (!searchQuery.value) return props.employees
        const query = searchQuery.value.toLowerCase()
        return props.employees.filter(emp => 
          emp.first_name.toLowerCase().includes(query) ||
          emp.last_name.toLowerCase().includes(query) ||
          emp.role.toLowerCase().includes(query) ||
          emp.email.toLowerCase().includes(query))
      })
      
      const getBranchName = (branchId) => {
        const branch = props.branches.find(b => b.branch_id === branchId)
        return branch ? branch.branch_name : 'Unknown'
      }
      
      return {
        searchQuery,
        filteredEmployees,
        getBranchName
      }
    }
  }
  </script>
  
  <style scoped>
  .employee-list {
    margin-top: 20px;
  }
  
  .active {
    color: green;
    font-weight: bold;
  }
  
  .inactive {
    color: #999;
  }
  </style>