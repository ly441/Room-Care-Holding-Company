<template>
    <div>
      <h2>Branches</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Address</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="branch in branches" :key="branch.branch_id">
            <td>{{ branch.branch_id }}</td>
            <td>{{ branch.branch_name }}</td>
            <td>{{ branch.address }}</td>
            <td>
              <button @click="editBranch(branch)">Edit</button>
              <button @click="deleteBranch(branch.branch_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="form">
        <h3>{{ editing ? 'Edit' : 'Add' }} Branch</h3>
        <input v-model="currentBranch.branch_name" placeholder="Name">
        <input v-model="currentBranch.address" placeholder="Address">
        <button @click="saveBranch">Save</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        branches: [],
        currentBranch: { branch_id: null, branch_name: '', address: '' },
        editing: false
      }
    },
    async created() {
      await this.$store.dispatch('fetchBranches')
      this.branches = this.$store.state.branches
    },
    methods: {
      async saveBranch() {
        if (this.editing) {
          await axios.put(`/api/branches/${this.currentBranch.branch_id}`, this.currentBranch)
        } else {
          await axios.post('/api/branches/', this.currentBranch)
        }
        this.resetForm()
        await this.$store.dispatch('fetchBranches')
      },
      editBranch(branch) {
        this.currentBranch = { ...branch }
        this.editing = true
      },
      async deleteBranch(id) {
        if (confirm('Are you sure?')) {
          await axios.delete(`/api/branches/${id}`)
          await this.$store.dispatch('fetchBranches')
        }
      },
      resetForm() {
        this.currentBranch = { branch_id: null, branch_name: '', address: '' }
        this.editing = false
      }
    }
  }
  </script>