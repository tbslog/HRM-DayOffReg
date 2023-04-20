import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://192.168.0.35:300/";
//103.149.28.137:300/ // anh kiểu

const getDataCustom = async (url, data, header = null) => {
  let dataReturn = [];
  await axios
    .post(API_URL + url, data, {
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
const getfile = async (url) => {
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
  var note = "";
  var rMsg = "";

  await axios
    .post(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      console.log(response.data.rCode);
      if (response.data.rCode === 1) {
        console.log(response);
        if (response.data.rError) {
          Object.keys(response.data.rError).forEach((key) => {
            note += response.data.rError[key];
          });
          isSuccess = 1;
          return { isSuccess, note };
        }
        if (response.data.rMsg) {
          Object.keys(response.data.rMsg).forEach((key) => {
            rMsg += response.data.rMsg[key];
          });
          isSuccess = 1;
          return { isSuccess, note, rMsg };
        }
        isSuccess = 1;
        return { isSuccess };
      } else if (response.data.rCode === 0) {
        console.log(response);
        Object.keys(response.data.rMsg).forEach((key) => {
          rMsg += response.data.rMsg[key];
        });
        Object.keys(response.data.rError).forEach((key) => {
          note += response.data.rError[key];
        });

        isSuccess = 0;
        return { isSuccess, note, rMsg };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note, rMsg };
};
const putData = async (url, data, header = null) => {
  var isSuccess = 0;
  var note = "";
  var rMsg = "";
  await axios
    .put(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      console.log(response);
      if (response.data.rCode === 1) {
        if (response.data.rError) {
          Object.keys(response.data.rError).forEach((key) => {
            note += response.data.rError[key];
          });

          isSuccess = 1;
          return { isSuccess, note };
        }
        if (response.data.rMsg) {
          Object.keys(response.data.rMsg).forEach((key) => {
            rMsg += response.data.rMsg[key];
          });
          isSuccess = 1;
          return { isSuccess, note, rMsg };
        }
        isSuccess = 1;
        return { isSuccess };
      } else if (response.data.rCode === 0) {
        Object.keys(response.data.rMsg).forEach((key) => {
          rMsg += response.data.rMsg[key];
        });
        Object.keys(response.data.rError).forEach((key) => {
          note += response.data.rError[key];
        });
        isSuccess = 0;
        return { isSuccess, note, rMsg };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note, rMsg };
};
export { getDataCustom, getData, postData, putData, getfile };
