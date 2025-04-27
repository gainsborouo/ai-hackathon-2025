<template>
  <!-- Main -->
  <div class="p-8 tracking-widest">
    <div class="mx-auto text-center">
      <div class="max-w-md mx-auto">
        <div class="font-mono">
          <h2 class="text-left text-xl font-bold text-black mb-6">註冊</h2>

          <div class="mt-6 mb-6">
            <div class="flex items-center">
              <label
                for="name"
                class="text-left mr-6 text-black font-semibold w-18"
                >帳號</label
              >
              <input
                id="name"
                type="text"
                v-model="name"
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus: outline-none"
              />
            </div>
          </div>

          <div class="mb-6">
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
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus: outline-none"
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
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus: outline-none"
              />
            </div>
          </div>

          <div class="mb-6">
            <div class="flex items-center">
              <label
                for="confirmPassword"
                class="text-left mr-6 text-black font-semibold w-18"
                >密碼確認</label
              >
              <input
                id="confirmPassword"
                type="password"
                v-model="confirmPassword"
                class="flex-1 px-3 py-1.5 border rounded-[0.6rem] focus: outline-none"
              />
            </div>
          </div>

          <div class="mb-6">
            <div class="flex flex-col">
              <label class="text-left mb-3 text-black font-semibold"
                >選擇大頭照</label
              >
              <div class="flex justify-between items-center gap-2">
                <div
                  v-for="id in 5"
                  :key="id"
                  @click="toggleAvatar(id)"
                  class="cursor-pointer p-1 rounded-full transition-all duration-200 w-[74px] h-[74px] flex items-center justify-center"
                  :class="{
                    'border-2 border-orange-500 bg-orange-100':
                      selectedAvatar === id,
                    'border-2 border-transparent hover:bg-gray-100':
                      selectedAvatar !== id,
                  }"
                >
                  <img
                    :src="`/avatar${id}.png`"
                    :alt="`Avatar ${id}`"
                    class="w-16 h-16 rounded-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="text-left mb-6 font-semibold">
            已經有帳號？
            <a href="/login" class="text-orange-500 font-bold underline"
              >登入</a
            >
          </div>

          <button
            @click="register"
            :disabled="!isFormValid"
            class="w-30 bg-orange-400 text-white font-bold py-2 rounded-3xl hover:bg-orange-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            送出
          </button>

          <div
            v-if="registrationSuccess"
            class="mt-4 text-green-600 font-semibold text-center"
          >
            註冊成功，請登入...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const apiBase = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const selectedAvatar = ref(null);
const registrationSuccess = ref(false);

const isFormValid = computed(() => {
  return (
    name.value.trim() !== "" &&
    email.value.trim() !== "" &&
    password.value.trim() !== "" &&
    password.value === confirmPassword.value &&
    selectedAvatar.value !== null
  );
});

const toggleAvatar = (id) => {
  if (selectedAvatar.value === id) {
    selectedAvatar.value = null;
  } else {
    selectedAvatar.value = id;
  }
};

const register = async () => {
  try {
    if (!isFormValid.value) {
      if (password.value !== confirmPassword.value) {
        alert("密碼與確認密碼不相符");
        return;
      }
      if (selectedAvatar.value === null) {
        alert("請選擇一個大頭照");
        return;
      }
      alert("所有欄位都必須填寫");
      return;
    }

    const registerData = {
      name: name.value,
      email: email.value,
      password: password.value,
      avatar: selectedAvatar.value,
    };

    const response = await fetch(`${apiBase}/user/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(registerData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "註冊失敗，請稍後再試");
    }

    registrationSuccess.value = true;

    name.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    selectedAvatar.value = null;

    setTimeout(() => {
      router.push({ name: "Login" });
    }, 2000);
  } catch (error) {
    alert(error.message);
  }
};
</script>
