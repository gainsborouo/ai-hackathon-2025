import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Live from "../views/Live.vue";
import Data from "../views/Data.vue";
import axios from "axios";
import { authStore } from "../store/auth";

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

router.beforeEach(async (to, from, next) => {
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

  if (from.name === "Live" && to.name !== "Live") {
    console.log("Leaving Live view, ensuring watch session is closed");

    try {
      const activeWatchTimeId = localStorage.getItem("activeWatchTimeId");

      if (activeWatchTimeId) {
        console.log("Found active watch session:", activeWatchTimeId);
        const apiBase = import.meta.env.VITE_API_BASE_URL;

        await axios.post(
          `${apiBase}/watch/stop`,
          {},
          {
            headers: {
              Authorization: `Bearer ${authStore.getToken()}`,
              "Content-Type": "application/json",
            },
          }
        );

        console.log("Successfully closed watch session during navigation");
        localStorage.removeItem("activeWatchTimeId");
      }
    } catch (error) {
      console.error("Failed to close watch session during navigation:", error);
      // Remove the ID from localStorage even if the API call fails
      localStorage.removeItem("activeWatchTimeId");
    }
  }

  // Always allow navigation to continue
  next();
});

export default router;
