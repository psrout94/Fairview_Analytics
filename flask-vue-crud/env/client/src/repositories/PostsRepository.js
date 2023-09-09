import Repository from './Repository';

const resource = {
  alpha: '/alpha',
  news: '/news',
  sec: '/sec',
  yahoo: '/yahoo',
  fred: '/fred',
  export: '/export',
  userstockdata: '/userstockdata',
  createnewuser: '/usercreation',
  signinuser: '/usersignin',
  // setcookie: '/setcookie',
  accountdata: '/getaccount',
  changepassword: '/changepassword',
  changestocks: '/changestocks',
};
export default {
  postAlpha(payload) {
    return Repository.post(`${resource.alpha}`, payload);
  },

  getPostAlpha(postId) {
    return Repository.get(`${resource.alpha}/${postId}`);
  },

  createPostalpha(payload) {
    return Repository.post(`${resource.alpha}`, payload);
  },

  postNews(payload) {
    return Repository.post(`${resource.news}`, payload);
  },

  postSec(payload) {
    return Repository.post(`${resource.sec}`, payload);
  },

  getYahoo() {
    return Repository.post(`${resource.yahoo}`);
  },

  postYahoo(payload) {
    return Repository.post(`${resource.yahoo}`, payload);
  },

  getFred(payload) {
    return Repository.post(`${resource.fred}`, payload);
  },

  exportData(payload) {
    return Repository.post(`${resource.export}`, payload);
  },

  getStockDbData() {
    return Repository.post(`${resource.userstockdata}`);
  },

  createNewUser(payload) {
    return Repository.post(`${resource.createnewuser}`, payload);
  },

  signInNewUser(payload) {
    return Repository.post(`${resource.signinuser}`, payload);
  },

  /* setCookie(payload) {
    return Repository.post(`${resource.setcookie}`, payload);
  }, */

  getAccountData(payload) {
    return Repository.post(`${resource.accountdata}`, payload);
  },

  changeUserPassword(payload) {
    return Repository.post(`${resource.changepassword}`, payload);
  },

  changeStocks(payload) {
    return Repository.post(`${resource.changestocks}`, payload);
  },
};
