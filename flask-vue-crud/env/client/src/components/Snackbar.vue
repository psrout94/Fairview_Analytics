<template>
  <v-snackbar
    v-model="showsnackbar"
    :timeout="timeout"
    :color="color">
    {{ message }}
    <v-btn
      text
      @click="showsnackbar = false"
    >
      Close
    </v-btn>
  </v-snackbar>
</template>

<script>
export default {
  props: {
    message: String,
    color: String,
    show: Boolean,
  },
  data() {
    return {
      showsnackbar: true,
      timeout: 3000,
    };
  },
};
</script>
