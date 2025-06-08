
<template>
  <div id="app">
    <nav v-if="isAuthenticated">
      <router-link to="/dashboard">Dashboard</router-link> |
      <router-link to="/branches">Branches</router-link> |
      <router-link to="/employees">Employees</router-link> |
      <button @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const logout = () => {
      store.dispatch("logout");
      router.push("/login");
    };

    const isAuthenticated = computed(() => store.getters.isAuthenticated);

    return { logout, isAuthenticated };
  },
};
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
