import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://tlogapi.tbslogistics.com.vn:202/";
// "http://tlogapi.tbslogistics.com.vn:202/";
//"http://192.168.0.45:300/"; cty
//http://192.168.0.114:300/
//103.149.28.137:300
//tlogapi.tbslogistics.com.vn:202 /

const login = (username, password, autogen) => {
  return axios
    .post(API_URL + "Login", {
      username,
      password,
      autogen,
    })
    .then((response) => {
      console.log(response);
      if (response.data.rData?.token) {
        Cookies.set("user", JSON.stringify(response.data.rData.token));
        Cookies.set("empid", JSON.stringify(response.data.rData.empid));
      }
      return response.data;
    });
};

const logout = () => {
  Cookies.remove("user");
  Cookies.remove("empid");
  Cookies.remove("info");
};

export default { login, logout };
