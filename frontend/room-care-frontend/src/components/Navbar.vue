<template>
    <nav>
      <router-link to="/dashboard">Dashboard</router-link> |
      <router-link to="/branches">Branches</router-link> |
      <router-link to="/employees">Employees</router-link> |
      <router-link to="/shifts">Shifts</router-link> |
      <button @click="logout">Logout</button>
    </nav>
  </template>
  
  <script>
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  export default {
    setup() {
      const store = useStore()
      const router = useRouter()
  
      const logout = () => {
        store.commit('setToken', '')
        router.push('/login')
      }
  
      return { logout }
    }
  }
  </script>
  
  <style scoped>
  nav {
    padding: 10px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
  }
  
  nav a {
    margin: 0 5px;
    text-decoration: none;
    color: #2c3e50;
  }
  
  nav a.router-link-exact-active {
    color: #42b983;
    font-weight: bold;
  }
  
  nav button {
    margin-left: 10px;
    padding: 5px 10px;
    background: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>