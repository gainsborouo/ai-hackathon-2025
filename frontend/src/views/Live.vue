<template>
  <div class="flex justify-center h-[60dvh]">
    <div class="flex p-6 tracking-widest w-full max-w-6xl mx-auto">
      <Sidebar v-model:isOpen="sidebarOpen" />
      <div class="flex-1 bg-[#0E1A37] rounded-2xl mr-6 flex flex-col">
        <div class="flex-1"></div>

        <div class="p-3 flex items-center">
          <div class="flex items-center">
            <div class="h-3 w-3 rounded-full bg-red-500 mr-2"></div>
            <span class="text-white text-sm">直播中</span>
          </div>
          <div class="ml-4 text-white text-sm">深夜聊聊天</div>
          <div
            class="ml-2 bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full"
          >
            粉絲限定
          </div>
          <div class="ml-auto">
            <div class="bg-gray-700 rounded-full px-3 py-1">
              <span class="text-white text-sm">FENiX</span>
            </div>
          </div>
        </div>
      </div>

      <div
        class="w-72 flex flex-col bg-white rounded-2xl border border-[#0E1A37] p-3"
      >
        <div class="flex-1 overflow-y-auto space-y-4 max-h-[calc(100vh-6rem)]">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex items-start gap-2"
          >
            <img
              :src="message.avatarUrl"
              alt="avatar"
              class="w-8 h-8 rounded-full"
            />
            <div>
              <div class="flex items-center gap-1">
                <div class="font-bold text-[#0E1A37] text-sm">
                  {{ message.username }}
                </div>
                <span
                  v-if="message.tag"
                  :class="[
                    'text-xs text-white rounded-full px-2 py-0.5 text-[10px]',
                    message.tag === '超級粉絲' ? 'bg-orange-400' : 'bg-red-400',
                  ]"
                >
                  {{ message.tag }}
                </span>
              </div>
              <div class="text-[#0E1A37] mt-0.5 text-sm">
                {{ message.content }}
              </div>
            </div>
          </div>
        </div>

        <div class="mt-2 flex items-center">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="你有什麼意見？？？"
            class="flex-1 border rounded-full px-3 py-1.5 text-sm text-[#0E1A37] focus:outline-none"
          />
          <button @click="sendMessage" class="ml-2 text-[#0E1A37]">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Sidebar from "../components/Sidebar.vue";
import { authStore } from "../store/auth";

const sidebarOpen = ref(false);
const inputMessage = ref("");
const userData = ref({});
const isAuthenticated = ref(false);

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const getUserDataFromToken = () => {
  try {
    const token = authStore.getToken();

    if (!token) {
      userData.value = {};
      isAuthenticated.value = false;
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

        isAuthenticated.value = true;
        console.log("Live: User data extracted:", userData.value);
      } catch (decodeError) {
        console.error("Failed to decode JWT token:", decodeError);
        isAuthenticated.value = false;
      }
    }
  } catch (error) {
    console.error("Error getting user data:", error);
    isAuthenticated.value = false;
  }
};

const messages = ref([
  {
    username: "orzzzzzzzzzzzzzzzzzzzz",
    avatarUrl: "/avatar1.png",
    content: "蟲合",
    tag: null,
  },
  {
    username: "熾氣a哞噗",
    avatarUrl: "/avatar2.png",
    content: "好喜歡><",
    tag: "超級粉絲",
  },
  {
    username: "滅火器",
    avatarUrl: "/avatar3.png",
    content: "承隆好帥❤️❤️",
    tag: "專屬粉絲",
  },
]);

const getFanClassTag = (classValue) => {
  const tagMap = {
    1: "",
    2: "專屬粉絲",
    3: "超級粉絲",
  };
  return tagMap[classValue] || null;
};

const sendMessage = () => {
  if (!isAuthenticated.value) {
    alert("請先登入才能發送訊息");
    return;
  }

  if (inputMessage.value.trim() !== "") {
    messages.value.push({
      username: userData.value.username || "訪客",
      avatarUrl: userData.value.avatarUrl
        ? `/avatar${userData.value.avatarUrl}.png`
        : "/default-avatar.png",
      content: inputMessage.value,
      tag: getFanClassTag(userData.value.fanClass),
    });
    inputMessage.value = "";
  }
};

onMounted(() => {
  getUserDataFromToken();
});
</script>

<style scoped>
::-webkit-scrollbar {
  width: 4px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 9999px;
}
</style>
