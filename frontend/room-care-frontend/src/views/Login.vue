
<template>
  <div class="login-container">
    <h2>Room and Care Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="email" placeholder="Email" type="email" required />
      <input v-model="password" placeholder="Password" type="password" required />
      <button type="submit" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const email = ref("");
    const password = ref("");
    const error = ref("");
    const loading = ref(false);

    const store = useStore();
    const router = useRouter();

    const handleLogin = async () => {
      error.value = "";
      loading.value = true;
      try {
        await store.dispatch("login", {
          email: email.value,
          password: password.value,
        });
        router.push("/dashboard");
      } catch (err) {
        error.value = err.message || "Login failed. Please check your credentials.";
      } finally {
        loading.value = false;
      }
    };

    return { email, password, error, loading, handleLogin };
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 50px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
