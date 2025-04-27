import { reactive } from "vue";

export const authStore = reactive({
  token: localStorage.getItem("jwtToken") || null,

  setToken(newToken) {
    this.token = newToken;
    if (newToken) {
      localStorage.setItem("jwtToken", newToken);
    } else {
      localStorage.removeItem("jwtToken");
    }
  },

  getToken() {
    return localStorage.getItem("jwtToken");
  },
  
  isAuthenticated() {
    return !!this.getToken();
  },
  
  clearAuth() {
    this.setToken(null);
  },

  logout() {
    if (window.appCleanupCallbacks && Array.isArray(window.appCleanupCallbacks)) {
      window.appCleanupCallbacks.forEach(callback => {
        if (typeof callback === 'function') {
          try {
            callback();
          } catch (e) {
            console.error('Error in cleanup callback:', e);
          }
        }
      });
    }

    localStorage.removeItem("jwtToken");
  }
});