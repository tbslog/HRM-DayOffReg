//pages
import Home from "../components/Home";
import Login from "../components/login/Login";
import IndexListRegister from "../components/register/IndexListRegister";

const privateRouters = [
  { path: "/", component: Home },
  { path: "/home", component: Home },
  { path: "/indexListRegister", component: IndexListRegister },
];

// đăng nhập mới vào được còn không chuyến hướng
const publicRouters = [
  { path: "/", component: Login },
  { path: "/login", component: Login },
];

export { publicRouters, privateRouters };
