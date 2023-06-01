import { useForm, Controller } from "react-hook-form";
import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../actions/auth";
import { Navigate, useNavigate } from "react-router-dom";
import { Modal } from "bootstrap";
import { getData, postData } from "../../services/user.service";
import { toast } from "react-toastify";
import Cookies from "js-cookie";

const ChangePass = (props) => {
  let navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [message, setmessage] = useState("");
  const { newpass } = useSelector((state) => state.newpass);

  const dispatch = useDispatch();

  const [ShowModal, SetShowModal] = useState("");
  const [modal, setModal] = useState(null);
  const parseExceptionModal = useRef();

  const [passwordNew, setPasswordNew] = useState("");
  const [passwordNewVerify, setPasswordNewVerify] = useState("");

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

  const {
    register,
    handleSubmit,
    setValue,
    reset,
    control,
    formState: { errors },
  } = useForm();

  useEffect(() => {
    if (props && Object.keys(props).length > 0) {
      setValue("Password", newpass);
      setValue("MSNV", props.user);
    }
  }, [props, props.user]);

  const validateForm = {
    MSNV: {
      required: "Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
    Password: {
      required: "Không được để trống",
      maxLength: {
        value: 15,
        message: " không được hơn 10 kí tự",
      },
    },
    passwordNew: {
      required: "Không được để trống",
      minLength: {
        value: 6,
        message: " không được ít hơn 6 kí tự",
      },
    },
    passwordNewVerify: {
      required: "Không được để trống",
      minLength: {
        value: 6,
        message: " không được ít hơn 6 kí tự",
      },
    },
  };
  const onChagepass = () => {
    showModalForm();
    SetShowModal("change");
  };
  const onChagepassOK = async (data) => {
    console.log(data);
    if (data.passwordNew !== data.passwordNewVerify) {
      setmessage(" Mật khẩu xác nhận không khớp");
    } else {
      console.log("first");
      var create = await postData("changePass", {
        currentPassword: data.Password,
        newPassword: data.passwordNew,
        confirmPass: data.passwordNewVerify,
      });

      if (create.isSuccess === 1) {
        toast.success("Đổi mật khẩu thành công \n" + create.note, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
        setValue("Password", data.passwordNew);
        console.log(data.MSNV);
        Cookies.set("empid", data.MSNV);
        hideModal();
        navigate("/");
        window.location.reload();
      } else {
        toast.error("Đổi mật khẩu thất bại Lỗi: \n" + create.note, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
      }
    }
  };

  const onSubmitReg = async (data) => {
    setLoading(true);
    dispatch(login(data.MSNV, data.Password, 0))
      .then(() => {
        navigate("/");
        window.location.reload();
      })
      .catch(() => {
        setLoading(false);
      });
  };
  return (
    <>
      <form>
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="">
            <div className="card rounded-3 text-black">
              <div className="">
                <div className="card-body p-md-5 mx-md-4">
                  <div className="text-center">
                    <h3>ĐĂNG KÍ NHANH </h3>
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
                      id="MSNV"
                      {...register("MSNV")}
                      className="form-control"
                      placeholder="tài khoản"
                      readOnly
                    />
                  </div>

                  <div className="form-outline mb-3">
                    <label className="form-label" htmlFor="password">
                      Mật khẩu
                    </label>
                    <div className="d-flex">
                      <input
                        id="Password"
                        {...register("Password", validateForm.Password)}
                        className="form-control"
                        readOnly
                      />
                    </div>
                    <span
                      className=""
                      style={{
                        color: "red",
                        fontSize: "10px",
                        marginLeft: "145px",
                      }}
                    >
                      {errors.Password?.message}
                    </span>
                  </div>
                  <div className="text-center mb-5 pb-1">
                    {newpass && (
                      <div className="form-group">
                        <div
                          className="alert alert-danger text-center"
                          role="alert"
                        >
                          <p style={{ fontSize: "12px", margin: "0" }}>
                            TẠO NHANH TÀI KHOẢN THÀNH CÔNG! ANH CHỊ VUI LÒNG
                            NGHI NHỚ MẬT KHẨU
                          </p>
                          <p style={{ fontSize: "12px", margin: "0" }}>
                            HOẶC THAY ĐỔI MẬT KHẨU
                          </p>
                        </div>
                      </div>
                    )}
                    <div className="row">
                      <div className="col-md-6">
                        <button
                          className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                          type="submit"
                          disabled={loading}
                          onClick={handleSubmit(onChagepass)}
                        >
                          {loading && (
                            <span className="spinner-border spinner-border-sm"></span>
                          )}
                          <span>Đổi Mật Khấu</span>
                        </button>
                      </div>
                      <div className="col-md-6">
                        <button
                          className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                          type="submit"
                          disabled={loading}
                          onClick={handleSubmit(onSubmitReg)}
                        >
                          <span>Đăng Nhập</span>
                        </button>
                      </div>
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
                                  ×
                                </span>
                              </button>
                            </div>
                            <div className="modal-body pt-0">
                              <>
                                {ShowModal === "change" && (
                                  <div className="col-md-6 offset-md-3">
                                    <span
                                      className="anchor"
                                      id="formChangePassword"
                                    />
                                    <hr className="mb-5" />
                                    {/* form card change password */}
                                    <div className="card card-outline-secondary">
                                      <div className="card-header">
                                        <h3 className="mb-0">
                                          THAY ĐỔI MẬT KHẨU
                                        </h3>
                                      </div>
                                      <div className="card-body">
                                        <form
                                          className="form"
                                          role="form"
                                          autoComplete="off"
                                        >
                                          <div className="form-group">
                                            <label>MẬT KHẨU CŨ </label>
                                            <input
                                              id="Password"
                                              {...register(
                                                "Password",
                                                validateForm.Password
                                              )}
                                              className="form-control"
                                              readOnly
                                            />
                                          </div>

                                          <div className="form-group">
                                            <label>MẬT KHẨU MỚI</label>
                                            <input
                                              className="form-control"
                                              id="passwordNew"
                                              {...register(
                                                "passwordNew",
                                                validateForm.passwordNew
                                              )}
                                            />
                                          </div>
                                          <p
                                            style={{
                                              fontSize: "10px",
                                              color: "red",
                                            }}
                                          >
                                            {errors.passwordNew?.message}
                                          </p>
                                          <div className="form-group">
                                            <label>NHẬP LẠI MẬT KHẨU</label>
                                            <input
                                              className="form-control"
                                              id="passwordNewVerify"
                                              {...register(
                                                "passwordNewVerify",
                                                validateForm.passwordNewVerify
                                              )}
                                            />
                                          </div>
                                          <p
                                            style={{
                                              fontSize: "10px",
                                              color: "red",
                                            }}
                                          >
                                            {errors.passwordNewVerify?.message}
                                          </p>
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
                                          <div className="form-group">
                                            <button
                                              className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                                              type="submit"
                                              disabled={loading}
                                              onClick={handleSubmit(
                                                onChagepassOK
                                              )}
                                            >
                                              {loading && (
                                                <span className="spinner-border spinner-border-sm"></span>
                                              )}
                                              <span> Thay đổi</span>
                                            </button>
                                          </div>
                                        </form>
                                      </div>
                                    </div>
                                    {/* /form card change password */}
                                  </div>
                                )}
                              </>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};
export default ChangePass;
