import axios from "axios";
import authHeader from "./auth-headerIMG";

import baseURL from "./baseURL";
const API_URL = baseURL;
//103.149.28.137:300/ // anh kiểu
//http://192.168.0.42:300
//"http://tlogapi.tbslogistics.com.vn:202/";
const postIMG = async (url, image) => {
  let dataReturn = [];

  await axios
    .post(API_URL + url, image, {
      headers: authHeader().headers,
    })
    .then((response) => {
      dataReturn = response.data;
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
    });
  return dataReturn;
};
const getIMG = async (url) => {
  let data;
  await axios
    .get(API_URL + url, {
      headers: authHeader().headers,
      responseType: "blob",
    })
    .then((response) => {
      data = response.data;
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
    });

  return data;
};
export { postIMG, getIMG };
