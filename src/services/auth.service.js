import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://192.168.0.103:300/";
//103.149.28.137:300

const login = (username, password, autogen) => {
  return axios
    .post(API_URL + "Login", {
      username,
      password,
      autogen,
    })
    .then((response) => {
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
};

export default { login, logout };
