<template>
  <div>
    <div
      @click="toggleSidebar"
      class="fixed top-24 right-1 text-[#0E1A37]rounded-full p-3 cursor-pointer z-30"
    >
      <i :class="['fas', isOpen ? 'fa-times' : 'fa-bars']"></i>
    </div>

    <transition name="slide-left">
      <div
        v-show="isOpen"
        class="fixed right-0 top-20 bottom-0 w-72 p-6 border-l-1 border-[#0E1A37] bg-[#f4f4f4] shadow-lg z-20 flex flex-col"
      >
        <div class="flex flex-col items-center mt-16 mb-6">
          <img
            :src="getAvatarUrl"
            alt="User"
            class="rounded-full mb-2 w-[60px] h-[60px] border-2 border-[#0E1A37]"
          />
          <div class="font-bold text-[#0E1A37]">{{ userData?.username }}</div>
        </div>

        <div class="flex flex-col gap-4 text-center font-semibold">
          <a
            href="/"
            class="py-2 px-4 hover:text-orange-400 hover:bg-gray-50 rounded-lg transition-colors"
            >首頁</a
          >
          <a
            href="/live"
            class="py-2 px-4 hover:text-orange-400 hover:bg-gray-50 rounded-lg transition-colors"
            >直播專區</a
          >
          <a
            href="/data"
            class="py-2 px-4 hover:text-orange-400 hover:bg-gray-50 rounded-lg transition-colors"
            >個人資料</a
          >
          <a
            @click="handleLogout"
            class="py-2 px-4 hover:text-orange-400 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer"
            >登出</a
          >
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div
        v-if="isOpen && isMobile"
        @click="toggleSidebar"
        class="fixed inset-0 bg-black bg-opacity-30 z-10"
      ></div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "../store/auth";
import axios from "axios";

const apiBase = import.meta.env.VITE_API_BASE_URL;

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const getAvatarUrl = computed(() => {
  if (!userData.value?.avatarUrl) {
    return '/default-avatar.png';
  }
  
//   // Check if the avatarUrl is already a complete URL
//   if (userData.value.avatarUrl.startsWith('http') || 
//       userData.value.avatarUrl.startsWith('https')) {
//     return userData.value.avatarUrl;
//   }
  
  // Handle a relative path
  return `/avatar${userData.value.avatarUrl}.png`;
});

const emit = defineEmits(["update:isOpen"]);
const router = useRouter();
const isMobile = ref(false);
const userData = ref({});
const isLoading = ref(false);

const checkIfMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

const toggleSidebar = () => {
  emit("update:isOpen", !props.isOpen);
};

const fetchUserData = async () => {
  try {
    isLoading.value = true;
    const token = authStore.getToken();

    if (!token) {
      userData.value = {};
      return;
    }

    const tokenParts = token.split('.');
    if (tokenParts.length === 3) {
      try {
        const base64Payload = tokenParts[1].replace(/-/g, '+').replace(/_/g, '/');
        const normalizedBase64 = base64Payload.padEnd(
          base64Payload.length + (4 - (base64Payload.length % 4)) % 4,
          '='
        );
        
        const payload = JSON.parse(atob(normalizedBase64));

        userData.value = {
          id: payload.id,
          username: payload.name,
          avatarUrl: payload.avatar,
          email: payload.email,
          fanClass: payload.class,
          credit: payload.credit,
          role: payload.role
        };
        
        console.log("Extracted user data from token:", userData.value);
      } catch (decodeError) {
        console.error("Failed to decode JWT token:", decodeError);
        authStore.setToken(null);
      }
    }
  } catch (error) {
    console.error("獲取用戶數據失敗:", error);
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = () => {
  authStore.setToken(null);

  router.push({ name: "Login" });

  toggleSidebar();
};

onMounted(() => {
  checkIfMobile();
  window.addEventListener("resize", checkIfMobile);
  fetchUserData();
});

onUnmounted(() => {
  window.removeEventListener("resize", checkIfMobile);
});
</script>

<style scoped>
.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.3s ease;
}

.slide-left-enter-from,
.slide-left-leave-to {
  transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
