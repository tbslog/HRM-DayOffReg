import React, { useState, useEffect, useCallback } from "react";
import { useForm, Controller, set } from "react-hook-form";
import Cookies from "js-cookie";
import { getData, postData, postDataCustom } from "../../services/user.service";
import moment from "moment";
import DatePicker from "react-datepicker";
import { Navigate, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Loading from "../common/loading/Loading";
import { toast } from "react-toastify";
import Pupup from "../common/Pupup";

let emID = Cookies.get("empid");

const Register = () => {
  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors },
  } = useForm();
  const [IsLoading, setIsLoading] = useState(false);
  let navigate = useNavigate();
  const [name, setname] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  const [jobpositionName, setJobpositionName] = useState("");
  const [annualLeave, setAnnualLeave] = useState("");
  const [comeDate, setcomeDate] = useState("");
  const [jPLevelName, setJPLevelName] = useState("");
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [listNV, setlistNV] = useState([]);

  const [emIDnv, setEmIDnv] = useState("");
  const [namenv, setnamenv] = useState("");
  const [MSNV, setMSNV] = useState("");

  const [showmess, setShowmess] = useState("");
  const [showmessHandel, setShowmessHandel] = useState("");
  const [savesendbutton, setsavesendbutton] = useState(0);
  const [pupupcus, setpupupcus] = useState(false);
  const [startdateV, setstartdateV] = useState("");
  const [enddateV, setenddateV] = useState("");
  const [period, setperiod] = useState("");

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData(`getEmpInfo?empId=${emID}`);
      setEmIDnv(emID);
      setname(data.rData.LastName + " " + data.rData.FirstName);
      setDepartmentName(data.rData.DepartmentName);
      setJobpositionName(data.rData.JobpositionName);
      setAnnualLeave(data.rData.AnnualLeave);
      setcomeDate(moment(data.rData.ComeDate).format("DD-MM-YYYY"));
      setJPLevelName(data.rData.JPLevelName);
      let name = data.rData.LastName + " " + data.rData.FirstName;

      let dataTypeOff = await getData("dayOffType");
      //console.log(dataTypeOff.rData);
      setlistTypeOff(dataTypeOff.rData);
      setIsLoading(false);
      let listlowergradedata = await getData("list-of-subordinates");
      console.log(listlowergradedata);
      if (listlowergradedata.rCode === 0) {
        setlistNV([
          {
            EmpID: emID,
            Name: data.rData.LastName + " " + data.rData.FirstName,
          },
        ]);
        console.log(listNV);
      } else {
        var lista = listlowergradedata.rData.map(
          ({ EmpID, FirstName, LastName }) => ({
            EmpID,
            Name: `${LastName} ${FirstName}`,
          })
        );
        lista.unshift({
          EmpID: emID,
          Name: data.rData.LastName + " " + data.rData.FirstName,
        });

        setlistNV(lista);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      let data = await getData(`getEmpInfo?empId=${emIDnv}`);

      setnamenv(data.rData?.LastName + " " + data.rData?.FirstName);
      setDepartmentName(data.rData?.DepartmentName);
      setJobpositionName(data.rData?.JobpositionName);
      setAnnualLeave(data.rData?.AnnualLeave);
      setcomeDate(moment(data.rData?.ComeDate).format("DD-MM-YYYY"));
      setJPLevelName(data.rData?.JPLevelName);
    })();
  }, [emIDnv]);

  const validateForm = {
    MSNV: {
      required: "Không được để trống",
      maxLength: {
        value: 10,
        message: " không được hơn 10 kí tự",
      },
    },
    reason: {
      required: " Không được để trống",
    },
    songaynghi: {
      required: " Không được để trống",
      pattern: {
        value: /^[0-9]*$/,
        message: "Chỉ được nhập  số",
      },
    },
    NgayBatDau: {
      required: " Không được để trống",
    },
    NgayKetThuc: {
      required: " Không được để trống",
    },
    offType: {
      required: " Không được để trống",
    },
  };

  const onSubmitSave = async (data) => {
    setsavesendbutton(1);
    var e = new Date();

    e.setDate(e.getDate() + 1);
    if (
      moment(new Date(e).toISOString()).format("YYYY-MM-DD") >=
      moment(new Date(data?.NgayBatDau).toISOString()).format("YYYY-MM-DD")
    ) {
      setpupupcus(true);
      setShowmess("Ngày Nghỉ phép không đúng quy định ");
      setShowmessHandel(" Bạn có muốn tiếp tục không ?");
    } else {
      save(data);
      setsavesendbutton(0);
    }
  };
  const save = async (data) => {
    let isotherRegis = "";
    if (emID != emIDnv) {
      isotherRegis = 1;
    } else {
      isotherRegis = 0;
    }

    setIsLoading(true);

    var create = await postDataCustom("day-off-letter", {
      emplid: emIDnv,
      type: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),
      address: data.address,
      command: 0,
      period: period,
    });
    // console.log(create);
    if (create.isSuccess === 1) {
      toast.success("lưu đơn thành công \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      reset();
      setIsLoading(false);
      setpupupcus(false);
      setsavesendbutton(0);
      navigate("/indexListRegister");
    } else {
      toast.error("lưu  thất bại Lỗi \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      setIsLoading(false);
    }
  };
  const onSubmitSend = async (data) => {
    setsavesendbutton(2);
    var e = new Date();

    e.setDate(e.getDate() + 1);

    if (
      moment(new Date(e).toISOString()).format("YYYY-MM-DD") >=
      moment(new Date(data.NgayBatDau).toISOString()).format("YYYY-MM-DD")
    ) {
      setpupupcus(true);
      setShowmess("Ngày Nghỉ phép không đúng quy định ");
      setShowmessHandel(" Bạn có muốn tiếp tục không ?");
    } else {
      send(data);
      setsavesendbutton(0);
    }
  };
  const send = async (data) => {
    // let isotherRegis = "";
    // if (emID != emIDnv) {
    //   isotherRegis = 1;
    // } else {
    //   isotherRegis = 0;
    // }

    setIsLoading(true);

    var create = await postDataCustom("day-off-letter", {
      emplid: emIDnv,
      type: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),
      address: data.address,
      command: 1,
      period: period,
    });

    if (create.isSuccess === 1) {
      toast.success("Gửi đơn thành công \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      reset();
      setIsLoading(false);
      setpupupcus(false);
      setsavesendbutton(0);

      navigate("/indexListRegister");
    } else {
      toast.error("Gửi thất bại Lỗi: \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      setIsLoading(false);
    }
  };

  const savesend = (data) => {
    if (savesendbutton === 1) {
      save(data);
    } else if (savesendbutton === 2) {
      send(data);
    }
  };
  const handeleder = (e) => {
    setEmIDnv(e.target.value);
  };

  const handleBlur = () => {
    if (startdateV === "" || startdateV === undefined) {
      setenddateV("Nhập ngày bắt đầu");
    }
    if (period !== "") {
      const roundedNumber = Math.round((Number(period) * 10) / 5) / 2;
      setperiod(roundedNumber.toString());
      const roundedNumber1 = Math.round(Number(roundedNumber));
      const inputDate = new Date(startdateV);
      const resultDate = new Date(
        inputDate.getTime() +
          roundedNumber1.toString() * 24 * 60 * 60 * 1000 -
          1 * 24 * 60 * 60 * 1000
      );
      setenddateV(
        moment(new Date(resultDate).toISOString()).format("DD-MM-YYYY")
      );
    }
  };
  const onchangeday = async (e) => {
    if (period === "" || period === undefined) {
      setenddateV("Nhập số ngày nghỉ");
    } else {
      const roundedNumber = Math.round((Number(period) * 10) / 5) / 2;
      setperiod(roundedNumber.toString());
      const roundedNumber1 = Math.round(Number(roundedNumber));
      const inputDate = new Date(e);
      const resultDate = new Date(
        inputDate.getTime() +
          roundedNumber1.toString() * 24 * 60 * 60 * 1000 -
          1 * 24 * 60 * 60 * 1000
      );

      setenddateV(
        moment(new Date(resultDate).toISOString()).format("DD-MM-YYYY")
      );
    }
    setstartdateV(e);
  };
  return (
    <form>
      <div className="content-wrapper pb-0 ">
        <section className="content" style={{ minHeight: "100%" }}>
          {/* Default box */}
          <div className="card  " style={{ minHeight: "100vh" }}>
            {IsLoading ? (
              <Loading />
            ) : (
              <div className="card-header py-0 border-0">
                <h2 className="p-4" style={{ textAlign: "center" }}>
                  ĐĂNG KÍ PHÉP
                </h2>
                <div className="row">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>
                      Họ Và Tên <span style={{ color: "red" }}>*</span>
                    </span>
                    <select
                      className="form-control ml-3"
                      style={{ borderRadius: "5px" }}
                      {...register("selectEmpIDNV", validateForm.selectEmpIDNV)}
                      onChange={handeleder}
                      selectEmpIDNV
                    >
                      {listNV &&
                        listNV.map((val) => {
                          return (
                            <option value={val.EmpID} key={val.EmpID}>
                              {val.Name}
                            </option>
                          );
                        })}
                    </select>
                  </div>
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}> Đ.Vị/B.Phận</span>
                    <input
                      className="form-control ml-3"
                      readOnly
                      value={departmentName}
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>MSNV</span>
                    <input
                      value={emIDnv}
                      readOnly
                      className="form-control ml-3 "
                    />
                  </div>
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}> Chức Vụ</span>
                    <input
                      className="form-control ml-3"
                      readOnly
                      value={jPLevelName}
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>Ngày vào Làm</span>
                    <input
                      value={comeDate}
                      readOnly
                      className="form-control ml-3 "
                    />
                  </div>
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}> Vị trí CV</span>
                    <input
                      className="form-control ml-3"
                      value={jobpositionName}
                      readOnly
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>
                      Loại Phép <span style={{ color: "red" }}>*</span>
                    </span>

                    <div className="ml-3 w-100">
                      <select
                        className="form-control"
                        {...register("offType", validateForm.offType)}
                      >
                        <option value="">Chọn Loại Phép</option>
                        {listTypeOff &&
                          listTypeOff.map((val) => {
                            return (
                              <option value={val.OffTypeID} key={val.OffTypeID}>
                                {val.Name}( {val.Note})
                              </option>
                            );
                          })}
                      </select>
                      <span
                        className=""
                        style={{
                          color: "red",
                          fontSize: "10px",
                        }}
                      >
                        {errors.offType?.message}
                      </span>
                    </div>
                  </div>
                  <div className="col-md-6 d-flex justify-content-between">
                    <span style={{ minWidth: "120px" }}>
                      Số phép năm hiện có
                    </span>
                    <input
                      value={annualLeave}
                      className="form-control ml-3 "
                      style={{ maxWidth: "80px" }}
                      readOnly
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-4 d-flex  ">
                    <span style={{ minWidth: "120px" }}>
                      Ngày bắt đầu<span style={{ color: "red" }}>*</span>
                    </span>
                    <div className="input-group ml-3 ">
                      <Controller
                        control={control}
                        name="NgayBatDau"
                        render={({ field }) => (
                          <DatePicker
                            className="form-control "
                            dateFormat="dd/MM/yyyy"
                            placeholderText="Chọn ngày bắt đầu"
                            onChange={(date) => {
                              field.onChange(date);
                              //setstartdateV(date);
                              onchangeday(date);
                            }}
                            selected={field.value}
                          />
                        )}
                        rules={validateForm.NgayBatDau}
                      />
                      {errors.NgayBatDau && (
                        <span
                          className=""
                          style={{
                            color: "red",
                            fontSize: "10px",
                          }}
                        >
                          {errors.NgayBatDau.message}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="col-md-4 d-flex justify-content-center mt-1 ">
                    <span> Số ngày nghỉ</span>
                    <div className="w-100 ml-3" style={{ maxWidth: "60px" }}>
                      <input
                        value={period}
                        className="form-control "
                        onBlur={handleBlur}
                        onChange={(e) => setperiod(e.target.value)}
                      />

                      <span
                        className=""
                        style={{
                          color: "red",
                          fontSize: "10px",
                        }}
                      >
                        {errors.songaynghi?.message}
                      </span>
                    </div>
                  </div>
                  <div className="col-md-4 d-flex justify-content-end mt-1">
                    <span style={{ minWidth: "120px" }}>
                      Ngày Kết thúc <span style={{ color: "red" }}>*</span>
                    </span>
                    <div className="input-group ml-3 ">
                      <input
                        value={enddateV}
                        className="form-control ml-3 "
                        readOnly
                      />
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
                      {...register("address")}
                    />
                  </div>
                </div>
                <div className="mt-3 d-flex justify-content-between mb-1">
                  <Link
                    to="/indexListRegister"
                    className="btn btn  btn-success "
                  >
                    <i className="fas fa-arrow-left"></i> Quay Lại
                  </Link>

                  <div>
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
                </div>
                {/* end */}
              </div>
            )}
          </div>
        </section>
      </div>
      {pupupcus && (
        <Pupup
          onClose={() => setpupupcus(false)}
          title={" Cảnh báo "}
          color="#FFFFFF"
        >
          <div className="row m-3">
            <p>
              {showmess} <br /> {showmessHandel}
            </p>
          </div>
          <div className="row d-flex justify-content-center p-3 ">
            <button
              className="btn btn-primary  "
              type="button"
              onClick={handleSubmit(savesend)}
            >
              {" "}
              Đồng ý
            </button>
          </div>
        </Pupup>
      )}
    </form>
  );
};
export default Register;
