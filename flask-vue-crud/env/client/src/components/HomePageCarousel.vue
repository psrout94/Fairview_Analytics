<template>
  <v-carousel
    cycle
    height="400"
    width="1500"
    hide-delimiter-background
    show-arrows-on-hover
  >
    <v-carousel-item
      v-for="(slide, i) in slides"
      :key="i"
    >
    <v-sheet
      :color="slide.color"
      height="100%"
      tile
    >
      <v-row
        class="fill-height"
        align="center"
        justify="center"
      >
        <div class="display-3 slide-text">{{ slide.text }}</div>
      </v-row>
    </v-sheet>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      slides: [
        { text: 'Markets', src: require('@/assets/download.png'), color: 'purple darken-4' },
        { text: 'Analytics', src: require('@/assets/analytics.jpg') },
        { text: 'Real Estate', src: require('@/assets/analytics.jpg'), color: 'blue lighten-2' },
      ],
    };
  },
};
</script>

<style scoped>
.slide-text {
  color: green;
}
</style>
