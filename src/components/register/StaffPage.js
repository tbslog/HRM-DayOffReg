import React, { useState, useEffect, useRef } from "react";
import DataTable from "react-data-table-component";
import { getData, getDataCustom } from "../../services/user.service";
import moment from "moment";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import { Modal } from "bootstrap";

import Edit from "./Edit";
import Approve from "./Approve";

const StaffPage = (props) => {
  const [dbTable, setdbTable] = useState([]);
  const [dbTableMana, setdbTableMana] = useState([]);
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [fullName, setdbFullName] = useState([]);
  const [empid, setdbEmpid] = useState([]);
  const [regID, setregID] = useState("");
  const [dataRegByID, setDataRegByID] = useState({});

  const [open, setOpen] = useState(false);
  const [onPop, setOn] = useState(false);
  const [isAppove, setisAppove] = useState(false);
  const [isInfo, setisInfo] = useState(false);
  const [isShow, setisShow] = useState(true);
  const [isme, setisme] = useState(false);

  const [ShowModal, SetShowModal] = useState("");
  const [modal, setModal] = useState(null);
  const parseExceptionModal = useRef();

  useEffect(() => {
    (async () => {
      let data = await getDataCustom("day-off-letters", {
        needAppr: 0,
        astatus: [],
      });
      setdbTable(data.rData);

      let dataMana = await getDataCustom("day-off-letters", {
        needAppr: 1,
        astatus: [],
      });
      // console.log(dataMana);

      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(false);
      // console.log(data.rData[0].EmpID);
      setdbEmpid(data.rData[0].EmpID);
      setdbFullName(data.rData[0].FirstName + "" + data.rData[0].LastName);

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
      return <i className="fas fa-long-arrow-alt-right" title="Chờ Duyệt" />;
    }
    if (aStatus === 3) {
      return <i className="fas fa-times" title="Từ Chối" />;
    }
    if (aStatus === 2) {
      return <i className="fas fa-check-circle" title="Đã Duyệt" />;
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
          className="btn btn-primary ml-1"
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
    console.log(dataReg);
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
    let data = await getDataCustom("day-off-letters", {
      needAppr: 0,
      astatus: [],
    });
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
            className="row p-3 "
            style={{
              justifyContent: "space-between ",
            }}
          >
            <div style={{ alignSelf: "end" }}>
              {empid}||{fullName}
            </div>
            <div>
              <h3>ĐƠN NGHỈ PHÉP CỦA TÔI</h3>
            </div>
            <div style={{ alignSelf: "end" }}>
              <a href="/Register" className="btn btn-sm btn-success">
                <i className="fas fa-plus" /> Tạo đơn
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
            fixedHeader
            fixedHeaderScrollHeight={props.sizeContenTB}
            selectableRows
            selectableRowsHighlight
            highlightOnHover
            subHeader
            subHeaderComponent={<input type="text" placeholder="Search" />}
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
