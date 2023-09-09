<template>
  <div class="container">
    <v-app-bar
      app
      color="blue darken-4"
      dark
      dense
      >
      <v-toolbar-title>Global Analytics -- AlphaVantage</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title v-if="stockname"> Current Commodity: {{ stockname }}</v-toolbar-title>
      <template>
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
      <v-spacer></v-spacer>
      <v-btn @click="CallSEC" color="blue darken-4">
        Sec
      </v-btn>
      <v-btn @click="CallAgriculture" color="blue darken-4">
        Agricultural
      </v-btn>
      <v-btn @click="CallEconomic" color="blue darken-4">
        Economic
      </v-btn>
      <v-btn @click="CallFred" color="blue darken-4">
        Fred
      </v-btn>
      <v-btn @click="dummy('Weather')" color="blue darken-4">
        Weather
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
    <template name="formcomponent">
      <v-select
        v-if="!stockresults"
        v-model="selectdataoption"
        :items="alphadataoptions"
        label="Select an alphadata function"
        chips
        clearable
      ></v-select>
      <v-select
        v-if="selectdataoption==='Stock Time Series'"
        v-model="selectstockoption"
        :items="alphastockoptions"
        label="Select a time series option"
        chips
        clearable
      ></v-select>
      <v-select
        v-if="selectdataoption==='Tech Indicators'"
        v-model="selecttechindicator"
        :items="alphatechindicators"
        label="Select tech indicator"
        chips
        clearable
      ></v-select>
      <v-combobox
        v-if="selecttechindicator!==''"
        v-model="selecttechindicatorsymbol"
        :items="alphatechindicatorsymbols"
        label="Select a security"
        chips
        clearable
      ></v-combobox>
      <v-combobox
        v-if="selecttechindicatorsymbol!==''"
        v-model="selecttechindicatortimeperiod"
        :items="alphatechindicatortimeperiod"
        label="Select time period"
        chips
        clearable
      ></v-combobox>
      <v-select
        v-if="selecttechindicatortimeperiod!==''"
        v-model="selecttechseriestype"
        :items="alphatechseriestype"
        label="Select series type"
        chips
        clearable
      ></v-select>
      <v-combobox
        v-if="selectstockoption!==''"
        v-model="selectstock"
        :items="alphabluechipstocks"
        label="Select a stock or type in symbol"
        chips
        clearable
      ></v-combobox>
      <v-select
        v-if="selectdataoption==='Forex'"
        v-model="selectfxoption"
        :items="alphafxoptions"
        label="Select a forex option"
        chips
        clearable
      ></v-select>
      <v-select
        v-if="selectdataoption==='Crypto'"
        v-model="selectcryptooption"
        :items="alphacryptooptions"
        label="Select a crypto option"
        chips
        clearable
      ></v-select>
      <v-combobox
        v-if="selectcryptooption!=''"
        v-model="firstcryptocurrency"
        :items="alphacryptocurrencies"
        label="Select a currency to convert from"
        chips
        clearable
      ></v-combobox>
      <v-combobox
        v-if="firstcryptocurrency!=''"
        v-model="secondcryptocurrency"
        :items="alphafxcurrencies"
        label="Select a currency to convert to"
        chips
        clearable
      ></v-combobox>
      <v-combobox
        v-if="selectfxoption!=''"
        v-model="firstfxcurrency"
        :items="alphafxcurrencies"
        label="Select a currency to convert from"
        chips
        clearable
      ></v-combobox>
      <v-combobox
        v-if="firstfxcurrency!=''"
        v-model="secondfxcurrency"
        :items="alphafxcurrencies"
        label="Select a currency to convert to"
        chips
        clearable
      ></v-combobox>
      <v-select
        v-if="selectdataoption==='Sector Performance'"
        v-model="sectorperformancetime"
        :items="alphasectorperformancetime"
        label="Select a time frame"
        chips
        clearable
      ></v-select>
      <v-btn color="primary" v-if="selectstock!==''" @click="getTimeSeries">
        Query Stock Data
      </v-btn>
      <v-btn color="primary" v-if="secondfxcurrency!==''" @click="getForex">
        Query Forex Data
      </v-btn>
      <v-btn color="primary" v-if="secondcryptocurrency!==''" @click="getCrypto">
        Query Crypto Data
      </v-btn>
      <v-btn color="primary" v-if="sectorperformancetime !==''" @click="getSecPer">
        Query Sector Performance
      </v-btn>
      <v-btn color="primary" v-if="selecttechseriestype !==''" @click="getTechIndicators">
        Query Tech Indicators
      </v-btn>
    </template>
    <template>
      <v-text-field v-if="stockresults"
        v-model="search"
        append-icon="mdi-magnify"
        label="Search Data"
        single-line
        hide-details
      ></v-text-field>
    </template>
    <template v-if="alphadata.TimeSeries.length > 0">
      <v-data-table
        :headers="headers"
        :items="alphadata.TimeSeries"
        class="elevation-1"
        :search="search"
      >
      </v-data-table>
    </template>
    <template v-else-if="alphaquotedata.length > 0">
      <v-data-table
        :headers="quoteheaders"
        :items="alphaquotedata"
        class="elevation-1"
        :search="search">
      </v-data-table>
    </template>
    <template v-else-if="alphaForexData.length > 0">
      <v-data-table
        :headers="forexheaders"
        :items="alphaForexData"
        class="elevation-1"
        :search="search">
      </v-data-table>
    </template>
    <template v-else-if="alphafxcurrencydata.length > 0">
      <v-data-table
        :headers="alphafxcurrencyheader"
        :items="alphafxcurrencydata"
        class="elevation-1"
        :search="search">
      </v-data-table>
    </template>
    <template v-else-if="alphaCryptoData.length > 0">
      <v-data-table
        :headers="cryptoheaders"
        :items="alphaCryptoData"
        class="elevation-1"
        :search="search">
      </v-data-table>
    </template>
    <template v-else-if="alphaTechData.length > 0">
      <v-data-table
        :headers="techheaders"
        :items="alphaTechData"
        class="elevation-1"
        :search="search">
      </v-data-table>
    </template>
    <template v-else-if="alphaSecData.length > 0">
      <v-data-table
        :headers="secheaders"
        :items="alphaSecData"
        class="elevation-1"
        disable-sort
        hide-default-footer>
      </v-data-table>
    </template>
    <template>
      <GoogleChart v-if="showchart" :title="chartTitle"
      :chartData="chartData"></GoogleChart>
    </template>
    <v-dialog
      class="flow_chart"
      v-model="showerror"
      max-width="290">
      <v-card>
        <v-card-title>Error</v-card-title>
        <v-card-text>
          400 Error -- Bad Request
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" small @click="closeError">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import RepositoryFactory from '../repositories/RepositoryFactory';
import store from '../store';

const PostsRepository = RepositoryFactory.get('posts');
export default {
  store,
  data() {
    return {
      components: {
      },
      alphaSecData: [],
      secheaders: [{ text: 'Communication Services', value: 'comsserv' }, { text: 'Consumer Discretionary', value: 'consdisc' }, { text: 'Consumer Staples', value: 'consstaps' }, { text: 'Energy', value: 'energy' }, { text: 'Financials', value: 'financials' }, { text: 'Health Care', value: 'health' }, { text: 'Industrials', value: 'industrials' }, { text: 'IT', value: 'it' }, { text: 'Materials', value: 'materials' }, { text: 'Real Estate', value: 'real' }, { text: 'Utilities', value: 'utils' }],
      sectorperformancetime: '',
      alphasectorperformancetime: ['Real Time', '1 Day', '5 Day', '1 Month', '3 Month', 'Fiscal Year', '1 Year', '3 Year', '5 Year', '10 Year'],
      techheaders: [{ text: 'Value', value: 'value' }, { text: 'Index', value: 'index' }, { text: 'Date', value: 'date' }],
      alphaTechData: [],
      alphaquotedata: [],
      quoteheaders: [{ text: 'Symbol', value: 'Symbol' }, { text: 'Open', value: 'Open' }, { text: 'High', value: 'High' }, { text: 'Low', value: 'Low' }, { text: 'Price', value: 'Price' }, { text: 'Volume', value: 'Volume' }, { text: 'Latest Trading Day', value: 'LatestTradingDay' }, { text: 'Previous Close', value: 'PreviousClose' }, { text: 'Change', value: 'Change' }, { text: 'Change Percent', value: 'ChangePercent' }],
      alphadata: {
        MetaData: [],
        TimeSeries: [],
      },
      headers: [{ text: 'Open', value: 'open' }, { text: 'Close', value: 'close' }, { text: 'High', value: 'high' }, { text: 'Low', value: 'low' }, { text: 'Volume', value: 'volume' }, { text: 'Date (Eastern)', value: 'date' }],
      subheaders: [],
      forexheaders: [{ text: 'Open', value: 'open' }, { text: 'Close', value: 'close' }, { text: 'High', value: 'high' }, { text: 'Low', value: 'low' }, { text: 'Date (UTC)', value: 'date' }],
      alphaForexData: [],
      cryptoheaders: [{ text: 'Open', value: 'open' }, { text: 'Close', value: 'close' }, { text: 'High', value: 'high' }, { text: 'Low', value: 'low' }, { text: 'Volume', value: 'volume' }, { text: 'Market Cap', value: 'market_cap' }, { text: 'Date', value: 'date' }],
      alphaCryptoData: [],
      drawer: false,
      stockname: '',
      menuoptions: ['Analyze', 'Metrics', 'Graphs'],
      selectdataoption: '',
      alphadataoptions: ['Stock Time Series', 'Forex', 'Crypto', 'Tech Indicators', 'Sector Performance'],
      alphastockoptions: ['Intraday', 'Daily', 'Weekly', 'Monthly', 'Quote'],
      alphabluechipstocks: ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB'],
      alphafxoptions: ['Currency Exchange Rate', 'Intraday', 'Daily', 'Weekly', 'Monthly'],
      alphafxcurrencies: ['USD', 'EUR', 'CAD', 'CHF', 'CNY', 'DKK', 'GBP', 'INR', 'JPY', 'RUB'],
      alphacryptocurrencies: ['BTC', 'ETH'],
      alphacryptooptions: ['Currency Exchange Rate', 'Crypto Daily', 'Crypto Weekly', 'Crypto Monthly'],
      alphatechindicators: ['SMA', 'EMA', 'RSI', 'ADX', 'CCI', 'AD', 'OBV'],
      alphatechseriestype: ['High', 'Low', 'Close', 'Open'],
      selecttechseriestype: '',
      selecttechindicator: '',
      selectcryptooption: '',
      firstcryptocurrency: '',
      secondcryptocurrency: '',
      selectfxoption: '',
      firstfxcurrency: '',
      secondfxcurrency: '',
      alphafxcurrencydata: [],
      alphafxcurrencyheader: [{ text: 'From Currency', value: 'FromCurrency' }, { text: 'To Currency', value: 'ToCurrency' }, { text: 'Exchange Rate', value: 'ExchangeRate' }, { text: 'Last Report Time (UTC)', value: 'LastReportTime' }, { text: 'Bid Price', value: 'BidPrice' }, { text: 'Bid Ask', value: 'BidAsk' }],
      selectstockoption: '',
      selectstock: '',
      searchparameters: '',
      stockresults: false,
      countcryptotimekeys: 0,
      alphatechindicatorsymbols: ['FB', 'MSFT', 'AAPL', 'AMZN', 'GOOG'],
      selecttechindicatorsymbol: '',
      alphatechindicatortimeperiod: ['10', '20', '50', '100', '200'],
      selecttechindicatortimeperiod: '',
      analyzedata: false,
      chartData: [['Date', 'High', 'Low']], // Array of Arrays
      chartTitle: '',
      search: '',
      moveable: {
        draggable: true,
      },
      showchart: false,
      showerror: false,
      usernamestring: '',
      loginoptions: ['logout'],
    };
  },
  computed: {
    alphaData() {
      return this.$data.alphadata;
    },
  },
  methods: {
    async getTimeSeries() {
      // this.isLoading = true;
      const payload = {
        dataoption: this.selectdataoption,
        stockoption: this.selectstockoption,
        stock: this.selectstock,
      };
      const { data } = await PostsRepository.postAlpha(payload);
      // this.searchparameters = this.selectdataoption + ' / ' + this.selectstockoption;
      this.selectdataoption = '';
      this.selectstock = '';
      this.selectstockoption = '';
      this.MassageResponse(data);
      this.stockresults = true;
    },
    async getSecPer() {
      const payload = {
        function: 'Sector',
      };
      const { data } = await PostsRepository.postAlpha(payload);
      this.selectdataoption = '';
      let SectorObject = {};
      if (this.sectorperformancetime === 'Real Time') {
        SectorObject = data.RankARealTimePerformance;
      } else if (this.sectorperformancetime === '1 Day') {
        SectorObject = data.RankB1DayPerformance;
      } else if (this.sectorperformancetime === '5 Day') {
        SectorObject = data.RankC5DayPerformance;
      } else if (this.sectorperformancetime === '1 Month') {
        SectorObject = data.RankD1MonthPerformance;
      } else if (this.sectorperformancetime === '3 Month') {
        SectorObject = data.RankE3MonthPerformance;
      } else if (this.sectorperformancetime === '1 Year') {
        SectorObject = data.RankG1YearPerformance;
      } else if (this.sectorperformancetime === '3 Year') {
        SectorObject = data.RankH3YearPerformance;
      } else if (this.sectorperformancetime === '5 Year') {
        SectorObject = data.RankI5YearPerformance;
      } else if (this.sectorperformancetime === '10 Year') {
        SectorObject = data.RankJ10YearPerformance;
      } else {
        SectorObject = data.RankFYeartoDateYTDPerformance;
      }
      // const temporaryKeys = Object.keys(data);
      this.buildSectorObject(SectorObject);
      // const tempObject = data;
      // const newArray = this.createCryptoData(data, temporaryKeys);
      // console.log(newArray);
      this.stockresults = true;
    },
    async getForex() {
      this.isLoading = true;
      const payload = {
        function: this.selectfxoption,
        from_currency: this.firstfxcurrency,
        to_currency: this.secondfxcurrency,
      };
      const { data } = await PostsRepository.postAlpha(payload);
      this.selectdataoption = '';
      this.selectfxoption = '';
      this.firstfxcurrency = '';
      this.secondfxcurrency = '';
      this.MassageResponse(data);
      this.stockresults = true;
    },
    async getCrypto() {
      this.isLoading = true;
      const payload = {
        function: this.selectcryptooption,
        from_currency: this.firstcryptocurrency,
        to_currency: this.secondcryptocurrency,
      };
      const { data } = await PostsRepository.postAlpha(payload);
      this.selectdataoption = '';
      this.selectcryptooption = '';
      this.firstcryptocurrency = '';
      this.secondcryptocurrency = '';
      this.MassageResponse(data);
      this.stockresults = true;
    },
    async getTechIndicators() {
      this.isLoading = true;
      const payload = {
        function: this.selecttechindicator,
        symbol: this.selecttechindicatorsymbol,
        time_period: this.selecttechindicatortimeperiod,
        series_type: this.selecttechseriestype,
      };
      const { data } = await PostsRepository.postAlpha(payload);
      this.stockname = this.selecttechindicatorsymbol;
      this.selectdataoption = '';
      this.selecttechindicatorsymbol = '';
      this.selecttechindicatortimeperiod = '';
      this.selecttechseriestype = '';
      this.MassageResponse(data);
      this.selecttechindicator = '';
      this.stockresults = true;
    },
    massageMetaData(metaKeys, AlphaObject) {
      let nSubKey = '';
      this.alphaquotedata = [];
      let fromStockName = '';
      for (let tempKey = 0; tempKey < metaKeys.length; tempKey += 1) {
        const nKey = metaKeys[tempKey].toString();
        const al = AlphaObject.MetaData[nKey]; // Alias to shorten line 122
        // replacingtimeKeys that have numbers or special characters
        const mystring = nKey.split('.').join('');
        nSubKey = mystring.replace(/[0-9]/g, ' ');
        if (nSubKey === '  Symbol') {
          this.stockname = al;
        } else if (nSubKey === '  From Symbol' || nSubKey === '  To Symbol') { // For Forex Data
          if (fromStockName !== '') {
            this.stockname = `${fromStockName} to ${al} `;
          } else {
            fromStockName = al;
          }
        } else if (nSubKey === '  Digital Currency Code' || nSubKey === '  Market Code') { // For Forex Data
          if (fromStockName !== '') {
            this.stockname = `${fromStockName} to ${al} `;
          } else {
            fromStockName = al;
          }
        }
      }
    },
    MassageResponse(AlphaObject) {
      if (AlphaObject === 'Error') {
        this.showerror = true;
        return;
      }
      const StartingObject = AlphaObject;
      const originalTimeKeys = Object.keys(StartingObject);
      const [meta, time] = originalTimeKeys;
      // eslint-disable-next-line
      console.log(meta);
      if (StartingObject.RealtimeCurrencyExchangeRate) {
        // StartingObject.originalTimeKey = AlphaObject[time];
        this.doCurrencyExchange(StartingObject.RealtimeCurrencyExchangeRate);
        return;
      }
      const forexIndex = time.indexOf('TimeSeriesFX');
      const cryptoIndex = time.indexOf('TimeSeriesDigitalCurrency');
      const techIndex = time.indexOf('TechnicalAnalysis');
      StartingObject.originalTimeKey = AlphaObject[time];
      if (StartingObject.GlobalQuote) {
        this.giveQuote(StartingObject.GlobalQuote);
      } else if (techIndex !== -1) {
        this.createTechIndicatorData(StartingObject, time, this.selecttechindicator);
      } else {
        const metaKeys = Object.keys(StartingObject.MetaData);
        this.massageMetaData(metaKeys, StartingObject);
        const timeKeys = Object.keys(StartingObject[time]);
        let newSubKey = '';
        for (let key = 0; key < timeKeys.length; key += 1) {
          const tempArray = [];
          const newKey = timeKeys[key].toString();
          const subKeys = Object.keys(StartingObject.originalTimeKey[newKey]);
          const a = StartingObject.originalTimeKey[newKey]; // Alias to shorten line 122
          // replacing time keys that have numbers or special characters
          for (let nKeys = 0; nKeys < subKeys.length; nKeys += 1) {
            const mystring = subKeys[nKeys].split('.').join('');
            newSubKey = mystring.replace(/[0-9]/g, ' ');
            if (newSubKey !== subKeys[nKeys]) {
              a[newSubKey] = a[subKeys[nKeys]];
              delete a[subKeys[nKeys]];
              tempArray.push(a[newSubKey]);
            }
          }
          tempArray.push(newKey);
          if (forexIndex !== -1) {
            this.createForexData(tempArray);
          } else if (cryptoIndex !== -1) {
            this.createCryptoData(tempArray, timeKeys);
          } else {
            const newTimeObject = {
              open: tempArray[0],
              high: tempArray[1],
              low: tempArray[2],
              close: tempArray[3],
              volume: tempArray[4],
              date: tempArray[5],
            };
            // eslint-disable-next-line
            console.log(newTimeObject);
            if (Object.entries(newTimeObject).length !== 0) {
              this.alphaData.TimeSeries.push(newTimeObject);
            }
          }
        }
      }
    },
    giveQuote(quote) {
      const QuoteKeys = Object.keys(quote);
      let tempArray = [];
      tempArray = this.prepObject(quote, QuoteKeys);
      const newObject = {
        Symbol: tempArray[0],
        Open: tempArray[1],
        High: tempArray[2],
        Low: tempArray[3],
        Price: tempArray[4],
        Volume: tempArray[5],
        LatestTradingDay: tempArray[6],
        PreviousClose: tempArray[7],
        Change: tempArray[8],
        ChangePercent: tempArray[9],
      };
      this.alphaquotedata = [];
      if (Object.entries(newObject).length !== 0) {
        this.alphaquotedata.push(newObject);
      }
    },
    doCurrencyExchange(fxObject) {
      const fxKeys = Object.keys(fxObject);
      let tempArray = [];
      tempArray = this.prepObject(fxObject, fxKeys);
      const newForexObject = {
        FromCurrency: tempArray[0],
        ToCurrency: tempArray[2],
        ExchangeRate: tempArray[4],
        LastReportTime: tempArray[5],
        BidPrice: tempArray[7],
        BidAsk: tempArray[8],
      };
      if (Object.entries(newForexObject).length !== 0) {
        this.alphafxcurrencydata.push(newForexObject);
      }
      this.stockname = `${newForexObject.FromCurrency} to ${newForexObject.ToCurrency} `;
    },
    createCryptoData(tempArray, timeKeys) {
      const newCryptoObject = {
        open: tempArray[0],
        high: tempArray[2],
        low: tempArray[4],
        close: tempArray[6],
        volume: tempArray[7],
        market_cap: tempArray[8],
        date: timeKeys[this.countcryptotimekeys],
      };
      this.countcryptotimekeys += 1;
      if (Object.entries(newCryptoObject).length !== 0) {
        this.alphaCryptoData.push(newCryptoObject);
      }
    },
    createForexData(tempArray) {
      const newForexObject = {
        open: tempArray[0],
        high: tempArray[1],
        low: tempArray[2],
        close: tempArray[3],
        date: tempArray[4],
      };
      if (Object.entries(newForexObject).length !== 0) {
        this.alphaForexData.push(newForexObject);
      }
    },
    createTechIndicatorData(StartingObject, time, indicator) {
      const timeKeys = Object.keys(StartingObject[time]);
      let newSubKey = '';
      // eslint-disable-next-line
      console.log(indicator);
      for (let key = 0; key < timeKeys.length; key += 1) {
        const tempArray = [];
        const newKey = timeKeys[key].toString();
        const subKeys = Object.keys(StartingObject.originalTimeKey[newKey]);
        const a = StartingObject.originalTimeKey[newKey]; // Alias to shorten line 122
        // replacing time keys that have numbers or special characters
        for (let nKeys = 0; nKeys < subKeys.length; nKeys += 1) {
          const mystring = subKeys[nKeys].split('.').join('');
          newSubKey = mystring.replace(/[0-9]/g, ' ');
          a[newSubKey] = a[subKeys[nKeys]];
          tempArray.push(a[newSubKey]);
        }
        tempArray.push(newSubKey);
        tempArray.push(newKey);
        const techObject = {
          value: tempArray[0],
          index: tempArray[1],
          date: tempArray[2],
        };
        this.alphaTechData.push(techObject);
      }
    },
    prepObject(newObject, tempKeys) {
      const tempObject = newObject;
      const tempArray = [];
      for (let key = 0; key < tempKeys.length; key += 1) {
        const newKey = tempKeys[key].toString();
        const mystring = newKey.split('.').join('');
        const newSubKey = mystring.replace(/[0-9]/g, ' ');
        if (newSubKey !== newObject[key]) {
          tempObject[newSubKey] = tempObject[newKey];
          delete tempObject[newKey];
          tempArray.push(tempObject[newSubKey]);
          if (key === 0) {
            this.stockname = tempObject[newSubKey];
          }
        }
      }
      return tempArray;
    },
    buildSectorObject(StartingObject) {
      this.stockname = this.sectorperformancetime;
      const timeKeys = Object.keys(StartingObject);
      const tempArray = [];
      for (let key = 0; key < timeKeys.length; key += 1) {
        const newKey = timeKeys[key].toString();
        tempArray.push(StartingObject[newKey]);
        this.secheaders.push(timeKeys[key]);
      }
      const SecObject = {
        comsserv: tempArray[0],
        consdisc: tempArray[1],
        consstaps: tempArray[2],
        energy: tempArray[3],
        financials: tempArray[4],
        health: tempArray[5],
        industrials: tempArray[6],
        it: tempArray[7],
        materials: tempArray[8],
        real: tempArray[9],
        utils: tempArray[10],
      };
      this.alphaSecData.push(SecObject);
      this.sectorperformancetime = '';
    },
    cleardata() {
      this.stockname = '';
      this.search = '';
      this.stockresults = false;
      if (this.alphadata.TimeSeries.length > 0) {
        this.alphadata.TimeSeries = []; // To clear the Object
        this.alphadata.TimeSeries.pop(); // To remove the empty object from the array
      } else if (this.alphaquotedata.length > 0) {
        this.alphaquotedata = [];
        this.alphaquotedata.pop();
      } else if (this.alphaForexData.length > 0) {
        this.alphaForexData = [];
        this.alphaquotedata.pop();
      } else if (this.alphafxcurrencydata.length > 0) {
        this.alphafxcurrencydata = [];
        this.alphafxcurrencydata.pop();
      } else if (this.alphaCryptoData.length > 0) {
        this.alphaCryptoData = [];
        this.alphaCryptoData.pop();
        this.countcryptotimekeys = 0;
      } else if (this.alphaTechData.length > 0) {
        this.alphaTechData = [];
        this.alphaTechData.pop();
      } else if (this.alphaSecData.length > 0) {
        this.alphaSecData = [];
        this.alphaSecData.pop();
      }
      this.chartData = [['Date', 'High', 'Low']]; // Array of Arrays;
    },
    home() {
      // this.$store.commit('ShowAlpha', false);
      this.$router.push('/');
    },
    clearChart() {
      this.chartData = [['Date', 'High', 'Low']];
      this.showGraphs();
    },
    showGraphs() {
      // eslint-disable-next-line
      this.chartTitle = this.stockname;
      this.showchart = true;
      if (this.alphaData.TimeSeries.length > 0) {
        for (let x = 0; x < this.alphaData.TimeSeries.length; x += 1) {
          this.chartData.push([this.alphaData.TimeSeries[x].date,
            Number(this.alphaData.TimeSeries[x].high), // Cast the string value to a number
            Number(this.alphaData.TimeSeries[x].low)]); // Cast the string value to a number
        }
      } else if (this.alphaForexData.length > 0) {
        for (let x = 0; x < this.alphaForexData.length; x += 1) {
          this.chartData.push([this.alphaForexData[x].date,
            Number(this.alphaForexData[x].high),
            Number(this.alphaForexData[x].low)]);
        }
      } else if (this.alphaCryptoData.length > 0) {
        for (let x = 0; x < this.alphaCryptoData.length; x += 1) {
          this.chartData.push([this.alphaCryptoData[x].date,
            Number(this.alphaCryptoData[x].high),
            Number(this.alphaCryptoData[x].low)]);
        }
      } else {
        this.chartTitle = 'This Data could not be displayed';
      }
    },
    dummy(item) {
      if (item === 'Graphs') {
        this.showGraphs();
      } else {
        // eslint-disable-next-line
        console.log(item);
      }
    },
    loginOptions() {
      this.usernamestring = '';
      document.cookie = 'username=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'; // Deleting the cookies
      document.cookie = 'password=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
    },
    CallSEC() {
      this.$router.push('/sec');
    },
    CallAgriculture() {
      this.$router.push('/agriculture');
    },
    CallEconomic() {
      this.$router.push('/economic');
    },
    CallFred() {
      this.$router.push('/fred');
    },
    handleDrag({ target, transform }) {
      // eslint-disable-next-line
      console.log('onDrag left, top', transform);
      target.style.transform = transform; // eslint-disable-line no-param-reassign
    },
    close() {
      this.showchart = false;
      this.chartData = [['Date', 'High', 'Low']]; // Array of Arrays;
    },
    closeError() {
      this.showerror = false;
      this.stockresults = false;
      this.search = '';
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
  },
  created() {
    this.alphadata.TimeSeries = [];
    this.alphaquotedata = [];
  },
  mounted() {
    if (document.cookie !== '') { // If there's a coookie, retrieve the sign-in data, otherwise just get the general DJIA data
      this.retrieveCookies();
    }
  },
};
</script>
