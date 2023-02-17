import { useForm, Controller } from "react-hook-form";
import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../actions/auth";
import { Navigate, useNavigate } from "react-router-dom";

const ChangePass = (props) => {
  let navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [message, setmessage] = useState("");
  const { newpass } = useSelector((state) => state.newpass);

  const dispatch = useDispatch();

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
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
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
          <div className="col-xl-10">
            <div className="card rounded-3 text-black">
              <div className="row g-0">
                <div className="col-lg-6">
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

                    <div className="form-outline mb-4">
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
                    <div className="text-center pt-1 mb-5 pb-1">
                      {newpass && (
                        <div className="form-group">
                          <div
                            className="alert alert-danger text-center"
                            role="alert"
                          >
                            TẠO NHANH TÀI KHOẢN THÀNH CÔNG! ANH CHỊ VUI LÒNG
                            NGHI NHỚ MẬT KHẨU
                          </div>
                        </div>
                      )}
                      <button
                        className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                        type="submit"
                        disabled={loading}
                        onClick={handleSubmit(onSubmitReg)}
                      >
                        {loading && (
                          <span className="spinner-border spinner-border-sm"></span>
                        )}
                        <span>Đăng Nhập</span>
                      </button>
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
