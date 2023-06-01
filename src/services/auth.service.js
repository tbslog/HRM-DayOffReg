import axios from "axios";
import Cookies from "js-cookie";
import baseURL from "./baseURL";
const API_URL = baseURL;

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
  Cookies.remove("fisstlogin");
};

export default { login, logout };
