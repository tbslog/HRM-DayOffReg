import React, { useState, useEffect, useCallback } from "react";
import { useForm } from "react-hook-form";
import Cookies from "js-cookie";
import { getData } from "../../services/user.service";
import moment from "moment";
import DatePicker from "react-datepicker";

let emID = Cookies.get("empid");

const Register = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [name, setname] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  const [jobpositionName, setJobpositionName] = useState("");
  const [annualLeave, setAnnualLeave] = useState("");
  const [comeDate, setcomeDate] = useState("");
  const [jPLevelName, setJPLevelName] = useState("");
  const [listTypeOff, setlistTypeOff] = useState([]);

  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  useEffect(() => {
    (async () => {
      let data = await getData("getEmpInfo", emID);

      setname(data.FirstName + " " + data.LastName);
      setDepartmentName(data.DepartmentName);
      setJobpositionName(data.JobpositionName);
      setAnnualLeave(data.AnnualLeave);
      setcomeDate(moment(data.ComeDate).format("DD-MM-YYYY"));
      setJPLevelName(data.JPLevelName);

      let dataTypeOff = await getData("dayOffType");
      console.log(dataTypeOff);
      setlistTypeOff(dataTypeOff);
    })();
  }, []);
  const validateForm = {
    MSNV: {
      required: " Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
    reason: {
      required: " Không được để trống",
    },
  };

  const onSubmitSave = (data) => console.log(data, "save");
  const onSubmitSend = (data) => console.log(data, "send");
  return (
    <form>
      <div className="content-wrapper pb-0 ">
        <section className="content" style={{ minHeight: "620px" }}>
          {/* Default box */}
          <div className="card  " style={{ minHeight: "630px" }}>
            <div className="card-header py-0 border-0">
              <h2 className="p-4" style={{ textAlign: "center" }}>
                ĐĂNG KÍ PHÉP
              </h2>
              <div className="row">
                <div className="col-md-6 d-flex">
                  MSNV
                  <p style={{ color: "red", minWidth: "74px" }}>(*)</p>
                  <input
                    {...register("MSNV", validateForm.MSNV)}
                    type="text"
                    value={emID}
                    disabled
                    className="form-control ml-3 "
                    style={{ maxWidth: "200px" }}
                    id="MSNV"
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Đ.Vị/B.Phận</span>
                  <input
                    type="text"
                    className="form-control ml-3"
                    disabled
                    value={departmentName}
                    id="MSNV"
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>Họ và tên</span>
                  <input
                    disabled
                    value={name}
                    type="text"
                    className="form-control ml-3 "
                    id="hoten"
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Chức Vụ</span>
                  <input
                    type="text"
                    className="form-control ml-3"
                    disabled
                    value={jPLevelName}
                    id="MSNV"
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>Ngày vào Làm</span>
                  <input
                    value={comeDate}
                    disabled
                    type="text"
                    className="form-control ml-3 "
                    id="hoten"
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Vị trí CV</span>
                  <input
                    type="text"
                    className="form-control ml-3"
                    value={jobpositionName}
                    id="MSNV"
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>
                    Loại Phép <span style={{ color: "red" }}>*</span>
                  </span>
                  <select className="form-control ml-3">
                    <option value="">Chọn Loại Phép</option>
                    {listTypeOff &&
                      listTypeOff.map((val) => {
                        return (
                          <option value={val.Name} key={val.OffTypeID}>
                            {val.Name}( {val.Note})
                          </option>
                        );
                      })}
                  </select>
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span style={{ minWidth: "120px" }}>Số phép năm hiện có</span>
                  <input
                    type="text"
                    value={annualLeave}
                    disabled
                    className="form-control ml-3 "
                    style={{ maxWidth: "80px" }}
                    id="MSNV"
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex pr-4">
                  <span style={{ minWidth: "120px" }}>Bắt đầu nghỉ từ</span>
                  <DatePicker
                    selected={fromDate}
                    onChange={(date) => setFromDate(date)}
                    dateFormat="dd/MM/yyyy"
                    className="ml-3 form-control "
                    placeholderText="Từ ngày"
                    value={fromDate}
                  />
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span style={{ minWidth: "120px" }}>
                    Số Ngày Nghỉ <span style={{ color: "red" }}>*</span>
                  </span>

                  <div className="w-100 ml-3" style={{ maxWidth: "120px" }}>
                    <input type="text" className="form-control " id="MSNV" />
                    <span
                      className=""
                      style={{
                        color: "red",
                        fontSize: "10px",
                      }}
                    >
                      {errors.reason?.message}
                    </span>
                  </div>
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span style={{ minWidth: "120px" }}>
                    Lí do nghỉ phép<span style={{ color: "red" }}>*</span>
                  </span>
                  <textarea
                    {...register("reason", validateForm.reason)}
                    type="text"
                    className="form-control ml-3 "
                    id="hoten"
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
                  {errors.reason?.message}
                </span>
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span style={{ minWidth: "120px" }}>Địa chỉ nghỉ phép</span>
                  <textarea
                    type="text"
                    className="form-control ml-3 "
                    id="hoten"
                  />
                </div>
              </div>
              <div className="  mt-3 d-flex justify-content-end">
                <button
                  className="btn btn  btn-success border border-light mr-3 "
                  type="submit"
                  onClick={handleSubmit(onSubmitSave)}
                >
                  Lưu
                </button>
                <button
                  className="btn btn  btn-success border border-light mr-5"
                  type="submit"
                  onClick={handleSubmit(onSubmitSend)}
                >
                  Gửi
                </button>
              </div>

              {/* end */}
            </div>
          </div>
        </section>
      </div>
    </form>
  );
};
export default Register;
