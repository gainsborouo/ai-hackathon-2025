<template>
  <div class="p-8 tracking-widest">
    <Sidebar v-model:isOpen="sidebarOpen" />
    <div class="mx-auto text-center">
      <div class="max-w-md mx-auto">
        <div class="font-mono">
          <h2 class="text-left text-xl font-bold text-black mb-6">個人資料</h2>

          <div v-if="isLoading" class="text-center py-8">
            <div class="text-gray-600">資料載入中...</div>
          </div>

          <div v-else-if="!userData.id" class="text-center py-8">
            <div class="text-gray-600">請先登入查看您的個人資料</div>
            <a
              href="/login"
              class="text-orange-500 font-bold underline mt-4 inline-block"
              >前往登入</a
            >
          </div>

          <div v-else>
            <div class="flex justify-center mb-8">
              <div class="relative">
                <img
                  :src="getAvatarUrl"
                  alt="User Avatar"
                  class="w-24 h-24 rounded-full border-2 border-[#0E1A37] object-cover"
                />
              </div>
            </div>

            <div class="mt-6 mb-6">
              <div class="flex items-center">
                <div class="text-left mr-6 text-black font-semibold w-24">
                  帳號
                </div>
                <div
                  class="flex-1 px-3 py-1.5 text-left border rounded-[0.6rem] bg-gray-50"
                >
                  {{ userData.username }}
                </div>
              </div>
            </div>

            <div class="mb-6">
              <div class="flex items-center">
                <div class="text-left mr-6 text-black font-semibold w-24">
                  電子郵件
                </div>
                <div
                  class="flex-1 px-3 py-1.5 text-left border rounded-[0.6rem] bg-gray-50"
                >
                  {{ userData.email }}
                </div>
              </div>
            </div>

            <div class="mb-6">
              <div class="flex items-center">
                <div class="text-left mr-6 text-black font-semibold w-24">
                  粉絲等級
                </div>
                <div
                  class="flex-1 px-3 py-1.5 text-left border rounded-[0.6rem] bg-gray-50"
                >
                  {{ userData.fanClass || "一般會員" }}
                </div>
              </div>
            </div>

            <div class="mb-6">
              <div class="flex items-center">
                <div class="text-left mr-6 text-black font-semibold w-24">
                  我的星星
                </div>
                <div
                  class="flex-1 px-3 py-1.5 text-left border rounded-[0.6rem] bg-gray-50"
                >
                  {{ userData.credit || 0 }} ⭐
                </div>
              </div>
            </div>

            <div v-if="userData.role" class="mb-6">
              <div class="flex items-center">
                <div class="text-left mr-6 text-black font-semibold w-24">
                  使用者身份
                </div>
                <div
                  class="flex-1 px-3 py-1.5 text-left border rounded-[0.6rem] bg-gray-50"
                >
                  {{ roleDisplay }}
                </div>
              </div>
            </div>

            <div class="flex justify-center mt-8">
              <button
                @click="goBack"
                class="w-30 bg-orange-400 text-white font-bold py-2 px-6 rounded-3xl hover:bg-orange-500 transition"
              >
                返回
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "../store/auth";
import Sidebar from "../components/Sidebar.vue";

const sidebarOpen = ref(false);

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const router = useRouter();
const userData = ref({});
const isLoading = ref(true);

const getAvatarUrl = computed(() => {
  if (!userData.value?.avatarUrl) {
    return "/default-avatar.png";
  }

  // Handle a relative path
  return `/avatar${userData.value.avatarUrl}.png`;
});

const roleDisplay = computed(() => {
  const role = userData.value.role;
  if (!role) return "一般會員";

  const roleMap = {
    fans: "粉絲",
    idol: "偶像",
  };

  return roleMap[role] || "其他";
});

const fetchUserData = () => {
  try {
    isLoading.value = true;
    const token = authStore.getToken();

    if (!token) {
      userData.value = {};
      return;
    }

    const tokenParts = token.split(".");
    if (tokenParts.length === 3) {
      try {
        const base64Payload = tokenParts[1]
          .replace(/-/g, "+")
          .replace(/_/g, "/");
        const normalizedBase64 = base64Payload.padEnd(
          base64Payload.length + ((4 - (base64Payload.length % 4)) % 4),
          "="
        );

        const payload = JSON.parse(atob(normalizedBase64));

        userData.value = {
          id: payload.id,
          username: payload.name,
          avatarUrl: payload.avatar,
          email: payload.email,
          fanClass: payload.class,
          credit: payload.credit,
          role: payload.role,
        };

        console.log("Profile data extracted:", userData.value);
      } catch (decodeError) {
        console.error("Failed to decode JWT token:", decodeError);
      }
    }
  } catch (error) {
    console.error("獲取用戶數據失敗:", error);
  } finally {
    isLoading.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchUserData();
});
</script>
