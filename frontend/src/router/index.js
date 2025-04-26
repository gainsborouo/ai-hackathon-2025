import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Live from "../views/Live.vue";
import Data from "../views/Data.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/live",
    name: "Live",
    component: Live,
  },
  {
    path: "/data",
    name: "Data",
    component: Data,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("jwtToken");
  if (to.meta.requiresAuth) {
    if (!token) {
      next({ name: "Login" });
    } else {
      next();
    }
  } else {
    if (to.name === "Login" && token) {
      next({ name: "Home" });
    } else {
      next();
    }
  }
});

export default router;
