import { RCODE } from "./type";

export const rcode = (n) => ({
  type: RCODE,
  payload: n,
});
