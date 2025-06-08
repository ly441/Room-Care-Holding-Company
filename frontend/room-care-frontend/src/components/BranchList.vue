
<template>
    <div class="branch-list">
      <div class="list-header">
        <h3>Branches</h3>
        <div class="actions">
          <input v-model="searchQuery" placeholder="Search branches..." />
          <button @click="$emit('add-branch')">Add Branch</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Address</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="branch in filteredBranches" :key="branch.branch_id">
            <td>{{ branch.branch_id }}</td>
            <td>{{ branch.branch_name }}</td>
            <td>{{ branch.address }}</td>
            <td>{{ branch.phone }}</td>
            <td>
              <button @click="$emit('edit-branch', branch)">Edit</button>
              <button @click="$emit('delete-branch', branch.branch_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredBranches.length === 0" class="empty-state">
        No branches found
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { toRefs } from 'vue'
  
  const props = defineProps({
    branches: {
      type: Array,
      default: () => []
    }
  })
  
  const { branches } = toRefs(props)
  const searchQuery = ref('')
  
  const filteredBranches = computed(() => {
    if (!searchQuery.value) return branches.value
    const query = searchQuery.value.toLowerCase()
    return branches.value.filter(branch =>
      (branch.branch_name && branch.branch_name.toLowerCase().includes(query)) ||
      (branch.address && branch.address.toLowerCase().includes(query)) ||
      (branch.phone && branch.phone.toLowerCase().includes(query))
    )
  })
  </script>
  
  <style scoped>
  .branch-list {
    margin-top: 20px;
  }
  
  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .actions {
    display: flex;
    gap: 10px;
  }
  
  .actions input {
    padding: 5px 10px;
    width: 250px;
  }
  
  .empty-state {
    padding: 20px;
    text-align: center;
    background-color: #f9f9f9;
    border: 1px solid #eee;
    margin-top: 10px;
  }
  </style>