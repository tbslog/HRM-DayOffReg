import { useForm, Controller } from "react-hook-form";
import React, { useState, useEffect, useRef } from "react";

import { getData, postData } from "../../services/user.service";
import { toast } from "react-toastify";
import Cookies from "js-cookie";
let emID = Cookies.get("empid");
const ChangepassHome = (props) => {
  const [message, setmessage] = useState("");
  const [modal, setModal] = useState(null);
  const {
    register,
    handleSubmit,
    setValue,
    reset,
    control,
    formState: { errors },
  } = useForm();

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (props.clear === true) {
      reset();
    }
  }, [props.clear]);
  const hideModal = () => {
    reset();
    modal.hide();
  };

  const validateForm = {
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

  const onChagepassOK = async (data) => {
    console.log(data);
    if (data.passwordNew !== data.passwordNewVerify) {
      setmessage(" Mật khẩu xác nhận không khớp");
    } else {
      setmessage("");
      //console.log("first");
      var create = await postData("changePass", {
        username: emID,
        currentPassword: data.Password,
        newPassword: data.passwordNew,
        confirmPass: data.passwordNewVerify,
      });
      console.log(create);
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
        reset();
        hideModal();
      } else {
        if (create.note) {
          toast.error("Đổi mật khẩu thất bại Lỗi: \n" + create.note, {
            autoClose: 2000,
            className: "",
            position: "top-center",
            theme: "colored",
          });
        } else {
          toast.error("Mật khẩu củ sai \n", {
            autoClose: 2000,
            className: "",
            position: "top-center",
            theme: "colored",
          });
        }
      }
    }
  };
  return (
    <>
      <form>
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="">
            <div className="text-center">
              <h3>ĐỔI MẬT KHẨU </h3>
              <div className="dropdown-divider" />
              <div className="form-outline mb-1">
                <label className="form-label" htmlFor="password">
                  Mật khẩu Cũ
                </label>
                <div className="d-flex">
                  <input
                    className="form-control"
                    id="Password"
                    {...register("Password", validateForm.Password)}
                  />
                </div>
              </div>

              <div className="form-outline mb-1">
                <label className="form-label" htmlFor="password">
                  Mật khẩu mới
                </label>
                <div className="d-flex">
                  <input
                    className="form-control"
                    id="passwordNew"
                    {...register("passwordNew", validateForm.passwordNew)}
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
              </div>
              <div className="form-outline mb-1">
                <label className="form-label" htmlFor="password">
                  Nhập lại mật khẩu mới
                </label>
                <div className="d-flex">
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
              </div>
              <div className="form-group">
                <button
                  className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3"
                  type="submit"
                  disabled={loading}
                  onClick={handleSubmit(onChagepassOK)}
                >
                  {loading && (
                    <span className="spinner-border spinner-border-sm"></span>
                  )}
                  <span> Thay đổi</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};
export default ChangepassHome;
