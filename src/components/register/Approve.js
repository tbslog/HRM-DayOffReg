import Popup from "../common/Popup";
import moment from "moment";
import { getData, postData } from "../../services/user.service";
import React, { useState, useEffect, useCallback } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import Loading from "../common/loading/Loading";
import { useForm, Controller } from "react-hook-form";
import { toast } from "react-toastify";
import "./style.css";

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
  const [Showstreamx, setShowstreamx] = useState(false);
  const [bg, setbg] = useState("#e9ecef");

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
      //console.log(props.dataRegByID.rData);

      setregID(props.dataRegByID.rData.regID);
      setMSNV(props.dataRegByID.rData.EmpID);
      setname(
        props.dataRegByID.rData.LastName +
          " " +
          props.dataRegByID.rData.FirstName
      );
      setDepartmentName(props.dataRegByID.rData.departmentName);
      setJobpositionName(props.dataRegByID.rData.JobPositionName);
      setAnnualLeave(props.dataRegByID.rData.AnnualLeave);
      setcomeDate(
        moment(props.dataRegByID.rData.comedate).format("DD-MM-YYYY")
      );
      setJPLevelName(props.dataRegByID.rData.Position);
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

        //console.log("first");
      }

      if (props.dataRegByID.rData?.aStatus === 1 && props.isAppove === true) {
        setApprovalDate(moment(new Date()).format("DD-MM-YYYY"));
        setApproName(info.FirstName + " " + info.LastName);
        setApproJobName(info.JobpositionName);
        setComment("");
        setshow(false);
        setShowstreamx(false);
        setShowstream(false);
        setbg("white");
        console.log("first1");
      } else {
        setbg("#e9ecef");
        if (props.isme === true) {
          if (props.dataRegByID.rData?.aStatus == 1) {
            setApprovalDate("");
            setApproName("");
            setApproJobName("");
            setComment("");
            console.log("2");
            setShowstream(false);
            setShowstreamx(true);
            Trangtt(props);
            console.log(props.dataRegByID.rData);
          } else {
            console.log(props.dataRegByID.rData?.apprInf[0]);
            setShowstream(true);
            setShowstreamx(true);
            Trangtt(props);
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
          //console.log(props.dataRegByID.rData);
          setShowstream(true);
          setShowstreamx(true);
          Trangtt(props);
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
  const validateForm = {
    comment: {
      required: "Kh??ng ???????c ????? tr???ng",
    },
  };
  const Trangtt = (props) => {
    if (props.dataRegByID.rData?.aStatus === 1) {
      setShowstream1("Ch??? Duy???t");
    }
    if (props.dataRegByID.rData?.aStatus === 2) {
      setShowstream1("???? duy???t");
    }
    if (props.dataRegByID.rData?.aStatus === 3) {
      setShowstream1("T??? Ch???i");
    }
    if (props.dataRegByID.rData?.aStatus === 4) {
      setShowstream1("???? ti???p nh???n");
    }
    if (props.dataRegByID.rData?.aStatus === 5) {
      setShowstream1("???? ki???m so??t");
    }
  };

  function ListItem(props) {
    const listItems = props.dataRegByID.rData?.apprInf;
    console.log(listItems);
    return (
      <>
        {listItems?.map((item) => (
          <div className="pt-3">
            <div className="row mt-2">
              <div className="col-md-6 d-flex">
                <span style={{ minWidth: "120px" }}>Tr???ng Th??i</span>
                <input
                  readOnly
                  className="form-controlCustomer ml-3 "
                  value={item.StateName}
                />
              </div>
              <div className="col-md-6 d-flex">
                <span style={{ minWidth: "120px" }}> Ng??y Duy???t</span>
                <input
                  className="form-control ml-3"
                  value={moment(item.ApprovalDate).format("DD-MM-YYYY")}
                  readOnly
                />
              </div>
            </div>
            <div className="row mt-2">
              <div className="col-md-6 d-flex">
                <span style={{ minWidth: "120px" }}>Ng?????i Duy???t</span>
                <input
                  readOnly
                  className="form-control ml-3 "
                  value={item.ApproLastName + " " + item.ApproFirstName}
                />
              </div>
              <div className="col-md-6 d-flex">
                <span style={{ minWidth: "120px" }}> Ch???c v???</span>
                <input
                  className="form-control ml-3"
                  value={item.ApproJobName}
                  readOnly
                />
              </div>
            </div>
            <div className="row mt-2">
              <div className="col-md-12 d-flex">
                <span style={{ minWidth: "120px" }}>
                  ?? Ki???n<span style={{ color: "red" }}>*</span>
                </span>
                <textarea
                  type="text"
                  className="form-control ml-3 "
                  readOnly
                  value={item.Comment}
                />
              </div>
            </div>
          </div>
        ))}
      </>
    );
  }
  const aStatusShow = (aStatus) => {
    if (aStatus === 1) {
      return "Ch??? Duy???t";
    }
    if (aStatus === 3) {
      return "T??? Ch???i";
    }
    if (aStatus === 2) {
      return "???? Duy???t";
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
    reset();
    if (create.isSuccess === 1) {
      setIsLoading(true);
      toast.warn(" ???? t??? ch???i\n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      console.log("t??? ch???i");
      setComment("");
      props.fetchData();
      props.hideModal();
    }
  };
  const handleApprove = async (data) => {
    setIsLoading(true);
    var create = await postData("approve", {
      regid: regID,
      comment: data.comment,
      state: 1,
    });
    if (create.isSuccess === 1) {
      toast.success("Duy???t th??nh c??ng \n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      console.log("Duy???t");
      props.fetchData();
      props.hideModal();
    }
  };
  return (
    <form>
      <section className="content" style={{}}>
        {/* Default box */}

        <div
          className="card  "
          style={{ maxHeight: "100vh", minHeight: "80vh" }}
        >
          {IsLoading ? (
            <Loading />
          ) : (
            <div className="card-header py-0 border-0">
              <div>
                <h2
                  className=" d-flex justify-content-center position-relative pb-1"
                  style={{ background: "rgb(224 224 224)", fontSize: "20px" }}
                >
                  <span>TH??NG TIN ????N NGH??? PH??P</span>
                </h2>
                {Showstreamx === true && (
                  <span style={{ position: "absolute ", right: "30px" }}>
                    <h5 style={{ fontSize: "15px" }}>
                      Tr???ng Th??i : {Showstream1}
                    </h5>
                  </span>
                )}
              </div>

              <div className="row mt-3 pt-3">
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    MSNV <span style={{ color: "red" }}>*</span>
                  </span>
                  <input
                    value={MSNV}
                    className="form-controlCustomer ml-3 "
                    readOnly
                    style={{ maxWidth: "200px" }}
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    {" "}
                    ??.V???/B.Ph???n
                  </span>
                  <input
                    className="form-controlCustomer ml-3"
                    value={departmentName}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    H??? v?? t??n
                  </span>
                  <input
                    value={name}
                    readOnly
                    className="form-controlCustomer ml-3 "
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    {" "}
                    Ch???c V???
                  </span>
                  <input
                    className="form-controlCustomer ml-3"
                    value={jPLevelName}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    Ng??y v??o L??m
                  </span>
                  <input
                    readOnly
                    className="form-controlCustomer ml-3 "
                    value={comeDate}
                  />
                </div>
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    {" "}
                    V??? tr?? CV
                  </span>
                  <input
                    className="form-controlCustomer ml-3"
                    value={jobpositionName}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    Lo???i Ph??p <span style={{ color: "red" }}>*</span>
                  </span>
                  <input
                    className="form-controlCustomer ml-3"
                    value={checkType(type)}
                    readOnly
                  />
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    S??? ph??p n??m hi???n c??
                  </span>
                  <input
                    className="form-controlCustomer ml-3 "
                    value={annualLeave}
                    readOnly
                    style={{ maxWidth: "80px" }}
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-6 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    B???t ?????u ngh??? t??? <span style={{ color: "red" }}>*</span>
                  </span>
                  <input
                    className="form-controlCustomer ml-3"
                    value={RegDate}
                    readOnly
                  />
                </div>
                <div className="col-md-6 d-flex justify-content-between">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    S??? Ng??y Ngh??? <span style={{ color: "red" }}>*</span>
                  </span>
                  <div className="w-100 ml-3" style={{ maxWidth: "120px" }}>
                    <input
                      type="text"
                      className="form-controlCustomer "
                      value={Period}
                      readOnly
                    />
                  </div>
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    L?? do ngh??? ph??p<span style={{ color: "red" }}>*</span>
                  </span>
                  <textarea
                    className="form-controlCustomer ml-3 "
                    value={Reason}
                    readOnly
                  />
                </div>
              </div>
              <div className="row mt-2">
                <div className="col-md-12 d-flex">
                  <span className="spancustomer" style={{ minWidth: "120px" }}>
                    ?????a ch??? ngh??? ph??p<span style={{ color: "red" }}>*</span>
                  </span>
                  <textarea
                    type="text"
                    className="form-controlCustomer ml-3 "
                    value={Address}
                    readOnly
                  />
                </div>
              </div>
              <div className="card mt-2 p-2 border border-warning ">
                <h5 className=" mt-1" style={{ textAlign: "center " }}>
                  ?? KI???N NG?????I PH?? DUY???T
                </h5>
                {Showstream ? (
                  ListItem(props)
                ) : (
                  <>
                    <div className="row mt-2">
                      <div className="col-md-6 d-flex">
                        <span style={{ minWidth: "120px" }}>Tr???ng Th??i</span>
                        <input
                          readOnly
                          className="form-controlCustomer ml-3 "
                          value={aStatus}
                        />
                      </div>
                      <div className="col-md-6 d-flex">
                        <span style={{ minWidth: "120px" }}> Ng??y Duy???t</span>
                        <input
                          className="form-controlCustomer ml-3"
                          value={approvalDate}
                          readOnly
                        />
                      </div>
                    </div>
                    <div className="row mt-2">
                      <div className="col-md-6 d-flex">
                        <span style={{ minWidth: "120px" }}>Ng?????i Duy???t</span>
                        <input
                          readOnly
                          className="form-controlCustomer ml-3 "
                          value={approName}
                        />
                      </div>
                      <div className="col-md-6 d-flex">
                        <span style={{ minWidth: "120px" }}> Ch???c v???</span>
                        <input
                          className="form-controlCustomer ml-3"
                          value={approJobName}
                          readOnly
                        />
                      </div>
                    </div>
                    <div className="row mt-2">
                      <div className="col-md-12 d-flex">
                        <span style={{ minWidth: "120px" }}>
                          ?? Ki???n<span style={{ color: "red" }}>*</span>
                        </span>
                        <textarea
                          type="text"
                          className="form-controlCustomer ml-3 "
                          {...register("comment", validateForm.comment)}
                          style={{ backgroundColor: bg }}
                          id="comment"
                          readOnly={show}
                          onChange={(e) => {
                            setComment(e.target.value);
                          }}
                          value={comment}
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
                        {errors.comment?.message}
                      </span>
                    </div>
                  </>
                )}
              </div>
              {/* end */}
              {props.isAppove === true && (
                <div className="mt-3 d-flex justify-content-end">
                  <button
                    className="btn btn  btn-success border border-light mr-3 "
                    type="submit"
                    onClick={handleSubmit(handleApprove)}
                  >
                    Ph?? Duy???t
                  </button>
                  <button
                    className="btn btn  btn-danger border border-light mr-5"
                    type="submit"
                    onClick={handleSubmit(handleRefuse)}
                  >
                    T??? Ch???i
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
