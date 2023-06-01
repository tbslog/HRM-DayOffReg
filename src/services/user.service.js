import axios from "axios";
import authHeader from "./auth-header";
import { computeHeadingLevel } from "@testing-library/react";
import baseURL from "./baseURL";
const API_URL = baseURL;
//103.149.28.137:300/ // anh kiểuy

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
const postData = async (url, data) => {
  var isSuccess = 0;
  var note = "";

  await axios
    .post(API_URL + url, data, {
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
        isSuccess = 1;
        note = response.data?.rMsg;
        return { isSuccess, note };
      } else if (response.data.rCode === 0) {
        var n = Object.keys(response.data.rError).forEach((key) => {
          note += response.data.rError[key];
        });

        isSuccess = 0;
        return { isSuccess, note };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note };
};
const postDataCustom = async (url, data) => {
  var isSuccess = 0;
  var note = "";

  await axios
    .post(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      //console.log(response);
      if (response.data.rCode === 1) {
        if (response.data.rError) {
          Object.keys(response.data.rError).forEach((key) => {
            note += response.data.rError[key];
          });
          isSuccess = 1;
          return { isSuccess, note };
        }
        isSuccess = 1;
        note = response.data?.rMsg;
        return { isSuccess, note };
      } else if (response.data.rCode === 0) {
        note = response.data?.rMsg;
        isSuccess = 0;
        return { isSuccess, note };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note };
};
const putData = async (url, data, header = null) => {
  var isSuccess = 0;
  var note = "";
  await axios
    .put(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      if (response.data.rCode === 1) {
        if (response.data.rError) {
          Object.keys(response.data.rError).forEach((key) => {
            note += response.data.rError[key];
          });
          isSuccess = 1;
          return { isSuccess, note };
        }
        isSuccess = 1;
        note = response.data?.rMsg;
        return { isSuccess };
      } else if (response.data.rCode === 0) {
        var n = Object.keys(response.data.rError).forEach((key) => {
          note += response.data.rError[key] + response.data?.rMsg;
        });
        isSuccess = 0;

        return { isSuccess, note };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note };
};
const putDataCus = async (url, data, header = null) => {
  var isSuccess = 0;
  var note = "";
  await axios
    .put(API_URL + url, data, {
      headers: authHeader().headers,
    })
    .then((response) => {
      if (response.data.rCode === 1) {
        if (response.data.rError) {
          Object.keys(response.data.rError).forEach((key) => {
            note += response.data.rError[key];
          });
          isSuccess = 1;
          return { isSuccess, note };
        }
        isSuccess = 1;
        note = response.data?.rMsg;
        return { isSuccess };
      } else if (response.data.rCode === 0) {
        note = response.data?.rMsg;
        return { isSuccess, note };
      }
    })
    .catch((error) => {
      isSuccess = 0;
      return { isSuccess, note: error };
    });

  return { isSuccess, note };
};

export {
  getDataCustom,
  getData,
  postData,
  putData,
  getfile,
  putDataCus,
  postDataCustom,
};
