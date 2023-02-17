import { combineReducers } from "redux";
import auth from "./auth";
import message from "./message";
import rcode from "./rcode";
import newpass from "./newpass";

export default combineReducers({
  auth,
  message,
  rcode,
  newpass,
});
