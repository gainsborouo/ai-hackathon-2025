<template>
  <div class="flex justify-center h-[60dvh]">
    <div class="flex p-6 tracking-widest w-full max-w-6xl mx-auto">
      <Sidebar v-model:isOpen="sidebarOpen" />
      <div class="flex-1 bg-[#0E1A37] rounded-2xl mr-6 flex flex-col">
        <div class="flex-1 relative">
          <div v-if="streamUrl" class="w-full h-full">
            <div v-if="isIdol" class="absolute top-4 right-4 z-10">
              <button
                @click="stopStream"
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md shadow-lg flex items-center"
              >
                <span class="mr-2">結束直播</span>
                <i class="fas fa-stop-circle"></i>
              </button>
            </div>
            <video
              ref="videoPlayer"
              class="w-full h-[90%] translate-y-14"
              autoplay
              controls
              muted
            ></video>
          </div>
          <div
            v-else-if="isIdol"
            class="w-full h-full flex flex-col items-center justify-center"
          >
            <div class="text-white text-2xl mb-6">開始您的直播</div>
            <div
              class="flex flex-col gap-4 w-80 bg-[#1C2A4D] p-6 rounded-lg shadow-lg"
            >
              <div>
                <label class="text-white text-sm mb-1 block">直播標題</label>
                <input
                  v-model="newStreamTitle"
                  type="text"
                  placeholder="輸入直播標題..."
                  class="w-full px-3 py-2 rounded-md text-white"
                />
              </div>
              <div>
                <label class="text-white text-sm mb-1 block">觀眾限制</label>
                <select
                  v-model="newStreamClass"
                  class="w-full px-3 py-2 rounded-md text-white"
                >
                  <option value="1">所有人可見</option>
                  <option value="2">專屬粉絲限定</option>
                  <option value="3">超級粉絲限定</option>
                </select>
              </div>
              <button
                @click="startStream"
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded-md flex items-center justify-center mt-2"
              >
                <div
                  class="h-3 w-3 rounded-full bg-white animate-pulse mr-2"
                ></div>
                <span>開始直播</span>
              </button>
            </div>
          </div>
          <div v-else class="w-full h-full flex items-center justify-center">
            <div class="text-white text-lg">等待直播開始...</div>
          </div>
        </div>

        <div class="p-3 flex items-center">
          <div v-if="streamUrl" class="flex items-center">
            <div class="h-3 w-3 rounded-full bg-red-500 mr-2"></div>
            <span class="text-white text-sm">直播中</span>
          </div>
          <div v-if="streamUrl" class="ml-4 text-white text-sm">
            <div class="ml-4 text-white text-sm">
              {{
                liveTitle || (streamUrl ? "未命名直播" : "目前沒有進行中的直播")
              }}
            </div>
          </div>
          <div
            v-if="liveAccess"
            class="ml-2 bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full"
          >
            {{ liveAccess }}
          </div>
          <div class="ml-auto">
            <div v-if="idolName" class="bg-gray-700 rounded-full px-3 py-1">
              <span class="text-white text-sm">{{ idolName }}</span>
            </div>
          </div>
        </div>
      </div>

      <div
        class="w-72 flex flex-col bg-white rounded-2xl border border-[#0E1A37] p-3"
      >
        <div
          class="flex-1 overflow-y-auto space-y-4 max-h-[calc(100vh-6rem)]"
          ref="chatContainer"
        >
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
                <span
                  v-if="message.user_class == 1"
                  :class="['text-xs px-0.5 py-0.5']"
                >
                  👑
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
            placeholder="輸入留言..."
            class="flex-1 border rounded-full px-3 py-1.5 text-sm text-[#0E1A37] focus:outline-none"
            @keyup.enter="sendMessage"
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
import {
  ref,
  computed,
  onMounted,
  nextTick,
  watch,
  onBeforeUnmount,
} from "vue";
import Sidebar from "../components/Sidebar.vue";
import { authStore } from "../store/auth";
import axios from "axios";
import { onBeforeRouteLeave } from "vue-router";

const apiBase = import.meta.env.VITE_API_BASE_URL;
const sidebarOpen = ref(false);
const inputMessage = ref("");
const userData = ref({});
const isAuthenticated = ref(false);
const messages = ref([]);
const chatContainer = ref(null);
const videoPlayer = ref(null);
const streamUrl = ref(null);
const liveTitle = ref(null);
const liveAccess = ref(null);
const idolName = ref(null);
const liveId = ref(null);
const watchTimeId = ref(null);
const isIdol = ref(false);
const newStreamTitle = ref("");
const newStreamClass = ref("1");
const commentIntervalId = ref(null);

watch(streamUrl, (newUrl) => {
  if (newUrl && videoPlayer.value) {
    // console.log("Loading video stream:", newUrl);
    videoPlayer.value.src = newUrl;
    videoPlayer.value.load();
    videoPlayer.value
      .play()
      .catch((err) => console.error("Video playback error:", err));
  }
});

const isUserIdol = computed(() => {
  return userData.value?.role === "idol";
});

watch(messages, () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
});

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const getAvatarUrl = computed(() => {
  if (!userData.value?.avatarUrl) {
    return "/default-avatar.png";
  }

  return `/avatar${userData.value.avatarUrl}.png`;
});

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

        isIdol.value = payload.role === "idol";
        isAuthenticated.value = true;
        // console.log("Live: User data extracted:", userData.value);
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

const getFanClassTag = (classValue) => {
  const tagMap = {
    1: "",
    2: "專屬粉絲",
    3: "超級粉絲",
  };
  return tagMap[classValue] || null;
};

const getLiveAccessText = (fansClass) => {
  const classMap = {
    1: "",
    2: "專屬粉絲限定",
    3: "超級粉絲限定",
  };
  return classMap[fansClass] || "";
};

const startStream = async () => {
  if (!isIdol.value) {
    console.error("Only idols can start streams");
    return;
  }

  try {
    const response = await axios.post(
      `${apiBase}/ls/create`,
      {
        title: newStreamTitle.value || "未命名直播",
        fans_class: parseInt(newStreamClass.value),
      },
      {
        headers: {
          Authorization: `Bearer ${authStore.getToken()}`,
          "Content-Type": "application/json",
        },
      }
    );

    // console.log("Stream created:", response.data);

    fetchCurrentLive();
  } catch (error) {
    console.error("Error creating stream:", error);
    alert("無法啟動直播，請稍後再試");
  }
};

const stopStream = async () => {
  if (!isIdol.value || !liveId.value) {
    console.error("Only idols can stop streams or no active stream");
    return;
  }

  try {
    if (!confirm("確定要結束直播嗎？")) {
      return;
    }

    await axios.patch(
      `${apiBase}/ls/end`,
      {},
      {
        headers: {
          Authorization: `Bearer ${authStore.getToken()}`,
          "Content-Type": "application/json",
        },
      }
    );

    // console.log("Stream stopped successfully");

    cleanupResources();
    streamUrl.value = null;
    liveTitle.value = null;
    liveAccess.value = null;
    idolName.value = null;
    liveId.value = null;
    messages.value = [];
  } catch (error) {
    console.error("Error stopping stream:", error);
    alert("無法結束直播，請稍後再試");
  }
};

const fetchCurrentLive = async () => {
  try {
    const response = await axios.get(`${apiBase}/ls/check`, {
      headers: {
        Authorization: `Bearer ${authStore.getToken()}`,
      },
    });

    if (response.data && response.data.id) {
      liveId.value = response.data.id;
      streamUrl.value = "/hardcode.mp4";
      liveTitle.value = response.data.title;
      liveAccess.value = getLiveAccessText(response.data.fans_class);
      idolName.value = response.data.initiator_name || "偶像";

      setTimeout(() => {
        if (videoPlayer.value && streamUrl.value) {
          //   console.log(
          //     "Explicitly loading video for",
          //     isIdol.value ? "idol" : "viewer"
          //   );
          videoPlayer.value.src = streamUrl.value;
          videoPlayer.value.load();
          videoPlayer.value.play().catch((err) => {
            console.error("Error playing video:", err);
            // Try again with user interaction if autoplay is blocked
            if (err.name === "NotAllowedError") {
              console.log("Autoplay blocked, video needs user interaction");
            }
          });
        }
      }, 100);

      if (!isIdol.value) {
        startWatchingStream(liveId.value);
      }

      fetchComments(liveId.value);
      setupCommentPolling(liveId.value);
    } else {
      cleanupResources();
      streamUrl.value = null;
      liveTitle.value = null;
      liveAccess.value = null;
      idolName.value = null;
      liveId.value = null;
      messages.value = [];
    }
  } catch (error) {
    console.error("Error fetching current live:", error);
    cleanupResources();
    streamUrl.value = null;
    messages.value = [];
  }
};

const startWatchingStream = async (streamId) => {
  try {
    const response = await axios.post(
      `${apiBase}/watch/start`,
      {},
      {
        headers: {
          Authorization: `Bearer ${authStore.getToken()}`,
          "Content-Type": "application/json",
        },
      }
    );

    watchTimeId.value = response.data.watch_time_id;
    // Store the watch time ID in localStorage as a backup
    localStorage.setItem("activeWatchTimeId", response.data.watch_time_id);
    console.log("Started watching stream, ID:", response.data.watch_time_id);
  } catch (error) {
    console.error("Error recording watch start:", error);
  }
};

const fetchComments = async (streamId) => {
  try {
    const response = await axios.get(`${apiBase}/comment`, {
      headers: {
        Authorization: `Bearer ${authStore.getToken()}`,
      },
    });

    console.log("Fetched comments:", response.data);

    if (response.data && Array.isArray(response.data)) {
      messages.value = response.data.map((comment) => ({
        username: comment.username || "匿名用戶",
        avatarUrl: comment.user_avatar
          ? `/avatar${comment.user_avatar}.png`
          : "/default-avatar.png",
        content: comment.comment,
        tag: getFanClassTag(comment.user_class),
        user_class: comment.user_class,
      }));
    }
  } catch (error) {
    console.error("Error fetching comments:", error);
  }
};

const setupCommentPolling = (streamId) => {
  if (commentIntervalId.value) {
    clearInterval(commentIntervalId.value);
  }

  commentIntervalId.value = setInterval(() => {
    fetchComments(streamId);
  }, 5000);
};

const cleanupResources = async () => {
  // Store watchTimeId in a local variable to prevent race conditions
  const currentWatchTimeId = watchTimeId.value;

  if (commentIntervalId.value) {
    clearInterval(commentIntervalId.value);
    commentIntervalId.value = null;
  }

  // If we have a watch session active, stop it
  if (currentWatchTimeId) {
    console.log("Stopping watch session from cleanup:", currentWatchTimeId);
    try {
      const response = await axios.post(
        `${apiBase}/watch/stop`,
        {},
        {
          headers: {
            Authorization: `Bearer ${authStore.getToken()}`,
            "Content-Type": "application/json",
          },
        }
      );
      console.log(
        "Successfully stopped watch session, response:",
        response.data
      );
      // Also clear from localStorage
      localStorage.removeItem("activeWatchTimeId");
    } catch (error) {
      console.error("Error stopping watch session:", error);
    } finally {
      // Always reset the watchTimeId regardless of success/failure
      watchTimeId.value = null;
      localStorage.removeItem("activeWatchTimeId");
    }
  }
};

const sendMessage = async () => {
  if (!isAuthenticated.value) {
    alert("請先登入才能發送訊息");
    return;
  }

  if (!liveId.value) {
    alert("目前沒有進行中的直播");
    return;
  }

  if (inputMessage.value.trim() !== "") {
    const messageContent = inputMessage.value.trim();

    try {
      await axios.post(
        `${apiBase}/comment`,
        {
          comment: messageContent,
          is_question: false,
        },
        {
          headers: {
            Authorization: `Bearer ${authStore.getToken()}`,
            "Content-Type": "application/json",
          },
        }
      );

      messages.value.push({
        username: userData.value.username || "匿名用戶",
        avatarUrl: userData.value.avatarUrl
          ? `/avatar${userData.value.avatarUrl}.png`
          : "/default-avatar.png",
        content: messageContent,
        tag: getFanClassTag(userData.value.fanClass),
      });

      inputMessage.value = "";
    } catch (error) {
      console.error("Error sending comment:", error);
      alert("無法發送留言，請稍後再試");
    }
  }
};

onMounted(() => {
  getUserDataFromToken();
  fetchCurrentLive();

  if (!window.appCleanupCallbacks) {
    window.appCleanupCallbacks = [];
  }
  window.appCleanupCallbacks.push(cleanupResources);
});

onBeforeUnmount(async () => {
  console.log("Component unmounting, cleaning up resources...");
  await cleanupResources();

  if (window.appCleanupCallbacks && Array.isArray(window.appCleanupCallbacks)) {
    const index = window.appCleanupCallbacks.indexOf(cleanupResources);
    if (index !== -1) {
      window.appCleanupCallbacks.splice(index, 1);
    }
  }
});

// onBeforeRouteLeave(async (to, from, next) => {
//   console.log("Route changing, cleaning up resources...");
//   try {
//     // Make a copy of the watchTimeId to ensure it's available throughout cleanup
//     const wtId = watchTimeId.value;

//     if (wtId) {
//       console.log("Stopping watch session before route change:", wtId);
//       // Make the API call directly here to ensure it happens
//       await axios.post(
//         `${apiBase}/watch/stop`,
//         {},
//         {
//           headers: {
//             Authorization: `Bearer ${authStore.getToken()}`,
//             "Content-Type": "application/json",
//           },
//         }
//       );
//       console.log("Successfully stopped watch session before navigation");
//     }

//     // Clean up other resources
//     if (commentIntervalId.value) {
//       clearInterval(commentIntervalId.value);
//       commentIntervalId.value = null;
//     }

//     // Clear the watchTimeId last
//     watchTimeId.value = null;
//   } catch (error) {
//     console.error("Error during navigation cleanup:", error);
//   } finally {
//     // Always proceed with navigation
//     next();
//   }
// });
</script>

<style scoped>
::-webkit-scrollbar {
  width: 4px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 9999px;
}

video {
  object-fit: contain;
  /* background-color: black; */
}
</style>
