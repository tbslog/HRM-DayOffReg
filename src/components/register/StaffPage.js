import React, { useState, useEffect, useRef } from "react";
import DataTable from "react-data-table-component";
import { getData, putDataCus } from "../../services/user.service";
import moment from "moment";

import { Modal } from "bootstrap";
import Cookies from "js-cookie";
import { toast } from "react-toastify";

import Edit from "./Edit";
import Approve from "./Approve";
import Loading from "../common/loading/Loading";

let info = Cookies.get("info") && JSON?.parse(Cookies.get("info")); // kiểm tra đk 1 nếu có chạy câu lệnh sau
let emID = Cookies.get("empid");
const StaffPage = (props) => {
  const [dbTable, setdbTable] = useState([]);
  const [IsLoading, setIsLoading] = useState(false);

  const [ftTable, setftTable] = useState([]);

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
  const [callback, setcallback] = useState(false);
  const [listNV, setlistNV] = useState([]);

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData("day-off-letters?needAppr=0");
      //console.log(data);
      setdbTable(data.rData);
      setftTable(data.rData);
      let dataTypeOff = await getData("dayOffType");
      setlistTypeOff(dataTypeOff.rData);
      setIsLoading(false);
      let dataMana = await getData(
        "day-off-letters?needAppr=1&astatus=1%2C2%2C3%2C4%2C5"
      );
      //console.log(dataMana);

      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(false);

      setdbEmpid(emID);
      setdbFullName(info?.LastName + "" + info?.FirstName);

      let listlowergradedata = await getData("list-of-subordinates");
      let lista = listlowergradedata.rData?.map(
        ({ EmpID, FirstName, LastName }) => ({
          EmpID,
          Name: `${LastName} ${FirstName}`,
        })
      );
      lista?.unshift({
        EmpID: emID,
        Name: info.LastName + "" + info.FirstName,
      });

      setlistNV(lista);
      setIsLoading(false);
    })();
  }, [callback]);
  const col = [
    {
      name: "MSNV",
      selector: (row) => row.EmpID,
      sortable: true,
    },
    {
      name: "Họ tên",
      selector: (row) => row.LastName + " " + row.FirstName,
      sortable: true,
    },

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
      conditionalCellStyles: [
        {
          when: (row) => 0 === 0,
          classNames: ["d-flex justify-content-center"],
        },
      ],
    },
  ];
  const aStatusShow = (aStatus) => {
    if (aStatus === 0) {
      return <span> Chưa Gửi</span>;
    }
    if (aStatus === 1) {
      return <span style={{ color: "#ffc107" }}> Chờ Duyệt</span>;
    }
    if (aStatus === 3) {
      return <span style={{ color: "#dc3545" }}> Từ Chối</span>;
    }
    if (aStatus === 2) {
      return <span style={{ color: "#0d6efd" }}> Đã Duyệt</span>;
    }
    if (aStatus === 4) {
      return <span style={{ color: "rgb(157 157 157)" }}> Đã Hủy</span>;
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
    if (aStatus === 1) {
      return (
        <>
          <div style={{ minWidth: "85px" }}>
            <button
              className="border border-light btn btn-warning "
              style={{ width: "40px", height: "40px" }}
              onClick={() => handleReturn(id)}
            >
              <i
                className=" fas fa-undo-alt"
                title="Duyệt"
                style={{ color: "#ffffff" }}
              />
            </button>

            <button
              className="border border-light btn btn-info"
              type="button"
              data-toggle="modal"
              data-target="#exampleModalCenter"
              style={{ width: "40px", height: "40px" }}
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
          </div>
        </>
      );
    }

    return (
      <div>
        <button
          className="border border-light btn btn-info"
          type="button"
          data-toggle="modal"
          data-target="#exampleModalCenter"
          style={{ width: "40px", height: "40px" }}
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
      </div>
    );
  };
  const handleInfo = async (id) => {
    showModalForm();
    let dataReg = await getData(`day-off-letter?regid=${id}`);
    setDataRegByID(dataReg);
  };

  const handleReturn = async (id) => {
    let res = await putDataCus(`recall?regID=${id}`);

    if (res.isSuccess === 1) {
      toast.success(res.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setcallback(!callback);
    } else {
      toast.error(res.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
    }
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
    setcallback(!callback);
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
        <div className="card-header py-0 border-0"></div>

        <div
          className="card-body m-0 p-0 "
          style={{ height: props.sizeConten }}
        >
          {IsLoading ? (
            <Loading />
          ) : (
            <DataTable
              columns={col}
              data={ftTable}
              pagination
              paginationRowsPerPageOptions={[25, 50, 100]}
              fixedHeader
              fixedHeaderScrollHeight={props.sizeContenTB}
              highlightOnHover
              noDataComponent="Không có dữ liệu"
              subHeader
              subHeaderComponent={
                <div
                  className="d-flex justify-content-between w-100 p-0 m-0"
                  // style={{
                  //   background: "rgb(224 224 224)",
                  // }}
                >
                  <div className="dropdown show pt-1">
                    <select
                      className=" btn btn-sm btn-outline-light dropdown-toggle text-left "
                      onClick={(e) => {
                        let a = [];
                        if (parseInt(e.target.value) === 10) {
                          setftTable(dbTable);
                        } else {
                          a = dbTable.filter((element) => {
                            return element.EmpID === parseInt(e.target.value);
                          });
                          setftTable(a);
                        }

                        // handleOpption(e.target.value);
                      }}
                    >
                      <option value="10">Tất cả đơn</option>
                      {listNV &&
                        listNV.map((val) => {
                          return (
                            <option value={val.EmpID} key={val.EmpID}>
                              {val.EmpID}({val.Name})
                            </option>
                          );
                        })}
                    </select>
                  </div>
                  <div className="pt-1 ">
                    {/* style={{ alignSelf: "end" }} */}
                    <a
                      href="/Register"
                      className="btn btn-sm btn-success mr-3 mb-2"
                    >
                      <i className="fas fa-plus" /> Tạo Đơn
                    </a>
                  </div>
                </div>
              }
            />
          )}
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
                  style={{ marginRight: "1px" }}
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
