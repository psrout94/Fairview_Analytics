<template>
  <div class="container">
    <v-app-bar
      app
      color="blue darken-4"
      dark
      dense
      >
      <v-toolbar-title>Global Analytics -- Agriculture</v-toolbar-title>
      <v-spacer></v-spacer>
<!-- <v-toolbar-title v-if="stockname"> Current Commodity: {{ stockname }}</v-toolbar-title> -->
     <!-- <template>
        <v-menu offset-y v-if="stockname">
          <template v-slot:activator="{ on }">
            <v-btn small icon fab
              :items="menuoptions"
              v-if="stockname"
              v-on="on">
              <v-icon>mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(item, index) in menuoptions"
              :key="index"
              @click="dummy(item)"
            >
              <v-list-item-title>{{ item }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <v-btn v-if="stockname" @click="cleardata" small icon fab>
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-spacer></v-spacer> -->
      <v-btn @click="CallAlpha" color="blue darken-4">
        Alpha
      </v-btn>
      <v-btn @click="CallEconomic" color="blue darken-4">
        Economic
      </v-btn>
      <v-btn @click="dummy('Weather')" color="blue darken-4">
        Weather
      </v-btn>
      <v-btn @click="home" color="blue darken-4">
        Home
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  data: () => ({
  }),
  methods: {
    CallAlpha() {
      // this.$store.commit('ShowAlpha', true);
      this.$router.push('/alpha');
    },
    CallEconomic() {
      this.$router.push('/economic');
    },
    home() {
      this.$router.push('/');
    },
    dummy(arg) {
      // eslint-disable-next-line
      console.log(arg);
    },
  },
};
</script>
