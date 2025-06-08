
import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Branches from "../views/Branches.vue";
import Employees from "../views/Employees.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/branches", component: Branches, meta: { requiresAuth: true } },
  { path: "/employees", component: Employees, meta: { requiresAuth: true } },
  { path: "/", redirect: "/dashboard" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const token = localStorage.getItem("token");
  const isAuthenticated = !!token;

  console.log(
    "Routing to:",
    to.path,
    "Requires auth?",
    requiresAuth,
    "Authenticated?",
    isAuthenticated
  );

  if (requiresAuth && !isAuthenticated) {
    next("/login");
  } else if (to.path === "/login" && isAuthenticated) {
    // Redirect logged-in users away from login page
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
