import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      first_name: null,
      last_name: null,
      email: null,
      organization_name: null,
      access: null,
      refresh: null,
    },
    inactivityTimeout: null, // Track the inactivity timer
    tokenExpirationTime: 12 * 60 * 60 * 1000 // 12 hours to auto log off.
  }),

  actions: {
    initStore() {
      if (localStorage.getItem("user.access")) {
        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.first_name = localStorage.getItem("user.first_name");
        this.user.last_name = localStorage.getItem("user.last_name");
        this.user.email = localStorage.getItem("user.email");
        this.user.organization_name = localStorage.getItem("user.organization_name");
        this.user.isAuthenticated = true;
        this.refreshToken();
        this.resetInactivityTimer();
      }
    },

    setToken(data) {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;
      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
      this.resetInactivityTimer();
    },

    removeToken() {
      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.first_name = null;
      this.user.last_name = null;
      this.user.email = null;
      this.user.organization_name = null;
      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.first_name", "");
      localStorage.setItem("user.last_name", "");
      localStorage.setItem("user.email", "");
      localStorage.setItem("user.organization_name", "");
      clearTimeout(this.inactivityTimeout);
    },

    setUserInfo(user) {
      this.user.id = user.id;
      this.user.first_name = user.first_name;
      this.user.last_name = user.last_name;
      this.user.email = user.email;
      this.user.organization_name = user.organization_name;
      localStorage.setItem("user.id", this.user.id);
      localStorage.setItem("user.first_name", this.user.first_name);
      localStorage.setItem("user.last_name", this.user.last_name);
      localStorage.setItem("user.email", this.user.email);
      localStorage.setItem("user.organization_name", this.user.organization_name);
    },

    resetInactivityTimer() {
      clearTimeout(this.inactivityTimeout);
      this.inactivityTimeout = setTimeout(() => {
        this.logout();
      }, this.tokenExpirationTime);
    },

    logout() {
      this.removeToken();
      if (this.router) {
        this.router.push('/login');
      } else {
        console.error("Router instance not found");
      }
    },

    refreshToken() {
      axios
        .post("/api/accounts/token/refresh/", {
          refresh: this.user.refresh,
        })
        .then((response) => {
          this.user.access = response.data.access;
          localStorage.setItem("user.access", response.data.access);
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);
          this.logout();
        });
    },

    trackUserActivity() {
      window.addEventListener('mousemove', this.resetInactivityTimer);
      window.addEventListener('keydown', this.resetInactivityTimer);
      window.addEventListener('scroll', this.resetInactivityTimer);
    }
    
  },
});
