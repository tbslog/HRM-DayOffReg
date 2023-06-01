import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import logo from "../../assets/imgs/logoTBS.jpg";
import "./login.css";

import { login } from "../../actions/auth";

import { Modal } from "bootstrap";
import Cookies from "js-cookie";

const Login = (props) => {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm();
  let navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  //const [newp, setnewp] = useState("");
  const [loading, setLoading] = useState(false);

  const { isLoggedIn } = useSelector((state) => state.auth);
  const { message } = useSelector((state) => state.message);
  const { rcode } = useSelector((state) => state.rcode);
  const { newpass } = useSelector((state) => state.newpass);

  const [showPassword, setShowPassword] = useState(false);
  const [message1, setMessage1] = useState("");

  const dispatch = useDispatch();

  const onChangeUsername = (e) => {
    const username = e.target.value;
    setUsername(username);
  };
  const offRegis = () => {
    window.location.reload();
  };

  const Regis = () => {
    setShowPassword(true);

    Cookies.set("empid", JSON.stringify(username));
    Cookies.set("fisstlogin", JSON.stringify(1));
    setMessage1(
      "Tạo mới tài khoản thành công \n Anh,Chị vui lòng nhớ mật khẩu cho lần đăng nhập lần sau"
    );
    dispatch(login(username, password, 1))
      .then(() => {
        // console.log("first1");
        // setPassword(newpass);
        // setValue("password", newpass);
        // setMessage1(
        //   "Tạo mới tài khoản thành công \n Anh,Chị vui lòng nhớ mật khẩu cho lần đăng nhập lần sau"
        // );
      })
      .catch(() => {
        setLoading(false);
      });
  };
  useEffect(() => {
    if (newpass !== "" || newpass !== undefined) {
      setValue("password", newpass);
      setPassword(newpass);
    } else {
      setShowPassword(false);
    }
  }, [newpass]);

  const validateLogin = {
    userName: {
      required: " Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
  };

  const onSubmit = (e) => {
    setLoading(true);
    setUsername(username);

    if (!errors.userName?.message && !errors.password?.message) {
      dispatch(login(username, e.password, 0))
        .then(() => {
          navigate("/");
          window.location.reload();
        })
        .catch(() => {
          setLoading(false);
        });
    } else {
      console.log(2);
      setLoading(false);
    }
  };
  useEffect(() => {
    if (isLoggedIn) {
      <Navigate to="/" />;
    }
  }, [isLoggedIn]);

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="d-flex justify-content-center"
      style={{ alignItems: "center", width: "100%", height: "100vh" }}
    >
      <section
        className="h-100 gradient-form pt-3"
        style={{ backgroundColor: "white" }}
      >
        <div
          className="container h-100"
          style={{
            paddingTop: "1 rem !important",
            paddingBottom: "1 rem !important",
          }}
        >
          <div className="row d-flex justify-content-center align-items-center h-100">
            <div className="col-xl-10">
              <div className="card rounded-3 text-black">
                <div className="row g-0">
                  <div className="col-lg-6">
                    <div className="card-body p-md-5 mx-md-4">
                      <div className="text-center">
                        <img
                          src={logo}
                          style={{ width: "185px" }}
                          alt="logo"
                        ></img>
                        <h4
                          className="mt-1 mb-5 pb-1"
                          style={{ borderBottom: "1px solid black" }}
                        ></h4>
                      </div>

                      <div className="form-outline mb-4">
                        {message && rcode === 0 && (
                          <p style={{ color: "red" }}>{message}</p>
                        )}
                        <label className="form-label" htmlFor="username">
                          Tài khoản
                        </label>

                        <input
                          type="text"
                          className="form-control"
                          placeholder="tài khoản"
                          {...register("userName")}
                          value={username}
                          onChange={onChangeUsername}
                        />
                      </div>

                      <div className="form-outline mb-4">
                        <label className="form-label" htmlFor="password">
                          Mật khẩu
                        </label>
                        <div className="d-flex">
                          <input
                            type={showPassword ? "text" : "password"}
                            className="form-control"
                            id="password"
                            {...register("password", validateLogin.Password)}
                            placeholder="Mật khẩu"
                          />
                          <button
                            className="border-0"
                            onClick={() => setShowPassword(!showPassword)}
                            type="button"
                          >
                            <span className="fa fa-fw fa-eye field-icon toggle-password"></span>
                          </button>
                        </div>
                        <p style={{ fontSize: "10px", color: "red" }}>
                          {errors.password?.message}
                        </p>
                      </div>

                      <div className="text-center pt-1 mb-5 pb-1">
                        <button
                          className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                          disabled={loading}
                          type="submit"
                        >
                          {loading && (
                            <span className="spinner-border spinner-border-sm"></span>
                          )}
                          <span>Login</span>
                        </button>
                        {message1 && (
                          <div className="form-group">
                            <div className="alert text-center" role="alert">
                              {message1}
                            </div>
                          </div>
                        )}
                        {message && rcode === 1 && (
                          <div className="form-group">
                            <div className="alert text-center" role="alert">
                              {message}
                            </div>
                          </div>
                        )}
                        {rcode === 1 && (
                          <div className="d-flex justify-content-center mb-0">
                            <button
                              className="btn btn-success gradient-custom-2"
                              style={{ width: "80px" }}
                              type="submit"
                              onClick={Regis}
                            >
                              <span>Có</span>
                            </button>
                            <button
                              className="btn btn-primary gradient-custom-2 ml-3 "
                              style={{ width: "80px" }}
                              type="submit"
                              onClick={offRegis}
                            >
                              <span>Không</span>
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="col-lg-6 d-flex align-items-center gradient-custom-2">
                    <div className="text-white px-3 py-4  mx-md-4">
                      <h4 className="mb-4">
                        "TBS LOGISTICS là đối tác uy tín và đáng tin cậy của các
                        Khách Hàng hàng đầu Thế Giới."
                      </h4>
                      <p className="small mb-0">
                        TBS Logistics tọa lạc tại trung tâm tứ giác kinh tế phía
                        Nam TP.HCM – Bình Dương – Đồng Nai – Bà Rịa Vũng Tàu.
                      </p>
                      <br />
                      <p className="small mb-0">
                        Hệ thống kho bãi quy mô lớn, theo tiêu chuẩn quốc tế:
                        diện tích kho lên đến 220.000 m2 với sức chứa tối đa
                        60,000 containers trải dài từ kho ngoại quan đến kho nội
                        địa, từ kho bách hóa đến kho chuyên dụng.
                      </p>
                      <br />
                      <p className="small mb-0">
                        Hệ thống cơ sở hạ tầng và công nghệ hiện đại: lắp đặt
                        phần mềm quản lý quy trình logistics tiên tiến nhằm kiểm
                        soát hoạt động vận hành kho bãi một cách chính xác nhất.
                      </p>
                      <br />
                      <p className="small mb-0">
                        Thiết kế xanh: khuôn viên có công viên bao bọc xung
                        quanh, tạo nên không gian thoáng mát và gần gũi với môi
                        trường.
                      </p>
                      <br />
                      <p className="small mb-0">
                        PCCC: Hệ thống PCCC Sprinkler tự động được đầu tư và
                        thiết kế chuyên nghiệp. Công tác huấn luyện, diễn tập
                        PCCC đựơc thường xuyên tổ chức hàng tuần, hàng tháng cho
                        toàn bộ cán bộ công nhân viên và các lực lượng nội bộ
                        tại chỗ, phối hợp với Công An PCCC cùng tổ chức các khóa
                        huấn luyện nhằm nâng cao kiến thức an toàn cháy nổ, sẵn
                        sàng cho mọi tình huống có thể xảy ra.
                      </p>
                      <br />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </form>
  );
};

export default Login;
