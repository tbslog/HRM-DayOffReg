import Popup from "../common/Popup";
import moment from "moment";
import { getData, postData } from "../../services/user.service";
import React, { useState, useEffect, useCallback } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import Loading from "../common/loading/Loading";
import { useForm, Controller } from "react-hook-form";

const Approve = (props) => {
  const {
    register,
    setValue,
    handleSubmit,
    reset,
    control,
    formState: { errors },
  } = useForm();
  const [IsLoading, setIsLoading] = useState(true);
  const [regID, setregID] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  const [jobpositionName, setJobpositionName] = useState("");
  const [annualLeave, setAnnualLeave] = useState("");
  const [comeDate, setcomeDate] = useState("");
  const [jPLevelName, setJPLevelName] = useState("");
  const [MSNV, setMSNV] = useState("");
  const [name, setname] = useState("");
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [type, setType] = useState("");
  const [RegDate, setRegDate] = useState("");
  const [Period, setPeriod] = useState("");
  const [Reason, setReason] = useState("");
  const [Address, setAddress] = useState("");
  const [show, setshow] = useState("");
  const [aStatus, setaStatus] = useState("");
  const [approJobName, setApproJobName] = useState("");
  const [approName, setApproName] = useState("");
  const [approvalDate, setApprovalDate] = useState("");
  const [comment, setComment] = useState("");
  const [Showstream, setShowstream] = useState(false);
  const [Showstream1, setShowstream1] = useState("");

  let info = JSON.parse(Cookies.get("info"));

  useEffect(() => {
    //console.log(info);
    setIsLoading(true);
    if (props.isShow === false) {
      setshow(false);
    } else {
      setshow(true);
    }
    (async () => {
      console.log(props.dataRegByID.rData);
      let data = await getData(
        `getEmpInfo?empId=${props.dataRegByID.rData?.EmpID}`
      );
      //console.log(data.rData);

      setregID(props.dataRegByID.rData.regID);
      setMSNV(props.dataRegByID.rData.EmpID);
      setname(data.rData.FirstName + " " + data.rData.LastName);
      setDepartmentName(data.rData.DepartmentName);
      setJobpositionName(data.rData.JobpositionName);
      setAnnualLeave(data.rData.AnnualLeave);
      setcomeDate(moment(data.rData.ComeDate).format("DD-MM-YYYY"));
      setJPLevelName(data.rData.JPLevelName);
      setType(props.dataRegByID.rData.Type);
      setRegDate(moment(props.dataRegByID.rData.RegDate).format("DD-MM-YYYY"));
      setPeriod(props.dataRegByID.rData.Period);
      setReason(props.dataRegByID.rData.Reason);
      setAddress(props.dataRegByID.rData.Address);
      setaStatus(aStatusShow(props.dataRegByID.rData?.aStatus));

      //console.log(props.isme);
      if (props.dataRegByID.rData?.aStatus === 1 && props.isAppove === false) {
        setApprovalDate("");
        setApproName("");
        setApproJobName("");
        setComment("");

        console.log("first");
      }

      if (props.dataRegByID.rData?.aStatus === 1 && props.isAppove === true) {
        setApprovalDate(moment(new Date()).format("DD-MM-YYYY"));
        setApproName(info.FirstName + " " + info.LastName);
        setApproJobName(info.JobpositionName);
        setComment("");
        setshow(false);
        console.log("2");
      } else {
        if (props.isme === true) {
          if (props.dataRegByID.rData?.aStatus == 1) {
            setApprovalDate("");
            setApproName("");
            setApproJobName("");
            setComment("");
          } else {
            console.log(props.dataRegByID.rData?.apprInf[0]);
            setShowstream(true);

            setApprovalDate(
              moment(props.dataRegByID.rData?.apprInf[0]?.ApprovalDate).format(
                "DD-MM-YYYY"
              )
            );
            setApproName(
              props.dataRegByID.rData?.apprInf[0].ApproFirstName +
                " " +
                props.dataRegByID.rData?.apprInf[0].ApproLastName
            );
            setApproJobName(props.dataRegByID.rData?.apprInf[0].ApproJobName);
            setComment(props.dataRegByID.rData?.apprInf[0].Comment);
          }
        } else {
          console.log(props.dataRegByID.rData?.apprInf[0]);
          setShowstream(true);
          if (props.dataRegByID.rData?.aStatus === 2) {
            setShowstream1("Đã duyệt");
          }
          if (props.dataRegByID.rData?.aStatus === 3) {
            setShowstream1("Từ Chối");
          }
          if (props.dataRegByID.rData?.aStatus === 2) {
            setShowstream1("Nhân sự");
          }
          if (props.dataRegByID.rData?.aStatus === 2) {
            setShowstream1("Giám đốc");
          }
          setApprovalDate(
            moment(props.dataRegByID.rData?.apprInf[0]?.ApprovalDate).format(
              "DD-MM-YYYY"
            )
          );
          setApproName(
            props.dataRegByID.rData?.apprInf[0].ApproFirstName +
              " " +
              props.dataRegByID.rData?.apprInf[0].ApproLastName
          );
          setApproJobName(props.dataRegByID.rData?.apprInf[0].ApproJobName);
          setComment(props.dataRegByID.rData?.apprInf[0].Comment);
        }
      }

      let dataTypeOff = await getData("dayOffType");
      setlistTypeOff(dataTypeOff.rData);
      setIsLoading(false);
    })(show);
  }, [props, props.dataRegByID, props.isShow]);
  const aStatusShow = (aStatus) => {
    if (aStatus === 1) {
      return "Chờ Duyệt";
    }
    if (aStatus === 3) {
      return "Từ Chối";
    }
    if (aStatus === 2) {
      return "Đã Duyệt";
    }
  };
  const checkType = (id) => {
    const result = listTypeOff.find(({ OffTypeID }) => OffTypeID === id);
    let a = result?.Name + "(" + result?.Note + ")";
    return a;
  };
  const handleRefuse = async (data) => {
    console.log(regID);
    console.log("1");
    var create = await postData("approve", {
      regid: regID,
      comment: data.comment,
      state: 0,
    });
    if (create.isSuccess === 1) {
      console.log("từ chối");
      props.fetchData();
      props.hideModal();
    }
  };
  const handleApprove = async (data) => {
    var create = await postData("approve", {
      regid: regID,
      comment: data.comment,
      state: 1,
    });
    if (create.isSuccess === 1) {
      console.log("Duyệt");
      props.fetchData();
      props.hideModal();
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
              <div>
                <h2 className="p-2 d-flex justify-content-center position-relative">
                  {Showstream === true && (
                    <span style={{ position: "absolute ", left: "0" }}>
                      <h5 style={{ fontSize: "15px" }}>{Showstream1}</h5>
                    </span>
                  )}
                  <span>THÔNG TIN ĐƠN NGHỈ PHÉP</span>
                </h2>
              </div>

              <div className="row mt-3">
                <div className="col-md-6 d-flex">
                  MSNV
                  <p style={{ color: "red", minWidth: "74px" }}>(*)</p>
                  <input
                    value={MSNV}
                    className="form-control ml-3 "
                    readOnly
                    style={{ maxWidth: "200px" }}
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Đ.Vị/B.Phận</span>
                  <input
                    className="form-control ml-3"
                    value={departmentName}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>Họ và tên</span>
                  <input value={name} readOnly className="form-control ml-3 " />
                </div>
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}> Chức Vụ</span>
                  <input
                    className="form-control ml-3"
                    value={jPLevelName}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>Ngày vào Làm</span>
                  <input
                    readOnly
                    className="form-control ml-3 "
                    value={comeDate}
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
                  <input
                    className="form-control ml-3"
                    value={checkType(type)}
                    readOnly
                  />
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span style={{ minWidth: "120px" }}>Số phép năm hiện có</span>
                  <input
                    className="form-control ml-3 "
                    value={annualLeave}
                    readOnly
                    style={{ maxWidth: "80px" }}
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span style={{ minWidth: "120px" }}>
                    Bắt đầu nghỉ từ <span style={{ color: "red" }}>*</span>
                  </span>
                  <input
                    className="form-control ml-3"
                    value={RegDate}
                    readOnly
                  />
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span style={{ minWidth: "120px" }}>
                    Số Ngày Nghỉ <span style={{ color: "red" }}>*</span>
                  </span>
                  <div className="w-100 ml-3" style={{ maxWidth: "120px" }}>
                    <input
                      type="text"
                      className="form-control "
                      value={Period}
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
                    className="form-control ml-3 "
                    value={Reason}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span style={{ minWidth: "120px" }}>
                    Địa chỉ nghỉ phép<span style={{ color: "red" }}>*</span>
                  </span>
                  <textarea
                    type="text"
                    className="form-control ml-3 "
                    value={Address}
                    readOnly
                  />
                </div>
              </div>
              <div className="card mt-2 p-2 border border-warning ">
                <h5 className=" mt-1" style={{ textAlign: "center " }}>
                  Ý KIẾN NGƯỜI PHÊ DUYỆT
                </h5>
                <div className="row mt-2">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>Trạng Thái</span>
                    <input
                      readOnly
                      className="form-control ml-3 "
                      value={aStatus}
                    />
                  </div>
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}> Ngày Duyệt</span>
                    <input
                      className="form-control ml-3"
                      value={approvalDate}
                      readOnly
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}>Người Duyệt</span>
                    <input
                      readOnly
                      className="form-control ml-3 "
                      value={approName}
                    />
                  </div>
                  <div className="col-md-6 d-flex">
                    <span style={{ minWidth: "120px" }}> Chức vụ</span>
                    <input
                      className="form-control ml-3"
                      value={approJobName}
                      readOnly
                    />
                  </div>
                </div>
                <div className="row mt-2">
                  <div className="col-md-12 d-flex">
                    <span style={{ minWidth: "120px" }}>
                      Ý Kiến<span style={{ color: "red" }}>*</span>
                    </span>
                    <textarea
                      type="text"
                      className="form-control ml-3 "
                      {...register("comment")}
                      id="comment"
                      readOnly={show}
                      onChange={(e) => {
                        setComment(e.target.value);
                      }}
                      value={comment}
                    />
                  </div>
                </div>
              </div>
              {props.isAppove === true && (
                <div className="mt-3 d-flex justify-content-end">
                  <button
                    className="btn btn  btn-success border border-light mr-3 "
                    type="submit"
                    onClick={handleSubmit(handleApprove)}
                  >
                    Phê Duyệt
                  </button>
                  <button
                    className="btn btn  btn-danger border border-light mr-5"
                    type="submit"
                    onClick={handleSubmit(handleRefuse)}
                  >
                    Từ Chối
                  </button>
                </div>
              )}

              {/* end */}
            </div>
          )}
        </div>
      </section>
    </form>
  );
};
export default Approve;
