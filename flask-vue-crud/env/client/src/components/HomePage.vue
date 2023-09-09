<template>
  <!-- <div id="inspire" @click.stop="setCookies">  TODO: Add This back when ready -->
  <div id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      v-if="activeUser"
    >
      <v-list light>
        <v-list-item-group v-model="item">
          <v-list-item v-for="(item, i) in nameandicons" :key="i" value="home"
          @click="redirectFunc(item.text)">
            <v-list-item-action>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      app
      color="blue darken-4"
      dark
      dense
    >
      <v-app-bar-nav-icon @click.stop="drawer=!drawer" v-if="activeUser"/>
      <v-toolbar-title>Global Analytics</v-toolbar-title>
      <v-system-bar class="stock_ticker" v-if="!stockdata">
        <v-progress-linear
          indeterminate
          color="blue darken-2"
        ></v-progress-linear>
      </v-system-bar>
      <v-system-bar class="stock_ticker" v-if="stockdata">
        <marquee-text
          :duration="45"
          :paused="paused">
          &nbsp;
          <span v-for="(item, index) in lowstockdata" :key="index" class="span_negative">
            {{ item.ticker }}:
            <span class="badge badge-danger ml-2">
              {{ item.value }} </span>
          </span>
          <span v-for="item in highstockdata" :key="item.ticker" class="span_positive">
            {{ item.ticker }}:
            <span class="badge badge-success ml-2" >
              {{ item.value }} </span>
          </span>
        </marquee-text>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn @click="refreshStocks" v-on="on" small icon fab>
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </template>
          <span>Refresh Stock Data</span>
        </v-tooltip>
        <v-tooltip bottom v-if="activeUser">
          <template v-slot:activator="{ on }">
            <v-btn @click="openStockDialog" v-on="on" small icon fab>
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>Select Stocks</span>
        </v-tooltip>
      </v-system-bar>
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
    <v-img class="carousel_items" src="@/assets/analytics.jpg" aspect-ratio="1.7"></v-img>
    <v-card class="returning_user" v-if="returninguser" height=auto width=25%>
      <v-card-title>Sign-In</v-card-title>
      <v-spacer></v-spacer>
      <v-text-field v-model="username" label="Enter Username"
      clearable dense></v-text-field>
      <v-text-field v-model="userpassword" label="Enter Password" dense
      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
      :type="show ? 'text' : 'password'"
      @click:append="show = !show">
      </v-text-field>
      <v-card-actions>
        <v-btn text color="red" @click="cancelUserSignIn">Cancel</v-btn>
        <v-spacer></v-spacer>
        <v-btn text color="info" @click="signInUser">Sign-in</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="new_user" v-if="newuser" height=auto width=75%>
      <v-form refs="card" v-model="valid">
        <v-card-title>Create New User</v-card-title>
        <v-spacer></v-spacer>
        <v-text-field v-model="userfullname" label="Enter Your Full Name"
        clearable dense outlined :rules="[passwordrules.required]"></v-text-field>
        <v-text-field v-model="username" label="Enter Username"
        clearable dense outlined :rules="[passwordrules.required]"></v-text-field>
        <v-text-field v-model="userpassword" label="Enter Password"
        dense outlined
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[passwordrules.required, passwordrules.min]"
        :type="show1 ? 'text' : 'password'"
        @click:append="show1 = !show1">
        </v-text-field>
        <v-text-field v-model="useremail" label="Enter Email"
        clearable dense outlined :rules="emailRules"></v-text-field>
        <v-text-field v-model="stocktext" label="stock symbol" outlined
        clearable @keyup.13="addStock" :append-icon="'mdi-plus'" @click:append="addStock"
        dense></v-text-field>
        <v-card-text>
          <v-chip v-for="(item, index) in tempstockarray" :key="index" close small
          @click:close="stockChipClose(index)">
            {{ item }}
          </v-chip>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="red" @click="cancelUserCreation">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn text color="info" :disabled="!valid" @click="saveUserCreation">Sign-Up</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
    <v-card class="select_stocks" v-if="userstocks" height=auto width=25%>
      <v-card-title>Select Stocks</v-card-title>
      <v-spacer></v-spacer>
      <v-text-field v-model="stocktext" label="stock symbol"
      clearable @keyup.13="addStock" dense
      :append-icon="'mdi-plus'" @click:append="addStock">
      </v-text-field>
      <v-card-text>
        <v-chip v-for="(item, index) in tempstockarray" :key="index" close small
        @click:close="stockChipClose(index)">
           {{ item }}
        </v-chip>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="red" @click="cancelChosenStocks">Cancel</v-btn>
        <v-spacer></v-spacer>
        <v-btn text color="info" @click="saveChosenStocks">Save</v-btn>
      </v-card-actions>
    </v-card>
    <div class="news_ticker" v-if="shownews">
      <v-toolbar
        dense
        dark
        color="blue darken-4"
      >
        <v-toolbar-title>News Feed</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-text-field v-model="searchterm" label="keywords" clearable @keyup.13="querySearch"
            dense single-line height=30>
          </v-text-field>
          <v-btn @click="querySearch" small icon fab depressed>
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <div class="scroll">
        <v-expansion-panels>
          <v-expansion-panel v-for="(item, i) in newsarticles" :key="i">
            <v-expansion-panel-header> {{ item.title }} </v-expansion-panel-header>
            <v-expansion-panel-content> Author: <strong> {{ item.author }} </strong>,
              Source: <strong> {{ item.source.name }} </strong>, <br>
              <v-btn :href='item.url' target="_blank" depressed text color="blue">
                Link To Resource</v-btn>
              <br>
              {{ item.publishedAt }}
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </div>
    <Carousel class="feature_carousel" v-if="!activeUser && !newuser"/>
    <v-footer
      color="blue darken-4"
      app
      dark
    >
      <span class="white--text">&copy; Global Analytics 2020</span>
    </v-footer>
    <Snackbar v-if="showsnackbar" :message="snackbarmessage" :color="snackbarcolor"></Snackbar>
  </div>
</template>

<script>
// import store from '../store';
// import { EventBus } from '../event-bus';
import Carousel from '@/components/HomePageCarousel.vue';
import RepositoryFactory from '../repositories/RepositoryFactory';

const PostsRepository = RepositoryFactory.get('posts');
export default {
  components: {
    Carousel,
  },
  props: {
    source: String,
  },
  data: () => ({
    item: 1,
    drawer: false,
    newTimeObject: {},
    nameandicons: [{ text: 'Alpha', icon: 'mdi-alpha' }, { text: 'Agriculture', icon: 'mdi-flower' }, { text: 'Economic', icon: 'mdi-chart-line' }, { text: 'SEC', icon: 'mdi-security' }, { text: 'Federal Reserve', icon: 'mdi-cash' }],
    stockdata: false,
    newsarticles: [],
    searchterm: '',
    highstockdata: [],
    lowstockdata: [],
    closestockdata: [],
    openstockdata: [],
    showsnackbar: false,
    chartTitle: '',
    chartData: [['Date', 'High', 'Low']],
    showchart: false,
    userstocks: false,
    stocktext: '',
    stocklist: [],
    stockliststring: '',
    paused: false,
    tempstockarray: [],
    newuser: false,
    returninguser: false,
    username: '',
    userpassword: '',
    useremail: '',
    userfullname: '',
    loginoptions: ['Sign-In', 'Create Account'],
    snackbarmessage: '',
    snackbarcolor: 'blue',
    usernamestring: '',
    activeUser: false,
    shownews: false,
    show: false,
    show1: false,
    valid: true,
    passwordrules: {
      required: (value) => !!value || 'Required.',
      min: (v) => v.length >= 8 || 'Min 8 characters',
    },
    emailRules: [
      (v) => !!v || 'E-mail is required',
      (v) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
  }),
  methods: {
    redirectFunc(arg) {
      if (arg === 'Alpha') {
        this.$router.push('/alpha');
      } else if (arg === 'Agriculture') {
        this.$router.push('/agriculture');
      } else if (arg === 'Economic') {
        this.$router.push('/economic');
      } else if (arg === 'SEC') {
        this.$router.push('/sec');
      } else if (arg === 'Federal Reserve') {
        this.$router.push('/fred');
      }
    },
    async getYahooData() {
      const { data } = await PostsRepository.getYahoo();
      this.MassageResponse(data);
    },
    MassageResponse(data) {
      if (data === 'Error') {
        this.manageSnackbar('Error Retrieving Stock Data', 'red');
        return;
      }
      const startingObject = data;
      // Checking the length allows for during market, and after market results to still be correct
      let indices = 0;
      const keylength = startingObject.data[0].length;
      if (startingObject.data.length > 3) {
        indices = 2;
      } else {
        indices = 1;
      }
      for (let key = 0; key < keylength / 2; key += 1) {
        let values = startingObject.data[0][key];
        const ret = startingObject.columns[key][1];
        values = Math.round(values * 100) / 100;
        this.closestockdata.push({ ticker: ret, value: values });
      }
      for (let newkey = keylength / 2; newkey < keylength; newkey += 1) {
        let newvalues = startingObject.data[indices][newkey];
        const rets = startingObject.columns[newkey][1];
        newvalues = Math.round(newvalues * 100) / 100;
        this.openstockdata.push({ ticker: rets, value: newvalues });
      }
      for (let i = 0; i < this.openstockdata.length; i += 1) {
        if (this.openstockdata[i].value > this.closestockdata[i].value) {
          this.lowstockdata.push(this.closestockdata[i]);
        } else {
          this.highstockdata.push(this.closestockdata[i]);
        }
      }
      this.stockdata = true;
      if (this.highstockdata.length + this.lowstockdata.length < 8) {
        this.paused = true;
      } else {
        this.paused = false;
      }
    },
    async getNews() {
      const payload = {
        method: 'top-headlines',
        country: 'us',
      };

      const { data } = await PostsRepository.postNews(payload);
      this.newsarticles = data.articles;
      this.shownews = true;
    },
    async querySearch() {
      this.newsarticles = [];
      if (this.searchterm !== '') {
        const payload = {
          method: 'everything',
          country: 'us',
          keyword: this.searchterm,
        };

        const { data } = await PostsRepository.postNews(payload);
        this.newsarticles = data.articles;
      } else {
        this.getNews();
      }
    },
    addStock() {
      this.tempstockarray.push(this.stocktext);
      this.stocktext = '';
      this.stockliststring = this.tempstockarray.toString();
    },
    refreshStocks() {
      this.closestockdata = [];
      this.highstockdata = [];
      this.openstockdata = [];
      this.lowstockdata = [];
      this.stockdata = false;
      if (this.stocklist.length > 0) {
        this.tempstockarray = this.stocklist;
        // var str = "How are you doing today?";
        this.tempstockarray = this.stockliststring.split(',');
        this.saveChosenStocks();
      } else {
        this.getYahooData();
      }
    },
    async saveChosenStocks() {
      this.stocklist = this.tempstockarray;
      this.stockliststring = this.stocklist.toString();
      this.userstocks = false;
      this.shownews = true;
      const payload = {
        username: this.usernamestring,
        stocklist: this.stockliststring,
      };
      const { data } = await PostsRepository.postYahoo(payload);
      this.highstockdata = [];
      this.closestockdata = [];
      this.lowstockdata = [];
      this.openstockdata = [];
      this.tempstockarray = [];
      this.MassageResponse(data);
      if (this.highstockdata.length + this.lowstockdata.length < 9) {
        this.paused = true;
      } else {
        this.paused = false;
      }
    },
    cancelChosenStocks() {
      this.userstocks = !this.userstocks;
      this.shownews = true;
      this.stocktext = '';
      this.tempstockarray = [];
      this.stockliststring = this.stocklist.toString();
    },
    stockChipClose(index) {
      this.tempstockarray.splice(index, 1);
      this.stockliststring = this.tempstockarray.toString();
    },
    openStockDialog() {
      this.userstocks = !this.userstocks;
      this.shownews = false;
      // eslint-disable-next-line
      const length = this.stocklist.length;
      let x = 0;
      if (this.tempstockarray.length !== this.stocklist.length) {
        for (x; x < length; x += 1) {
          this.tempstockarray.push(this.stocklist[x]);
        }
      }
    },
    async getUserStocks() {
      const { data } = await PostsRepository.getStockDbData();
      // eslint-disable-next-line
      this.stockliststring = data[1];
      this.tempstockarray = this.stockliststring.split(' ');
      if (this.tempstockarray.length > 0) {
        this.saveChosenStocks();
      } else {
        this.getYahooData();
      }
      this.userstocks = false;
      this.shownews = true;
    },
    openUserDialog() {
      this.newuser = !this.newuser;
      this.shownews = !this.shownews;
    },
    openSignInDialog() {
      this.returninguser = !this.returninguser;
      this.shownews = false;
    },
    cancelUserCreation() {
      this.userfullname = '';
      this.useremail = '';
      this.username = '';
      this.userpassword = '';
      this.stocktext = '';
      this.tempstockarray = [];
      this.stockliststring = this.stocklist.toString();
      this.newuser = !this.newuser;
      this.shownews = !this.shownews;
    },
    cancelUserSignIn() {
      this.returninguser = !this.returninguser;
      this.shownews = true;
    },
    async signInUser() {
      const payload = {
        username: this.username,
        password: this.userpassword,
      };
      const { data } = await PostsRepository.signInNewUser(payload);
      if (data !== 'Bad Password' && data !== 'Bad Username') {
        this.signin(data);
        this.manageSnackbar('User Sign-in Successful!', 'blue');
      } else {
        this.manageSnackbar(data, 'red');
        if (this.highstockdata.length === 0 && this.lowstockdata.length === 0) {
          this.getYahooData();
        }
      }
      this.returninguser = false;
      this.shownews = true;
      this.username = '';
      this.userpassword = '';
    },
    async saveUserCreation() {
      const payload = {
        fullname: this.userfullname,
        username: this.username,
        password: this.userpassword,
        email: this.useremail,
        stocks: this.tempstockarray,
      };
      const { data } = await PostsRepository.createNewUser(payload);
      if (data !== 'Email is already registered' && data !== 'Username is already registered') {
        this.signin(data);
        this.setCookies();
        this.manageSnackbar('User Creation Successful!', 'blue');
      } else {
        this.manageSnackbar(data, 'red');
      }
      this.newuser = false;
      this.username = '';
      this.userpassword = '';
      this.useremail = '';
      this.userfullname = '';
    },
    signin(data) {
      this.tempstockarray = data.split(' ');
      if (this.tempstockarray.length > 0) {
        this.saveChosenStocks();
      } else {
        this.getYahooData();
      }
      this.setCookies();
      this.usernamestring = this.username;
      this.activeUser = true;
      this.loginoptions = ['Account', 'Logout'];
    },
    logout() {
      this.tempstockarray = [];
      this.stocklist = [];
      this.stockliststring = '';
      this.usernamestring = '';
      this.closestockdata = [];
      this.highstockdata = [];
      this.openstockdata = [];
      this.lowstockdata = [];
      this.stockdata = false;
      this.getYahooData();
      this.loginoptions = ['Sign-In', 'Create Account'];
      this.activeUser = false;
      document.cookie = 'username=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'; // Deleting the cookies
      document.cookie = 'password=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
      this.manageSnackbar('Successfully Logged Out!', 'blue');
    },
    loginOptions(item) {
      if (item === 'Create Account') {
        this.openUserDialog();
      } else if (item === 'Logout') {
        this.logout();
      } else if (item === 'Account') {
        this.$router.push('/account');
      } else {
        this.openSignInDialog();
      }
    },
    setCookies() {
      if (this.usernamestring !== '' || this.username !== '') {
        const now = new Date();
        const time = now.getTime();
        const expireTime = time + 3600000; // The cookie lasts for an hour
        now.setTime(expireTime);
        document.cookie = `username =  ${this.username}; expires = ${now.toGMTString()}; samesite=lax`;
        document.cookie = `password = ${this.userpassword}; expires = ${now.toGMTString()}; samesite=lax`;
      }
      /* const payload = {
        username: this.username,
        password: this.userpassword,
      };
      const { cookie } = await PostsRepository.setCookie(payload);
      console.log(cookie); */
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
          this.username = cookieValue;
        } else if (cookieKey === 'password') {
          this.userpassword = cookieValue;
        }
      }
    },
    async cookieSignIn() {
      const payload = {
        username: this.username,
        password: this.userpassword,
      };
      const { data } = await PostsRepository.signInNewUser(payload);
      if (data !== 'Bad Password' && data !== 'Bad Username') {
        this.signin(data);
      } else {
        this.manageSnackbar(data, 'red');
        if (this.highstockdata.length === 0 && this.lowstockdata.length === 0) {
          this.getYahooData();
        }
      }
      this.returninguser = false;
      this.shownews = true;
      this.username = '';
      this.userpassword = '';
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
  },
  mounted() {
    this.getNews();
    if (document.cookie !== '') { // If there's a coookie, retrieve the sign-in data, otherwise just get the general DJIA data
      this.retrieveCookies();
      this.cookieSignIn();
    } else {
      this.getYahooData();
    }
  },
};
</script>

<style scoped>
.returning_user {
  position: fixed !important;
  top: 25% !important;
  left: 83% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  z-index: 100 !important;
}
.new_user {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  z-index: 100 !important;
}

.stock_ticker {
  width: 60% !important;
  margin: 0 auto;
}

.news_ticker {
  position: fixed !important;
  top: 50% !important;
  left: 83% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  width: 30% !important;
  height: 60% !important;
  z-index: 100 !important;
}

.feature_carousel {
  position: fixed !important;
  top: 47% !important;
  left: 17% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  width: 30% !important;
  /* height: 60% !important; */
  z-index: 100 !important;
}

.scroll {
  height: 80% !important;
  overflow-y: scroll !important;
}

.span_negative {
  padding: 2px;
}

.span_positive {
  padding: 2px;
}

.carousel_items {
  width: 100%;
  height: 100% !important;
  overflow: none;
}

.select_stocks {
  position: fixed !important;
  top: 30% !important;
  left: 83% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  z-index: 100 !important;
}

#inspire {
  height: 100%;
  overflow: none;
}
</style>
