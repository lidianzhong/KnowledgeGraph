<template>
  <div>
    <top-bar class="topbar"></top-bar>
    <index></index>
  </div>
</template>
<script>
import TopBar from "components/TopBar.vue";
import Index from "views/Index.vue";

export default {
  name: "Main",
  components: {
    TopBar,
    Index,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}
</style>
