import React, { useState, useEffect, useRef } from "react";
import DataTable from "react-data-table-component";
import { getData, postData, getDataCustom } from "../../services/user.service";
import moment from "moment";
import Approve from "./Approve";
import { Modal } from "bootstrap";

const ManagerPage = (props) => {
  const [dbTableMana, setdbTableMana] = useState([]);
  const [ftTableMana, setftTableMana] = useState([]);
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [onPop, setOn] = useState(false);
  const [dataRegByID, setDataRegByID] = useState({});
  const [IdEM, setIdEM] = useState("");
  const [isAppove, setisAppove] = useState(true);
  const [isShow, setisShow] = useState(true);

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

  const fetchData = async () => {
    let dataMana = await getDataCustom("day-off-letters", {
      needAppr: 1,
      astatus: [0, 1, 2, 3, 4, 5],
    });
    setdbTableMana(dataMana.rData);
    setftTableMana(dataMana.rData);
  };

  useEffect(() => {
    (async () => {
      let dataMana = await getDataCustom("day-off-letters", {
        needAppr: 1,
        astatus: [0, 1, 2, 3, 4, 5],
      });
      // console.log(dataMana);

      setdbTableMana(dataMana.rData);
      setftTableMana(dataMana.rData);
      let dataTypeOff = await getData("dayOffType");
      // console.log(dataTypeOff);
      setlistTypeOff(dataTypeOff.rData);
    })();
  }, []);
  const col = [
    {
      selector: (row) => row.DeptID,
      minWidth: "60px",
      maxWidth: "70px",
      sortable: true,
    },
    {
      name: "Mã NV",
      selector: (row) => row.EmpID,
      width: "96px",
      sortable: true,
    },
    {
      name: "Họ tên NV",
      selector: (row) => (
        <div>
          {row.FirstName} {row.LastName}
        </div>
      ),
      width: "150px",
      sortable: true,
    },
    {
      name: "Ngày gửi",
      selector: (row) => moment(row.RegDate).format("DD-MM-YYYY"),
      sortable: true,
    },
    {
      name: "Ngày Nghỉ",
      selector: (row) => moment(row.StartDate).format("DD-MM-YYYY"),
      sortable: true,
    },
    {
      name: "Số Ngày",
      selector: (row) => row.Period,
      minWidth: "90px",
      maxWidth: "92px",
      sortable: true,
    },
    {
      name: "Loại Phép",
      selector: (row) => checkTypeOff(row.Type),
      sortable: true,
      width: "120px",
    },
    {
      name: "",
      cell: (row) => aStatusShow(row.aStatus, row.regID),

      conditionalCellStyles: [
        {
          when: (row) => row.aStatus != 0,
          classNames: ["d-flex justify-content-center"],
        },
      ],
    },
  ];
  const checkTypeOff = (id) => {
    let a = listTypeOff?.find((data) => data.OffTypeID === id);
    return a?.Name + "(" + a?.Note + ")";
  };
  const aStatusShow = (aStatus, regid) => {
    if (aStatus === 1) {
      return (
        <div>
          <button
            className="border border-light btn btn-primary "
            style={{ width: "40px", height: "40px" }}
            onClick={() => handleApprove(regid)}
          >
            <i className=" fas fa-check-circle" title="Duyệt" />
          </button>

          <button
            className="border border-light btn btn-info"
            type="button"
            data-toggle="modal"
            data-target="#exampleModalCenter"
            style={{ width: "40px", height: "40px" }}
            onClick={() =>
              handleInfoApprove(
                regid,
                SetShowModal("Info"),
                setisAppove(true),
                setisShow(false)
              )
            }
          >
            <i className="fas fa-info-circle" title="Thông tin"></i>
          </button>
        </div>
      );
    }
    if (aStatus === 3) {
      return (
        <div
          className="border border-light btn btn-danger "
          style={{ width: "40px", height: "40px" }}
          onClick={() =>
            handleInfoApprove(
              regid,
              SetShowModal("Info"),
              setisAppove(false),
              setisShow(true)
            )
          }
        >
          <i className=" fas fa-times" title="Đã Từ Chối" />
        </div>
      );
    }
    if (aStatus === 2 || aStatus === 4 || aStatus == 5) {
      return (
        <>
          <div
            className="border border-light btn btn-success"
            style={{ width: "40px", height: "40px" }}
            onClick={() =>
              handleInfoApprove(
                regid,
                SetShowModal("Info"),
                setisAppove(false),
                setisShow(true)
              )
            }
          >
            <i className="  fas fa-check-circle" title="Đã Duyệt" />
          </div>
        </>
      );
    }
  };

  const handleApprove = async (id) => {
    console.log(id);
    var create = await postData("approve", {
      regid: id,
      comment: "",
      state: 1,
    });
    if (create.isSuccess === 1) {
      console.log("Duyệt");
    }
  };

  const handleInfoApprove = async (id) => {
    showModalForm();
    let dataReg = await getData(`day-off-letter?regid=${id}`);
    //console.log(dataReg);
    setDataRegByID(dataReg);
    setIdEM(dataReg.rData.EmpID);
  };
  const handleOpption = async (id) => {
    console.log(id);
  };

  return (
    <>
      <form>
        <div className="card-header py-0 border-0">
          <div
            className="row m-3 "
            style={{
              justifyContent: "center ",
            }}
          >
            <h3>DANH SÁCH ĐƠN NGHỈ PHÉP</h3>
          </div>
        </div>
        <div
          className="card-body m-0 p-0 "
          style={{ height: props.sizeConten }}
        >
          <DataTable
            columns={col}
            data={ftTableMana}
            pagination
            fixedHeader
            fixedHeaderScrollHeight={props.sizeContenTB}
            selectableRows
            selectableRowsHighlight
            highlightOnHover
            subHeader
            subHeaderComponent={
              <div className="d-flex justify-content-between w-100">
                <div className="dropdown show">
                  <select
                    className="form-control btn btn-secondary dropdown-toggle text-left"
                    onClick={(e) => {
                      let a = [];
                      if (parseInt(e.target.value) === 10) {
                        setftTableMana(dbTableMana);
                      } else {
                        a = dbTableMana.filter((element) => {
                          return element.aStatus === parseInt(e.target.value);
                        });
                        setftTableMana(a);
                      }

                      // handleOpption(e.target.value);
                    }}
                  >
                    <option value="10">Tất cả đơn</option>
                    <option value="1">Chờ Duyệt</option>
                    <option value="2">Đã Duyệt</option>
                    <option value="3">Từ Chối</option>
                  </select>
                </div>
                <input type="text" placeholder="Search"></input>
              </div>
            }
          />
        </div>
      </form>
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
                  <span aria-hidden="true" style={{ fontSize: "30px" }}>
                    ×
                  </span>
                </button>
              </div>
              <div className="modal-body pt-0">
                <>
                  {ShowModal === "Info" && (
                    <Approve
                      dataRegByID={dataRegByID}
                      isAppove={isAppove}
                      isShow={isShow}
                      fetchData={fetchData}
                      hideModal={hideModal}
                    />
                  )}
                </>
              </div>
            </div>
          </div>
        </div>
      </>
    </>
  );
};

export default ManagerPage;
