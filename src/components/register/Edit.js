import React, { useState, useEffect, useCallback } from "react";
import { useForm, Controller, set } from "react-hook-form";
import Cookies from "js-cookie";
import { getData, putDataCus } from "../../services/user.service";
import moment from "moment";
import DatePicker from "react-datepicker";
import { Navigate, useNavigate } from "react-router-dom";
import Loading from "../common/loading/Loading";
import { toast } from "react-toastify";

import Pupup from "../common/Pupup";

let emID = Cookies.get("empid");
const Edit = (props) => {
  const {
    register,
    setValue,
    handleSubmit,
    reset,
    control,
    formState: { errors },
  } = useForm();

  let navigate = useNavigate();
  const [IsLoading, setIsLoading] = useState(false);
  const [name, setname] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  const [jobpositionName, setJobpositionName] = useState("");
  const [annualLeave, setAnnualLeave] = useState("");
  const [comeDate, setcomeDate] = useState("");
  const [jPLevelName, setJPLevelName] = useState("");
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [showmess, setShowmess] = useState("");
  const [showmessHandel, setShowmessHandel] = useState("");

  const [type, setType] = useState("");
  const [regID, setregID] = useState("");
  const [pupupcus, setpupupcus] = useState(false);
  const [savesendbutton, setsavesendbutton] = useState(0);
  const [startdateV, setstartdateV] = useState("");
  const [enddateV, setenddateV] = useState("");
  const [period, setperiod] = useState("");
  const [emIDnv, setemIDnv] = useState("");

  useEffect(
    () => {
      if (
        props &&
        props.dataRegByID &&
        Object.keys(props.dataRegByID).length > 0 &&
        Object.keys(props).length > 0
      ) {
        setregID(props.dataRegByID.rData?.regID);
        setType(props.dataRegByID.rData.Type);
        setValue("NgayBatDau", new Date(props.dataRegByID.rData.StartDate));
        setstartdateV(new Date(props.dataRegByID.rData.StartDate));
        setValue("songaynghi", props.dataRegByID.rData.Period);
        setValue("address", props.dataRegByID.rData.Address);
        setValue("reason", props.dataRegByID.rData.Reason);
        setValue("offType", props.dataRegByID.rData.Type);
        setperiod(props.dataRegByID.rData.Period);
        setenddateV(
          moment(props.dataRegByID.rData.EndDate).format("DD-MM-YYYY")
        );
      }
    },
    [props, props.dataRegByID, props.fullName],
    regID
  );
  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData(`day-off-letter?regid=${regID}`);

      setValue("MSNV", data.rData?.EmpID);
      setemIDnv(data.rData?.EmpID);
      //console.log(data.rData);
      setname(data.rData.LastName + " " + data.rData.FirstName);
      setDepartmentName(data.rData.departmentName);
      setJobpositionName(data.rData?.JobPositionName);
      setAnnualLeave(data.rData.AnnualLeave);
      setcomeDate(moment(data.rData.comedate).format("DD-MM-YYYY"));
      setJPLevelName(data.rData.Position);
      let dataTypeOff = await getData("dayOffType");
      setlistTypeOff(dataTypeOff.rData);
      //console.log(dataTypeOff);
      setIsLoading(false);
    })();
  }, [props, regID]);
  const checkType = (id) => {
    const result = listTypeOff.find(({ OffTypeID }) => OffTypeID === id);
    let a = result?.Name + "(" + result?.Note + ")";
    return a;
  };
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
  const onSubmitSave = (data) => {
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
    setIsLoading(true);
    var create = await putDataCus("adjust-day-off", {
      regid: regID,
      offtype: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),

      address: data.address,
      command: 0,
      period: period,
    });

    if (create.isSuccess === 1) {
      toast.success("lưu đơn thành công \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setpupupcus(false);
      setsavesendbutton(0);
      props.fetchData();
      props.hideModal();

      reset();
      setIsLoading(false);
      navigate("/indexListRegister");
    } else {
      toast.error("lưu thất bại Lỗi \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      setIsLoading(false);
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
    var create = await putDataCus("adjust-day-off", {
      regid: regID,
      offtype: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),
      period: period,
      address: data.address,
      command: 1,
    });
    if (create.isSuccess === 1) {
      toast.success("Gửi đơn thành công \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      setpupupcus(false);
      setsavesendbutton(0);
      reset();
      props.fetchData();
      props.hideModal();
      setIsLoading(false);
      navigate("/indexListRegister");
    } else {
      toast.error("Gửi thất bại Lỗi \n" + create.note, {
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

  const savesend = (data) => {
    if (savesendbutton === 1) {
      save(data);
    } else if (savesendbutton === 2) {
      send(data);
    }
  };
  // const handelClickViewWorkingDays = async (e) => {
  //   e.preventDefault(); // loại bỏ ngăn chặn reload
  //   if (
  //     startdateV === "" ||
  //     startdateV === undefined ||
  //     startdateV === "" ||
  //     startdateV === undefined
  //   ) {
  //     console.log("lỗi");
  //   } else {
  //     let st = moment(new Date(startdateV).toISOString()).format("YYYY-MM-DD");
  //     let ed = moment(new Date(enddateV).toISOString()).format("YYYY-MM-DD");

  //     var getDay = await getData(
  //       `workingDays?emplID=${emIDnv}&startDate=${st}&endDate=${ed}`
  //     );
  //     setperiod(getDay.rData.period);
  //     console.log(getDay.rData.period);
  //   }
  // };
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
      <section className="content" style={{ minHeight: "620px" }}>
        {/* Default box */}
        <div className="card  " style={{ minHeight: "630px" }}>
          {IsLoading ? (
            <Loading />
          ) : (
            <div className="card-header py-0 border-0">
              <h2 className="p-4" style={{ textAlign: "center" }}>
                ĐƠN NGHỈ PHÉP
              </h2>
              <div className="row mt-3">
                <div className="col-md-6 d-flex">
                  MSNV
                  <p style={{ color: "red", minWidth: "74px" }}>(*)</p>
                  <input
                    id="MSNV"
                    {...register("MSNV")}
                    className="form-control ml-3 "
                    readOnly
                    style={{ maxWidth: "200px" }}
                  />
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
                  <span style={{ minWidth: "120px" }}>Họ và tên</span>
                  <input
                    {...register("fullName")}
                    id="fullName"
                    readOnly
                    className="form-control ml-3 "
                    value={name}
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
                      id="offType"
                    >
                      <option value={type}>{checkType(type)}</option>
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
                  <span style={{ minWidth: "120px" }}>Số phép năm hiện có</span>
                  <input
                    value={annualLeave}
                    className="form-control ml-3 "
                    readOnly
                    style={{ maxWidth: "80px" }}
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
                  <div className="w-100 ml-3" style={{ maxWidth: "100px" }}>
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
                    id="reason"
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
                    id="address"
                  />
                </div>
              </div>
              <div className="mt-3 d-flex justify-content-end">
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
          )}
        </div>
      </section>
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

export default Edit;
