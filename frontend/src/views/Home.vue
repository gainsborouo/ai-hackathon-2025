<template>
  <div class="p-8 tracking-widest">
    <Sidebar v-model:isOpen="sidebarOpen" />

    <div class="flex justify-center">
      <div class="flex flex-col gap-6 w-full max-w-2xl">
        <template v-for="(post, index) in posts" :key="index">
          <div class="p-6 border-2 border-[#0E1A37] rounded-2xl">
            <div class="flex items-center gap-2 mb-4">
              <img
                :src="post.avatarUrl"
                alt="Avatar"
                class="rounded-full w-10 h-10"
              />
              <div class="font-bold text-[#0E1A37] flex items-center">
                {{ post.username }}
                <span
                  v-if="post.isSuperFan"
                  class="bg-orange-400 text-white text-xs ml-2 px-2 py-0.5 rounded-full inline-flex items-center"
                  >超級粉絲限定</span
                >
              </div>
            </div>

            <div class="mb-4 text-[#0E1A37]">
              {{ post.content }}
            </div>

            <div
              v-if="post.pollOptions && post.pollOptions.length > 0"
              class="flex flex-col gap-2 mb-4"
            >
              <div
                v-for="(option, idx) in post.pollOptions"
                :key="idx"
                :class="[
                  'px-4 py-2 rounded-full cursor-pointer',
                  option.selected
                    ? 'bg-[#0E1A37] text-[#f4f4f4]'
                    : 'border hover:bg-gray-100',
                ]"
                @click="toggleOption(post.id, idx)"
              >
                {{ option.selected ? "⭐" : "⭘" }} {{ option.text }}
              </div>
            </div>

            <div class="flex items-center gap-4 text-sm text-gray-500">
              <div
                class="flex items-center gap-1 cursor-pointer hover:text-blue-700"
                @click="toggleLike(post.id)"
              >
                <i
                  :class="[
                    'fas',
                    post.isLiked
                      ? 'fa-thumbs-up text-blue-700'
                      : 'fa-thumbs-up',
                  ]"
                ></i>
                <span>{{ post.likes }}</span>
              </div>
              <div
                class="flex items-center gap-1 cursor-pointer hover:text-gray-700"
              >
                <i class="fas fa-comment"></i>
                <span>{{ post.comments }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Sidebar from "../components/Sidebar.vue";

const sidebarOpen = ref(false);

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const posts = ref([]);

const fetchPosts = async () => {
  // const response = await fetch('/api/posts');
  // posts.value = await response.json();

  posts.value = [
    {
      id: 1,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "各位救火隊下個禮拜想看什麼呢～😎",
      isSuperFan: true,
      pollOptions: [
        { text: "vlog", selected: false },
        { text: "採訪", selected: false },
        { text: "心電感應", selected: false },
      ],
      likes: 300,
      comments: 17,
      isLiked: true,
    },
    {
      id: 2,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "下禮拜新歌上線！敬請期待～～",
      isSuperFan: false,
      pollOptions: [],
      likes: 214,
      comments: 42,
      isLiked: false,
    },
    {
      id: 3,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "今天練團好順！有預感演唱會會超炸🔥🔥",
      isSuperFan: true,
      pollOptions: [],
      likes: 489,
      comments: 58,
      isLiked: false,
    },
    {
      id: 4,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "偷偷透露～週邊商品設計中，想要什麼款式呢？",
      isSuperFan: true,
      pollOptions: [
        { text: "帽子", selected: false },
        { text: "T恤", selected: false },
        { text: "手環", selected: false },
      ],
      likes: 377,
      comments: 29,
      isLiked: false,
    },
    {
      id: 5,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "晚安～明天也要一起加油喔💪💤",
      isSuperFan: false,
      pollOptions: [],
      likes: 152,
      comments: 12,
      isLiked: true,
    },
    {
      id: 6,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "假日來個小互動～大家最愛的FEniX歌曲是哪一首？🎶",
      isSuperFan: false,
      pollOptions: [
        { text: "逆風飛翔", selected: false },
        { text: "星火燎原", selected: false },
        { text: "無盡旅程", selected: false },
      ],
      likes: 412,
      comments: 58,
      isLiked: true,
    },
    {
      id: 7,
      username: "FEniX",
      avatarUrl: "/avatar2.png",
      content: "偷偷預告一下，下個月有特別活動喔😉",
      isSuperFan: true,
      pollOptions: [],
      likes: 289,
      comments: 31,
      isLiked: false,
    },
  ];
};

const toggleOption = (postId, optionIdx) => {
  const post = posts.value.find((p) => p.id === postId);
  if (post && post.pollOptions) {
    const option = post.pollOptions[optionIdx];
    if (option.selected) {
      option.selected = false;
    } else {
      post.pollOptions.forEach((opt) => {
        opt.selected = false;
      });
      option.selected = true;
    }
  }
};

const toggleLike = (postId) => {
  const post = posts.value.find((p) => p.id === postId);
  if (post) {
    if (post.isLiked) {
      post.likes--;
      post.isLiked = false;
    } else {
      post.likes++;
      post.isLiked = true;
    }
  }
};

onMounted(() => {
  fetchPosts();
});
</script>

<style scoped></style>
