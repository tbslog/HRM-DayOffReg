import axios from "axios";
import authHeader from "./auth-headerIMG";

const API_URL = "http://192.168.0.35:300/";
//103.149.28.137:300/ // anh kiểu

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
    })
    .then((response) => {
      data = response.data;
      console.log(data);
    })
    .catch((error) => {
      console.log(`${error.response.data}`);
    });

  return data;
};
export { postIMG, getIMG };
