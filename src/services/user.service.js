import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://192.168.0.103:300/";
//103.149.28.137:300

const getInfoEmplID = (EmpId) => {
  return axios.get(API_URL + "getEmpInfo?EmpId=" + EmpId, {
    headers: authHeader().headers,
  });
};
const getDataCustom = async (url, data, header = null) => {
  let dataReturn = [];
  await axios
    .post(API_URL + url, data, header)
    .then((response) => {
      dataReturn = response.data;
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
    });
  return dataReturn;
};
const getData = async (url) => {
  let data;
  await axios
    .get(API_URL + url, {
      headers: authHeader().headers,
    })
    .then((response) => {
      data = response.data;
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
    });

  return data;
};
const postData = async (url, data, header = null) => {
  var isSuccess = 0;
  await axios
    .post(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      console.log(`${response.data}`);
      return (isSuccess = 1);
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
      return (isSuccess = 0);
    });

  return isSuccess;
};
export { getInfoEmplID, getDataCustom, getData, postData };
