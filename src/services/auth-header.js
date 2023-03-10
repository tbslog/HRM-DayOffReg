import Cookies from "js-cookie";

export default function authHeader() {
  const user = JSON.parse(Cookies.get("user"));
  if (user && user) {
    const headers = {
      accept: "application/json",
      "Content-Type": "application/json",
      Authorization: "Bearer " + user,
    };
    // console.log(headers);
    return { headers };
  } else {
    return {};
  }
}
