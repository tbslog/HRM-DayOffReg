import React, { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import logo from "../../assets/imgs/logoTBS.jpg";
import "./login.css";

import { login } from "../../actions/auth";

const required = (value) => {
  if (!value) {
    return (
      <div className="alert alert-danger" role="alert">
        This field is required!
      </div>
    );
  }
};

const Login = (props) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  let navigate = useNavigate();

  const form = useRef();
  const checkBtn = useRef();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const { isLoggedIn } = useSelector((state) => state.auth);
  const { message } = useSelector((state) => state.message);

  const dispatch = useDispatch();

  const onChangeUsername = (e) => {
    const username = e.target.value;
    setUsername(username);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };
  const validateLogin = {
    userName: {
      required: " Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
    Password: {
      required: " Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
  };

  const onSubmit = (e) => {
    setLoading(true);

    if (!errors.userName?.message && !errors.password?.message) {
      dispatch(login(username, password, 0))
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
    <form onSubmit={handleSubmit(onSubmit)}>
      <section
        className="h-100 gradient-form"
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
                        <label className="form-label" htmlFor="username">
                          Tài khoản
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="tài khoản"
                          {...register("userName", validateLogin.userName)}
                          value={username}
                          onChange={onChangeUsername}
                          validations={[required]}
                        />
                      </div>
                      <p style={{ fontSize: "10px", color: "red" }}>
                        {errors.userName?.message}
                      </p>

                      <div className="form-outline mb-4">
                        <label className="form-label" htmlFor="password">
                          Mật khẩu
                        </label>
                        <input
                          type="password"
                          className="form-control"
                          id="password"
                          {...register("password", validateLogin.Password)}
                          placeholder="Mật khẩu"
                          value={password}
                          onChange={onChangePassword}
                          validations={[required]}
                        />
                      </div>
                      <p style={{ fontSize: "10px", color: "red" }}>
                        {errors.password?.message}
                      </p>

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
                        {message && (
                          <div className="form-group">
                            <div
                              className="alert alert-danger text-center"
                              role="alert"
                            >
                              {message}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="col-lg-6 d-flex align-items-center gradient-custom-2">
                    <div className="text-white px-3 py-4 p-md-5 mx-md-4">
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