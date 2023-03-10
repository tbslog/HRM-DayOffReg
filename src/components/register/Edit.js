import Popup from "../common/Popup";
import React, { useState, useEffect, useCallback } from "react";
import { useForm, Controller } from "react-hook-form";
import Cookies from "js-cookie";
import { getData, postData, putData } from "../../services/user.service";
import moment from "moment";
import DatePicker from "react-datepicker";
import { Navigate, useNavigate } from "react-router-dom";
import Loading from "../common/loading/Loading";
import { toast } from "react-toastify";
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
  const [reason, setReason] = useState("");
  const [songaynghi, setsongaynghi] = useState("");
  const [address, setAddress] = useState("");
  const [type, setType] = useState("");
  const [regID, setregID] = useState("");

  useEffect(() => {
    //console.log(props.dataRegByID);
    if (
      props &&
      props.dataRegByID &&
      Object.keys(props.dataRegByID).length > 0 &&
      Object.keys(props).length > 0
    ) {
      //console.log(props.dataRegByID.rData);
      setregID(props.dataRegByID.rData?.regID);
      setValue("MSNV", props.dataRegByID.rData.EmpID);
      setType(props.dataRegByID.rData.Type);
      setValue("NgayBatDau", new Date(props.dataRegByID.rData.StartDate));
      setValue("songaynghi", props.dataRegByID.rData.Period);
      setValue("address", props.dataRegByID.rData.Address);
      setValue("reason", props.dataRegByID.rData.Reason);
      setValue("offType", props.dataRegByID.rData.Type);
    }
    setValue("fullName", props.fullName);
    (async () => {
      let data = await getData("getEmpInfo", emID);
      //console.log(data.rData);
      setname(data.rData.FirstName + " " + data.rData.LastName);
      setDepartmentName(data.rData.DepartmentName);
      setJobpositionName(data.rData.JobpositionName);
      setAnnualLeave(data.rData.AnnualLeave);
      setcomeDate(moment(data.rData.ComeDate).format("DD-MM-YYYY"));
      setJPLevelName(data.rData.JPLevelName);

      let dataTypeOff = await getData("dayOffType");
      setlistTypeOff(dataTypeOff.rData);
      //console.log(dataTypeOff);
    })();
  }, [props, props.dataRegByID, props.fullName]);
  const checkType = (id) => {
    const result = listTypeOff.find(({ OffTypeID }) => OffTypeID === id);
    let a = result?.Name + "(" + result?.Note + ")";
    return a;
  };
  const validateForm = {
    MSNV: {
      required: "Kh??ng ???????c ????? tr???ng",
      maxLength: {
        value: 10,
        message: " kh??ng ???????c h??n 10 k?? t???",
      },
    },
    reason: {
      required: " Kh??ng ???????c ????? tr???ng",
    },
    songaynghi: {
      required: " Kh??ng ???????c ????? tr???ng",
      pattern: {
        value: /^[0-9]*$/,
        message: "Ch??? ???????c nh???p  s???",
      },
    },
    NgayBatDau: {
      required: " Kh??ng ???????c ????? tr???ng",
    },
    offType: {
      required: " Kh??ng ???????c ????? tr???ng",
    },
  };

  const onSubmitSave = async (data) => {
    setIsLoading(true);
    console.log(data);
    var create = await putData("adjust-day-off", {
      regid: regID,
      offtype: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),
      period: data.songaynghi,
      address: data.address,
      command: 0,
    });
    console.log(create);
    if (create.isSuccess === 1) {
      toast.success("l??u ????n th??nh c??ng \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      navigate("/indexListRegister");
      window.location.reload();
      reset();
      setIsLoading(false);
    } else {
      toast.success("l??u  th???t b???i L???i \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setIsLoading(false);
    }
  };
  const onSubmitSend = async (data) => {
    setIsLoading(true);
    var create = await putData("adjust-day-off", {
      regid: regID,
      offtype: data.offType,
      reason: data.reason,
      startdate: moment(new Date(data.NgayBatDau).toISOString()).format(
        "YYYY-MM-DD"
      ),
      period: data.songaynghi,
      address: data.address,
      command: 1,
    });
    console.log(create);
    if (create.isSuccess === 1) {
      toast.success("G???i ????n th??nh c??ng \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      navigate("/indexListRegister");
      reset();
      props.fetchData();
      props.hideModal();
      setIsLoading(false);
    } else {
      toast.danger("G???i ????n th???t b???i L???i: \n" + create.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setIsLoading(false);
    }
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
                ????N NGH??? PH??P
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
                  <span style={{ minWidth: "120px" }}> ??.V???/B.Ph???n</span>
                  <input
                    className="form-control ml-3"
                    readOnly
                    value={departmentName}
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>H??? v?? t??n</span>
                  <input
                    {...register("fullName")}
                    id="fullName"
                    readOnly
                    className="form-control ml-3 "
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Ch???c V???</span>
                  <input
                    className="form-control ml-3"
                    readOnly
                    value={jPLevelName}
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>Ng??y v??o L??m</span>
                  <input
                    value={comeDate}
                    readOnly
                    className="form-control ml-3 "
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> V??? tr?? CV</span>
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
                    Lo???i Ph??p <span style={{ color: "red" }}>*</span>
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
                  <span style={{ minWidth: "120px" }}>S??? ph??p n??m hi???n c??</span>
                  <input
                    value={annualLeave}
                    className="form-control ml-3 "
                    readOnly
                    style={{ maxWidth: "80px" }}
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex pr-4 ">
                  <span style={{ minWidth: "120px" }}>
                    B???t ?????u ngh??? t??? <span style={{ color: "red" }}>*</span>
                  </span>
                  <div className="input-group ml-3 ">
                    <Controller
                      control={control}
                      name="NgayBatDau"
                      id="NgayBatDau"
                      render={({ field }) => (
                        <DatePicker
                          className="form-control "
                          dateFormat="dd/MM/yyyy"
                          placeholderText="Ch???n ng??y b???t ?????u"
                          onChange={(date) => field.onChange(date)}
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
                <div className="col-md-6 d-flex justify-content-between">
                  <span style={{ minWidth: "120px" }}>
                    S??? Ng??y Ngh??? <span style={{ color: "red" }}>*</span>
                  </span>

                  <div className="w-100 ml-3" style={{ maxWidth: "120px" }}>
                    <input
                      type="text"
                      className="form-control "
                      {...register("songaynghi", validateForm.songaynghi)}
                      id="songaynghi"
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
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span style={{ minWidth: "120px" }}>
                    L?? do ngh??? ph??p<span style={{ color: "red" }}>*</span>
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
                  <span style={{ minWidth: "120px" }}>?????a ch??? ngh??? ph??p</span>
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
                  L??u
                </button>
                <button
                  className="btn btn  btn-success border border-light mr-5"
                  type="submit"
                  onClick={handleSubmit(onSubmitSend)}
                >
                  G???i
                </button>
              </div>

              {/* end */}
            </div>
          )}
        </div>
      </section>
    </form>
  );
};

export default Edit;
