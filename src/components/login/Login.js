import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import logo from "../../assets/imgs/logoTBS.jpg";
import "./login.css";

import { login } from "../../actions/auth";
import ChangePass from "./ChangePass";

import { Modal } from "bootstrap";

const Login = (props) => {
  const {
    register,
    handleSubmit,
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

  const [onchanpass, setonchanpass] = useState(false);

  const [showPassword, setShowPassword] = useState(false);

  const [ShowModal, SetShowModal] = useState("");
  const [modal, setModal] = useState(null);
  const parseExceptionModal = useRef();

  const showModalForm = () => {
    const modal = new Modal(parseExceptionModal.current, {
      keyboard: false,
      backdrop: "static",
    });
    setModal(modal);
    modal.show();
  };
  const hideModal = () => {
    modal.hide();
  };

  const dispatch = useDispatch();
  const showRegis = (e) => {
    const username = e.target.value;
    setUsername(username);
  };

  const onChangeUsername = (e) => {
    const username = e.target.value;
    setUsername(username);
  };
  const offRegis = () => {
    window.location.reload();
  };

  const Regis = (e) => {
    dispatch(login(username, password, 1))
      .then(() => {
        showModalForm();
        SetShowModal("change");
      })
      .catch(() => {
        setLoading(false);
      });

    showModalForm();
    SetShowModal("change");
    setPassword(newpass);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };

  const validateLogin = {
    userName: {
      required: " Kh??ng ???????c ????? tr???ng",
      maxLength: {
        value: 10,
        message: " kh??ng ???????c h??n 10 k?? t???",
      },
    },
    Password: {
      required: " Kh??ng ???????c ????? tr???ng",
      maxLength: {
        value: 10,
        message: " kh??ng ???????c h??n 10 k?? t???",
      },
    },
  };

  const onSubmit = (e) => {
    setLoading(true);
    setUsername(username);

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
                        <label className="form-label" htmlFor="username">
                          T??i kho???n
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="t??i kho???n"
                          {...register("userName", validateLogin.userName)}
                          value={username}
                          onChange={onChangeUsername}
                        />
                      </div>
                      <p style={{ fontSize: "10px", color: "red" }}>
                        {errors.userName?.message}
                      </p>

                      <div className="form-outline mb-4">
                        <label className="form-label" htmlFor="password">
                          M???t kh???u
                        </label>
                        <div className="d-flex">
                          <input
                            type={showPassword ? "text" : "password"}
                            className="form-control"
                            id="password"
                            {...register("password", validateLogin.Password)}
                            placeholder="M???t kh???u"
                            value={password}
                            onChange={onChangePassword}
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
                        {rcode === 1 && (
                          <div className="d-flex justify-content-center mb-0">
                            <button
                              className="btn btn-success gradient-custom-2"
                              style={{ width: "80px" }}
                              type="submit"
                              onClick={Regis}
                            >
                              <span>C??</span>
                            </button>
                            <button
                              className="btn btn-primary gradient-custom-2 ml-3 "
                              style={{ width: "80px" }}
                              type="submit"
                              onClick={offRegis}
                            >
                              <span>Kh??ng</span>
                            </button>
                          </div>
                        )}
                      </div>
                      <>
                        <div
                          className="modal fade"
                          id="modal-xl"
                          data-backdrop="static"
                          ref={parseExceptionModal}
                          aria-labelledby="parseExceptionModal"
                          backdrop="static"
                        >
                          <div
                            className="modal-dialog modal-dialog-scrollable"
                            style={{ maxWidth: "88%" }}
                          >
                            <div className="modal-content">
                              <div className="modal-header border-0 p-0">
                                <button
                                  type="button"
                                  className="close ml"
                                  data-dismiss="modal"
                                  onClick={() => hideModal()}
                                  aria-label="Close"
                                >
                                  <span
                                    aria-hidden="true"
                                    style={{ fontSize: "30px" }}
                                  >
                                    ??
                                  </span>
                                </button>
                              </div>
                              <div className="modal-body pt-0">
                                <>
                                  {ShowModal === "change" && (
                                    <ChangePass user={username} />
                                  )}
                                </>
                              </div>
                            </div>
                          </div>
                        </div>
                      </>
                    </div>
                  </div>
                  <div className="col-lg-6 d-flex align-items-center gradient-custom-2">
                    <div className="text-white px-3 py-4  mx-md-4">
                      <h4 className="mb-4">
                        "TBS LOGISTICS l?? ?????i t??c uy t??n v?? ????ng tin c???y c???a c??c
                        Kh??ch H??ng h??ng ?????u Th??? Gi???i."
                      </h4>
                      <p className="small mb-0">
                        TBS Logistics t???a l???c t???i trung t??m t??? gi??c kinh t??? ph??a
                        Nam TP.HCM ??? B??nh D????ng ??? ?????ng Nai ??? B?? R???a V??ng T??u.
                      </p>
                      <br />
                      <p className="small mb-0">
                        H??? th???ng kho b??i quy m?? l???n, theo ti??u chu???n qu???c t???:
                        di???n t??ch kho l??n ?????n 220.000 m2 v???i s???c ch???a t???i ??a
                        60,000 containers tr???i d??i t??? kho ngo???i quan ?????n kho n???i
                        ?????a, t??? kho b??ch h??a ?????n kho chuy??n d???ng.
                      </p>
                      <br />
                      <p className="small mb-0">
                        H??? th???ng c?? s??? h??? t???ng v?? c??ng ngh??? hi???n ?????i: l???p ?????t
                        ph???n m???m qu???n l?? quy tr??nh logistics ti??n ti???n nh???m ki???m
                        so??t ho???t ?????ng v???n h??nh kho b??i m???t c??ch ch??nh x??c nh???t.
                      </p>
                      <br />
                      <p className="small mb-0">
                        Thi???t k??? xanh: khu??n vi??n c?? c??ng vi??n bao b???c xung
                        quanh, t???o n??n kh??ng gian tho??ng m??t v?? g???n g??i v???i m??i
                        tr?????ng.
                      </p>
                      <br />
                      <p className="small mb-0">
                        PCCC: H??? th???ng PCCC Sprinkler t??? ?????ng ???????c ?????u t?? v??
                        thi???t k??? chuy??n nghi???p. C??ng t??c hu???n luy???n, di???n t???p
                        PCCC ???????c th?????ng xuy??n t??? ch???c h??ng tu???n, h??ng th??ng cho
                        to??n b??? c??n b??? c??ng nh??n vi??n v?? c??c l???c l?????ng n???i b???
                        t???i ch???, ph???i h???p v???i C??ng An PCCC c??ng t??? ch???c c??c kh??a
                        hu???n luy???n nh???m n??ng cao ki???n th???c an to??n ch??y n???, s???n
                        s??ng cho m???i t??nh hu???ng c?? th??? x???y ra.
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
