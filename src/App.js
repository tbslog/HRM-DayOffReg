import { Routes, Route } from "react-router-dom";
import PrivateRoutes from "./router/PrivateRoutes";

import "react-tabs/style/react-tabs.css";
import "react-datepicker/dist/react-datepicker.css";

import "react-toastify/dist/ReactToastify.css";
import Home from "./components/Home";
import Login from "./components/login/Login";
import IndexListRegister from "./components/register/IndexListRegister";
import Register from "./components/register/Register";
import Info from "./components/profile/Info";

function App() {
  const accountType = "all";
  return (
    <Routes>
      <Route element={<PrivateRoutes />}>
        {accountType && accountType === "all" && (
          <>
            <Route path="/home" element={<Home />} />
            <Route path="/indexListRegister" element={<IndexListRegister />} />
            <Route path="/register" element={<Register />} />
            <Route path="/info" element={<Info />} />
          </>
        )}
        <Route path="/" element={<Home />} exact />
        <Route path="*" element={<Home />} />
      </Route>
      <Route element={<Login />} path="/login"></Route>
      <Route element={<Login />} path="/"></Route>
    </Routes>
  );
}

export default App;
