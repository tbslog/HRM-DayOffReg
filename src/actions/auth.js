import {
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  SET_MESSAGE,
  RCODE,
  NEWPASS,
} from "./type";
import AuthService from "../services/auth.service";

export const login = (username, password, autogen) => (dispatch) => {
  return AuthService.login(username, password, autogen).then(
    (data) => {
      console.log(data);
      if (data.rCode === 0) {
        const message = data.rMsg;
        dispatch({
          type: LOGIN_FAIL,
        });
        dispatch({
          type: SET_MESSAGE,
          payload: message,
        });

        return Promise.reject();
      }
      if (data.rCode === 1) {
        const message =
          data.rMsg + " bạn có muốn tạo tự động tài khoản không ?";
        dispatch({
          type: LOGIN_FAIL,
        });
        dispatch({
          type: SET_MESSAGE,
          payload: message,
        });
        dispatch({
          type: RCODE,
          payload: data.rCode,
        });

        return Promise.reject();
      }
      if (data.rCode === 3) {
        console.log("login sussec");
        dispatch({
          type: LOGIN_SUCCESS,
          payload: { user: data },
        });

        return Promise.resolve();
      }
      if (data.rCode === 2) {
        const message = data.rMsg + " :" + data.rData.password;
        dispatch({
          type: LOGIN_FAIL,
        });
        dispatch({
          type: SET_MESSAGE,
          payload: message,
        });

        dispatch({
          type: NEWPASS,
          payload: data.rData.password,
        });
        dispatch({
          type: RCODE,
          payload: data.rCode,
        });

        return Promise.reject();
      }
    },
    (error) => {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();

      dispatch({
        type: LOGIN_FAIL,
      });

      dispatch({
        type: SET_MESSAGE,
        payload: message,
      });

      return Promise.reject();
    }
  );
};

export const logout = () => (dispatch) => {
  AuthService.logout();

  dispatch({
    type: LOGOUT,
  });
};
