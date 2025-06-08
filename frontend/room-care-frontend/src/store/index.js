
import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    token: localStorage.getItem("token") || "",
    branches: [],
    employees: [],
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    setBranches(state, branches) {
      state.branches = branches;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/token",
          `username=${credentials.email}&password=${credentials.password}`,
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );
        commit("setToken", response.data.access_token);
      } catch (error) {
        // Propagate error to component
        throw new Error("Invalid login credentials");
      }
    },
    logout({ commit }) {
      commit("setToken", "");
    },
    async fetchBranches({ commit, state }) {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/branches/",
          {
            headers: { Authorization: `Bearer ${state.token}` },
          }
        );
        commit("setBranches", response.data);
      } catch (error) {
        console.error("Failed to fetch branches:", error);
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
});
