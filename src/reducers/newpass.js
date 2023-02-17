import { NEWPASS } from "../actions/type";

const initialState = {};

export default function (state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case NEWPASS:
      return { newpass: payload };
    default:
      return state;
  }
}
