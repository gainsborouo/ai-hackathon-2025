<template>
  <div class="p-8 tracking-widest">
    <div class="mx-auto text-center">
      <div class="max-w-md mx-auto">
        <div class="font-mono">
          <h2 class="text-left text-xl font-bold text-black mb-6">
            登入以見到你最愛的偶像🌟
          </h2>

          <div class="mt-6 mb-6">
            <div class="flex items-center">
              <label
                for="email"
                class="text-left mr-6 text-black font-semibold w-18"
                >電子郵件</label
              >
              <input
                id="email"
                type="email"
                v-model="email"
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus:outline-none"
              />
            </div>
          </div>

          <div class="mb-6">
            <div class="flex items-center">
              <label
                for="password"
                class="text-left mr-6 text-black font-semibold w-18"
                >密碼</label
              >
              <input
                id="password"
                type="password"
                v-model="password"
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus:outline-none"
              />
            </div>
          </div>

          <div class="text-left mb-6 font-semibold">
            還沒有帳號？
            <a href="/register" class="text-orange-500 font-bold underline"
              >註冊一個</a
            >
          </div>

          <button
            @click="localLogin"
            :disabled="!email || !password"
            class="w-30 bg-orange-400 text-white font-bold py-2 rounded-3xl hover:bg-orange-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            登入
          </button>

          <div
            v-if="isTokenReceived"
            class="mt-4 text-green-600 font-semibold text-center"
          >
            登入成功，正在導向...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "../store/auth";

const apiBase = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const email = ref("");
const password = ref("");
const isTokenReceived = ref(false);

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");
  if (token) {
    authStore.setToken(token);
    isTokenReceived.value = true;
    router.replace({ name: "Home" });
  }
});

const localLogin = async () => {
  try {
    if (!email.value.trim() || !password.value.trim()) {
      alert("Email and password cannot be empty.");
      return;
    }

    const loginData = {
      email: email.value,
      password: password.value,
    };

    const response = await fetch(`${apiBase}/user/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginData),
    });

    if (!response.ok) throw new Error("登入失敗，請檢查帳號與密碼");

    const data = await response.json();
    if (data.token) {
      authStore.setToken(data.token);
      router.replace({ name: "Home" });
    }
  } catch (error) {
    alert(error.message);
  }
};
</script>
