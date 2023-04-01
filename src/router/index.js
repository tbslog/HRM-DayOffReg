//pages
import Home from "../components/Home";
import Login from "../components/login/Login";
import IndexListRegister from "../components/register/IndexListRegister";
import Register from "../components/register/Register";
import Info from "../components/profile/Info";

const privateRouters = [
  { path: "/", component: Home },
  { path: "/home", component: Home },
  { path: "/indexListRegister", component: IndexListRegister },
  { path: "/Register", component: Register },
  { path: "/info", component: Info },
];

// đăng nhập mới vào được còn không chuyến hướng
const publicRouters = [
  { path: "/", component: Login },
  { path: "/login", component: Login },
];

export { publicRouters, privateRouters };
