import React, { useState, useEffect, useRef } from "react";
import DataTable from "react-data-table-component";
import { getData } from "../../services/user.service";
import moment from "moment";

import { Modal } from "bootstrap";
import Cookies from "js-cookie";

import Edit from "./Edit";
import Approve from "./Approve";

let info = Cookies.get("info") && JSON?.parse(Cookies.get("info")); // kiểm tra đk 1 nếu có chạy câu lệnh sau
let emID = Cookies.get("empid");
const StaffPage = (props) => {
  const [dbTable, setdbTable] = useState([]);

  const [listTypeOff, setlistTypeOff] = useState([]);
  const [fullName, setdbFullName] = useState([]);
  const [empid, setdbEmpid] = useState([]);

  const [dataRegByID, setDataRegByID] = useState({});

  const [open, setOpen] = useState(false);

  const [isAppove, setisAppove] = useState(false);

  const [isShow, setisShow] = useState(true);
  const [isme, setisme] = useState(false);

  const [ShowModal, SetShowModal] = useState("");
  const [modal, setModal] = useState(null);
  const parseExceptionModal = useRef();

  useEffect(() => {
    (async () => {
      let data = await getData("day-off-letters?needAppr=0");
      setdbTable(data.rData);

      let dataMana = await getData(
        "day-off-letters?needAppr=1&astatus=1%2C2%2C3%2C4%2C5"
      );
      //console.log(dataMana);

      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(false);

      setdbEmpid(emID);
      setdbFullName(info?.LastName + "" + info?.FirstName);

      let dataTypeOff = await getData("dayOffType");
      setlistTypeOff(dataTypeOff.rData);
    })();
  }, []);
  const col = [
    {
      name: "Ngày gửi",
      selector: (row) => checkRegDate(row.RegDate),
      sortable: true,
    },
    {
      name: "Ngày Bắt đầu Nghỉ",
      selector: (row) => moment(row.StartDate).format("DD-MM-YYYY"),
      sortable: true,
    },
    {
      name: "Số Ngày Nghỉ",
      selector: (row) => row.Period,
      sortable: true,
    },
    {
      name: "Loại Phép",
      selector: (row) => checkTypeOff(row.Type),
      sortable: true,
    },
    {
      name: "Trạng Thái",
      selector: (row) => aStatusShow(row.aStatus),
      sortable: true,
    },
    {
      name: "Action",
      cell: (row) => actionEdit(row.aStatus, row.regID),
    },
  ];
  const aStatusShow = (aStatus) => {
    if (aStatus === 1) {
      return (
        <i
          className="fas fa-long-arrow-alt-right  "
          style={{ fontSize: "20px", color: "#ffc107" }}
          title="Chờ Duyệt"
        />
      );
    }
    if (aStatus === 3) {
      return (
        <i
          className="fas fa-times"
          style={{ fontSize: "20px", color: "#dc3545" }}
          title="Từ Chối"
        />
      );
    }
    if (aStatus === 2 || aStatus === 4 || aStatus === 5) {
      return (
        <i
          className="fas fa-check-circle"
          style={{ fontSize: "20px", color: "#0d6efd" }}
          title="Đã Duyệt"
        />
      );
    }
  };

  const actionEdit = (aStatus, id) => {
    if (aStatus === 0) {
      return (
        <>
          <button
            type="button"
            data-toggle="modal"
            data-target="#exampleModalCenter"
            className="btn btn-info"
            onClick={() => handleEditButtonClick(id, SetShowModal("Edit"))}
          >
            <i className="fas fa-edit " title="Chỉnh Sửa" />
          </button>
          {/* <button
            type="button"
            data-toggle="modal"
            data-target="#exampleModalCenter"
            className="btn btn-primary ml-1"
            onClick={() =>
              handleInfo(id, SetShowModal("Info"), setisShow(true))
            }
          >
            <i className="fas fa-info-circle" title="Thông tin"></i>
          </button> */}
        </>
      );
    }
    return (
      <>
        <button
          type="button"
          data-toggle="modal"
          data-target="#exampleModalCenter"
          className="btn btn-success ml-1"
          onClick={() =>
            handleInfo(
              id,
              SetShowModal("Info"),
              setisAppove(false),
              setisme(true)
            )
          }
        >
          <i className="fas fa-info-circle" title="Thông tin"></i>
        </button>
      </>
    );
  };
  const handleInfo = async (id) => {
    showModalForm();
    let dataReg = await getData(`day-off-letter?regid=${id}`);
    setDataRegByID(dataReg);
  };
  const handleEditButtonClick = async (id) => {
    showModalForm();
    let dataReg = await getData(`day-off-letter?regid=${id}`);
    setDataRegByID(dataReg);
  };
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
    let data = await getData("day-off-letters?needAppr=0");
    setdbTable(data.rData);
  };
  const checkRegDate = (regDate) => {
    if (regDate == null) {
      return <div style={{ color: "red" }}> Chưa Gửi</div>;
    } else return moment(regDate).format("DD-MM-YYYY");
  };
  const checkTypeOff = (id) => {
    let a = listTypeOff?.find((data) => data.OffTypeID === id);
    return a?.Name + "(" + a?.Note + ")";
  };
  return (
    <>
      <form>
        <div className="card-header py-0 border-0">
          <div
            className="row pt-1 "
            style={{
              justifyContent: "space-between ",
              // background: "rgb(224 224 224)",
            }}
          >
            <div className="pt-2 ml-2">
              {/* style={{ alignSelf: "end" }} */}
              {empid} || {fullName}
            </div>

            <div className="pt-1 ">
              {/* style={{ alignSelf: "end" }} */}
              <a href="/Register" className="btn btn-sm btn-success mr-3 mb-2">
                <i className="fas fa-plus" /> Tạo Đơn
              </a>
            </div>
          </div>
        </div>
        <div
          className="card-body m-0 p-0 "
          style={{ height: props.sizeConten }}
        >
          <DataTable
            columns={col}
            data={dbTable}
            pagination
            paginationRowsPerPageOptions={[25, 50, 100]}
            fixedHeader
            fixedHeaderScrollHeight={props.sizeContenTB}
            selectableRows
            selectableRowsHighlight
            highlightOnHover
            subHeader
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
                  <span aria-hidden="true">×</span>
                </button>
              </div>
              <div className="modal-body">
                <>
                  {ShowModal === "Edit" && (
                    <Edit
                      dataRegByID={dataRegByID}
                      listTypeOff1={listTypeOff}
                      fullName={fullName}
                      hideModal={hideModal}
                      fetchData={fetchData}
                    />
                  )}
                  {ShowModal === "Info" && (
                    <Approve
                      dataRegByID={dataRegByID}
                      isAppove={isAppove}
                      hideModal={hideModal}
                      isShow={isShow}
                      isme={isme}
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

export default StaffPage;
