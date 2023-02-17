import { RCODE } from "../actions/type";

const initialState = {};

export default function (state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case RCODE:
      return { rcode: payload };
    default:
      return state;
  }
}
