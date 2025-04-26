<template>
  <div id="app" class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-grow pt-24">
      <router-view />
    </main>
    <!-- <Footer /> -->
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
// import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    Navbar,
    // Footer,
  },
};
</script>

<style></style>
