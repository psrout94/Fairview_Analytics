<template>
  <div class="container">
    <v-app-bar
      app
      color="blue darken-4"
      dark
      dense
      >
      <v-toolbar-title>Global Analytics -- Fred</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn @click="CallAlpha" color="blue darken-4">
        Alpha
      </v-btn>
      <v-btn @click="CallEconomic" color="blue darken-4">
        Economic
      </v-btn>
      <v-btn @click="dummy('Weather')" color="blue darken-4">
        Weather
      </v-btn>
      <v-btn @click="CallAgriculture" color="blue darken-4">
        Agriculture
      </v-btn>
      <v-btn @click="CallSec" color="blue darken-4">
        SEC
      </v-btn>
      <v-btn @click="home" color="blue darken-4">
        Home
      </v-btn>
      {{ usernamestring }}
      <template>
        <v-menu offset-y>
          <template v-slot:activator="{ on }">
            <v-btn small icon fab
              :items="loginoptions"
              v-on="on">
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(item, index) in loginoptions"
              :key="index"
              @click="loginOptions(item)"
            >
              <v-list-item-title>{{ item }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
    <br><br>
    <template>
      <v-select
        v-if="freddata.length < 2"
        v-model="selectindex"
        :items="domesticoptions"
        label="Select an Economic Measure"
        chips
        clearable
      ></v-select>
      <v-btn color="green" @click="getFred" v-if="freddata.length < 2">Fred Data</v-btn>
      <v-btn color="info" v-if="freddata.length > 1" @click="chartFred">Chart Fred</v-btn>
      <v-btn color="warning" v-if="freddata.length > 1" @click="saveFred">Export Fred</v-btn>
      <v-btn color="error" v-if="freddata.length > 1" @click="clearFred">Clear</v-btn>
      <v-text-field v-if="freddata.length > 1"
        v-model="search"
        append-icon="mdi-magnify"
        label="Search Data"
        single-line
        hide-details
      ></v-text-field>
      <v-data-table
        v-if="freddata.length > 1"
        :headers="headers"
        :items="freddata"
        :search="search"
      >
      </v-data-table>
      <v-card class="save_file" v-if="savefile" height=auto width=25%>
        <v-form v-model="valid">
          <v-card-title>Download Data</v-card-title>
          <v-spacer></v-spacer>
          <v-text-field v-model="filename" label="File Name" clearable dense
          :rules="[exportrules.required]"></v-text-field>
          <v-card-actions>
            <v-btn text color="red" @click="cancelSaveFile">Cancel</v-btn>
            <v-spacer></v-spacer>
            <v-btn text color="info" @click="saveFile" :disabled="!valid">Save</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
    <template>
      <GoogleChart v-if="showchart" :title="chartTitle"
      :chartData="chartData"></GoogleChart>
    </template>
    <Snackbar :message="snackbarmessage" :color="snackbarcolor" :value="showsnackbar"
    v-if="showsnackbar"></Snackbar>
  </div>
</template>

<script>
import RepositoryFactory from '../repositories/RepositoryFactory';

const PostsRepository = RepositoryFactory.get('posts');
export default {
  data: () => ({
    freddata: [],
    headers: [{ text: 'Date', value: 'date' }],
    showchart: false,
    chartTitle: '',
    chartData: [['Date', 'GNPC']],
    selectindex: '',
    search: '',
    savefile: false,
    snackbarmessage: '',
    snackbarcolor: '',
    showsnackbar: false,
    filename: '',
    loginoptions: ['logout'],
    valid: true,
    usernamestring: '',
    exportrules: {
      required: (value) => !!value || 'Required.',
    },
    domesticoptions: ['GDP', 'GNPCA', 'UNRATE', 'DGS10', 'PAYEMS', 'CPIAUCSL', 'ICSA', 'INDPRO', 'WALCL', 'FEDFUNDS', 'MORTGAGE30US', 'GFDEGDQ188S', 'T10YIE', 'CSUSHPINSA'],
  }),
  methods: {
    CallAgriculture() {
      this.$router.push('/agriculture');
    },
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
    CallSec() {
      this.$router.push('/sec');
    },
    dummy(arg) {
      // eslint-disable-next-line
      console.log(arg);
    },
    saveFred() {
      this.savefile = true;
    },
    clearFred() {
      this.freddata = [];
      this.selectindex = '';
      this.headers.pop();
    },
    cancelSaveFile() {
      this.savefile = false;
      this.filename = '';
    },
    async saveFile() {
      const data = {
        filename: this.filename,
        data: this.freddata,
      };
      const fileValue = await PostsRepository.exportData(data);
      this.snackbarmessage = fileValue.data;
      if (this.snackbarmessage === 'Download Failed') {
        this.snackbarcolor = 'red';
        this.showsnackbar = true;
      } else if (this.snackbarmessage === 'Successfully Downloaded!') {
        this.snackbarcolor = 'blue';
        this.showsnackbar = true;
      }
      window.setTimeout(this.markFalse, 5000);
      this.savefile = false;
      this.filename = '';
    },
    markFalse() {
      this.showsnackbar = false;
    },
    async getFred() {
      this.headers.push({ text: this.selectindex, value: 'value' });
      const value = {
        data: this.selectindex,
      };
      const { data } = await PostsRepository.getFred(value);
      for (let i = 0; i < data.observations.length; i += 1) {
        if (data.observations[i].value !== '.') {
          this.freddata.push(data.observations[i]);
        }
      }
    },
    chartFred() {
      this.chartTitle = this.selectindex;
      this.chartData = [['Date', this.selectindex]];
      for (let x = 0; x < this.freddata.length; x += 1) {
        if (this.freddata.length > 100 && x % 10 === 0) {
          this.chartData.push([this.freddata[x].date,
            Number(this.freddata[x].value)]); // Cast the string value to a number
        } else if (this.freddata.length < 100) {
          this.chartData.push([this.freddata[x].date,
            Number(this.freddata[x].value)]); // Cast the string value to a number
        } else if (x === this.freddata.length - 1) {
          this.chartData.push([this.freddata[x].date,
            Number(this.freddata[x].value)]); // Cast the string value to a number
        }
      }
      console.log(this.freddata);
      this.showchart = true;
    },
    clearChart() {
      this.chartData = [['Date', 'GNPC']];
      this.chartFred();
    },
    retrieveCookies() {
      let cookieKey = '';
      let cookieValue = '';
      let x = 0;
      const decodedCookie = decodeURIComponent(document.cookie);
      const cookies = decodedCookie.split(';');
      for (x; x < cookies.length; x += 1) {
        const subcookies = cookies[x].split('=');
        [cookieKey, cookieValue] = subcookies;
        cookieKey = cookieKey.trim();
        cookieValue = cookieValue.trim();
        if (cookieKey === 'username') {
          this.usernamestring = cookieValue;
        }
      }
    },
    loginOptions() {
      this.usernamestring = '';
      document.cookie = 'username=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'; // Deleting the cookies
      document.cookie = 'password=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
    },
  },
  mounted() {
    if (document.cookie !== '') { // If there's a coookie, retrieve the sign-in data, otherwise just get the general DJIA data
      this.retrieveCookies();
    }
  },
};
</script>

<style scoped>
.save_file {
  position: fixed !important;
  top: 30% !important;
  left: 83% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  z-index: 100 !important;
}
</style>
