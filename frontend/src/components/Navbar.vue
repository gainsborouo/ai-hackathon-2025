<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-[#14213d] shadow-md">
    <div class="mx-auto">
      <div class="flex items-center justify-between h-24">
        <!-- Logo -->
        <div class="flex-shrink-0 self-end mb-0">
          <router-link to="/">
            <img
              src="/logo.png"
              alt="Logo"
              class="h-12 inline-block"
            />
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      isOpen: false,
    };
  },
};
</script>
