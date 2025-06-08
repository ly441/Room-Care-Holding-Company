<template>
    <div>
      <h2>Employees</h2>
      <div class="controls">
        <input v-model="searchQuery" placeholder="Search employees..." @input="filterEmployees">
        <button @click="showAddForm = true">Add Employee</button>
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
            <td>{{ employee.is_active ? 'Active' : 'Inactive' }}</td>
            <td>
              <button @click="editEmployee(employee)">Edit</button>
              <button @click="toggleEmployeeStatus(employee)">
                {{ employee.is_active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <div v-if="showAddForm || editingEmployee" class="form">
        <h3>{{ editingEmployee ? 'Edit' : 'Add' }} Employee</h3>
        <input v-model="currentEmployee.first_name" placeholder="First Name">
        <input v-model="currentEmployee.last_name" placeholder="Last Name">
        <input v-model="currentEmployee.email" placeholder="Email" type="email">
        <input v-model="currentEmployee.role" placeholder="Role">
        <input v-model="currentEmployee.hourly_rate" placeholder="Hourly Rate" type="number" step="0.01">
        <select v-model="currentEmployee.branch_id">
          <option v-for="branch in branches" :value="branch.branch_id" :key="branch.branch_id">
            {{ branch.branch_name }}
          </option>
        </select>
        <div>
          <button @click="saveEmployee">Save</button>
          <button @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import axios from 'axios'
  
  export default {
    setup() {
      const store = useStore()
      const searchQuery = ref('')
      const showAddForm = ref(false)
      const editingEmployee = ref(null)
      const currentEmployee = ref({
        first_name: '',
        last_name: '',
        email: '',
        role: '',
        hourly_rate: 0,
        branch_id: null
      })
      const filteredEmployees = ref([])
  
      onMounted(async () => {
        await store.dispatch('fetchBranches')
        await store.dispatch('fetchEmployees')
        filteredEmployees.value = store.state.employees
      })
  
      const getBranchName = (branchId) => {
        const branch = store.state.branches.find(b => b.branch_id === branchId)
        return branch ? branch.branch_name : 'Unknown'
      }
  
      const filterEmployees = () => {
        if (!searchQuery.value) {
          filteredEmployees.value = store.state.employees
          return
        }
        const query = searchQuery.value.toLowerCase()
        filteredEmployees.value = store.state.employees.filter(emp => 
          emp.first_name.toLowerCase().includes(query) ||
          emp.last_name.toLowerCase().includes(query) ||
          emp.role.toLowerCase().includes(query)
        )
      }
  
      const editEmployee = (employee) => {
        currentEmployee.value = { ...employee }
        editingEmployee.value = employee
        showAddForm.value = true
      }
  
      const saveEmployee = async () => {
        try {
          if (editingEmployee.value) {
            await axios.put(`/api/employees/${currentEmployee.value.employee_id}`, currentEmployee.value)
          } else {
            await axios.post('/api/employees/', currentEmployee.value)
          }
          await store.dispatch('fetchEmployees')
          cancelEdit()
        } catch (error) {
          console.error('Error saving employee:', error)
        }
      }
  
      const toggleEmployeeStatus = async (employee) => {
        try {
          await axios.patch(`/api/employees/${employee.employee_id}`, {
            is_active: !employee.is_active
          })
          await store.dispatch('fetchEmployees')
        } catch (error) {
          console.error('Error updating employee status:', error)
        }
      }
  
      const cancelEdit = () => {
        currentEmployee.value = {
          first_name: '',
          last_name: '',
          email: '',
          role: '',
          hourly_rate: 0,
          branch_id: null
        }
        editingEmployee.value = null
        showAddForm.value = false
      }
  
      return {
        branches: computed(() => store.state.branches),
        searchQuery,
        showAddForm,
        editingEmployee,
        currentEmployee,
        filteredEmployees,
        getBranchName,
        filterEmployees,
        editEmployee,
        saveEmployee,
        toggleEmployeeStatus,
        cancelEdit
      }
    }
  }
  </script>
  
  <style scoped>
  .controls {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  
  select {
    display: block;
    margin: 10px 0;
    padding: 8px;
    width: 300px;
  }
  </style>