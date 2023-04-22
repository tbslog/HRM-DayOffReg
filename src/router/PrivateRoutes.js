import { Outlet, Navigate } from "react-router-dom";
import { ToastContainer, Bounce } from "react-toastify";
import Cookies from "js-cookie";
import Layoutmaster from "../components/Layoutmaster";

const PrivateRoutes = () => {
  let token = Cookies.get("user");
  console.log(token);
  return token ? (
    <>
      <ToastContainer transition={Bounce} />
      <Layoutmaster>
        <Outlet />
      </Layoutmaster>
    </>
  ) : (
    <Navigate to="/login" />
  );
};

export default PrivateRoutes;
