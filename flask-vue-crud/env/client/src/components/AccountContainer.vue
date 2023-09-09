<template>
  <div class="container">
    <v-app-bar
      app
      color="blue darken-4"
      dark
      dense
      >
      <v-toolbar-title>Global Analytics -- Account Info for {{ usernamestring }}</v-toolbar-title>
      <v-spacer></v-spacer>
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
    <v-card
      class="acct_info"
      width=80%
    >
      <v-card-title>Account Info</v-card-title>
      <v-card-text>
        <v-text-field v-model="fullname" label="Your Name" dense :readonly="fullnameReadOnly"
        :append-icon="'mdi-pencil'" @click:append="changeFullName" ref="full"></v-text-field>
        <v-text-field v-model="username" label="Your Username" dense readonly></v-text-field>
        <v-text-field v-model="userstocks" label="Your Stocks" dense :readonly="stocksReadOnly"
        :append-icon="'mdi-pencil'" @click:append="changeStockList" ref="stocks"></v-text-field>
        <v-text-field v-model="useremail" label="Your Email" dense readonly></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="deep-purple accent-4" @click="changePassword">
          Change Password
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn text color="indigo darken-4" v-if="tempstocks.length!=userstocks.length"
        @click="commitChanges">
          Submit Changes
        </v-btn>
        <v-btn text color="indigo darken-4" v-if="tempname.length!=fullname.length"
        @click="commitChanges">
          Submit Changes
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="acct_info" v-if="showpassworddialog" height=auto width=25%>
      <v-form refs="card" v-model="valid">
        <v-card-title>Change Password</v-card-title>
        <v-spacer></v-spacer>
        <v-text-field v-model="oldpassword" label="Enter Current Password"
        dense outlined :rules="[passwordrules.required, passwordrules.min]"
        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show ? 'text' : 'password'"
        @click:append="show = !show"></v-text-field>
        <v-text-field v-model="newpassword" label="Enter New Password"
        dense outlined
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[passwordrules.required, passwordrules.min]"
        :type="show1 ? 'text' : 'password'"
        @click:append="show1 = !show1">
        </v-text-field>
        <v-card-actions>
          <v-btn text color="red" @click="cancelPasswordChange">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn text color="info" :disabled="!valid" @click="submitPasswordChange">Submit</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
    <Snackbar v-if="showsnackbar" :message="snackbarmessage" :color="snackbarcolor"></Snackbar>
  </div>
</template>

<script>
import RepositoryFactory from '../repositories/RepositoryFactory';

const PostsRepository = RepositoryFactory.get('posts');
export default {
  data: () => ({
    loginoptions: ['logout'],
    valid: true,
    usernamestring: '',
    showsnackbar: false,
    fullname: '',
    username: '',
    useremail: '',
    userstocks: '',
    oldpassword: '',
    newpassword: '',
    tempstocks: '',
    tempname: '',
    snackbarcolor: 'blue',
    snackbarmessage: '',
    fullnameReadOnly: true,
    stocksReadOnly: true,
    show: false,
    show1: false,
    showpassworddialog: false,
    passwordrules: {
      required: (value) => !!value || 'Required.',
      min: (v) => v.length >= 8 || 'Min 8 characters',
    },
  }),
  methods: {
    home() {
      this.$router.push('/');
    },
    async getAccountInfo() {
      const payload = {
        username: this.usernamestring,
      };
      const { data } = await PostsRepository.getAccountData(payload);
      const stringData = data.replace(/['"]+/g, '');
      const arrayData = stringData.split(',');
      [, this.fullname, this.username, , this.useremail, this.userstocks] = arrayData;
      this.userstocks = this.userstocks.replace(/[[\]']+/g, '');
      this.tempstocks = this.userstocks;
      this.tempname = this.fullname;
    },
    changeFullName() {
      this.fullnameReadOnly = !this.fullnameReadOnly;
      if (this.fullnameReadOnly === false) {
        this.$nextTick(this.$refs.full.focus); // Give the text box focus when active
      }
    },
    changeStockList() {
      this.stocksReadOnly = !this.stocksReadOnly;
      if (this.stocksReadOnly === false) {
        this.$nextTick(this.$refs.stocks.focus); // Give the text box focus when active
      }
    },
    async commitChanges() {
      if (this.userstocks !== this.tempstocks) {
        const payload = {
          username: this.username,
          stocklist: this.userstocks,
        };
        const { data } = await PostsRepository.changeStocks(payload);
        if (data === 'Success!') {
          this.manageSnackbar('Successfully changed stocks!', 'blue');
          this.tempstocks = this.userstocks;
          this.changeStockList();
        } else {
          this.manageSnackbar('There was an error changing stocks', 'red');
        }
      }
    },
    changePassword() {
      this.showpassworddialog = true;
    },
    cancelPasswordChange() {
      this.newpassword = '';
      this.oldpassword = '';
      this.showpassworddialog = false;
    },
    async submitPasswordChange() {
      const payload = {
        username: this.username,
        old: this.oldpassword,
        new: this.newpassword,
      };

      const { data } = await PostsRepository.changeUserPassword(payload);

      if (data === 'Bad Password') {
        this.manageSnackbar('Error Changing Password', 'red');
        this.oldpassword = '';
        this.newpassword = '';
      } else {
        this.manageSnackbar('Password Changed Successfully!', 'blue');
        this.setCookies();
        this.oldpassword = '';
        this.newpassword = '';
        this.showpassworddialog = false;
      }
    },
    manageSnackbar(message, color) {
      this.snackbarmessage = message;
      this.snackbarcolor = color;
      this.showsnackbar = true;
      window.setTimeout(this.markFalse, 5000);
    },
    markFalse() {
      this.showsnackbar = false;
    },
    setCookies() {
      const now = new Date();
      const time = now.getTime();
      const expireTime = time + 3600000; // The cookie lasts for an hour
      now.setTime(expireTime);
      document.cookie = `username =  ${this.username}; expires = ${now.toGMTString()}; samesite=lax`;
      document.cookie = `password = ${this.newpassword}; expires = ${now.toGMTString()}; samesite=lax`;
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
      this.getAccountInfo();
    }
  },
};
</script>

<style scoped>
.acct_info {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  z-index: 100 !important;
}
</style>
