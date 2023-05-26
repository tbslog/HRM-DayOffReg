import React, { useState, useEffect, useRef, useMemo } from "react";
import DataTable from "react-data-table-component";
import {
  getData,
  postData,
  putData,
  putDataCus,
} from "../../services/user.service";
import moment from "moment";
import Approve from "./Approve";
import { toast } from "react-toastify";
import { Modal } from "bootstrap";
import Loading from "../common/loading/Loading";

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

  const [filterText, setFilterText] = useState("");
  const [resetPaginationToggle, setResetPaginationToggle] = useState(false);
  const [callback, setcallback] = useState(false);
  const [IsLoading, setIsLoading] = useState(false);

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

  useEffect(() => {
    setIsLoading(true);
    setftTableMana(
      dbTableMana.filter(
        (item) =>
          (item.FirstName &&
            item.FirstName.toLowerCase().includes(filterText.toLowerCase())) ||
          (item.LastName &&
            item.LastName.toLowerCase().includes(filterText.toLowerCase()))
      )
    );
    setIsLoading(false);
  }, [filterText]);

  const handleClear = () => {
    // if (filterText) {
    setResetPaginationToggle(!resetPaginationToggle);
    setFilterText("");
    setftTableMana(dbTableMana);
    // }
  };
  // const Searchdatatable = useMemo(() => {

  //   return (
  //     <FilterComponent
  //       // filterText={filterText}
  //       onChange={(e) => setFilterText(e.target.value)}
  //       onClear={handleClear}
  //     />
  //   );
  // }, [filterText, resetPaginationToggle]);

  const fetchData = async () => {
    let dataMana = await getData(
      "day-off-letters?needAppr=1&astatus=1%2C2%2C3%2C4%2C5"
    );
    setdbTableMana(dataMana.rData);
    setftTableMana(dataMana.rData);
  };

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let dataMana = await getData(
        "day-off-letters?needAppr=1&astatus=1%2C2%2C3%2C4%2C5"
      );
      setdbTableMana(dataMana.rData);
      setftTableMana(dataMana.rData);
      let dataTypeOff = await getData("dayOffType");
      // console.log(dataTypeOff);
      setlistTypeOff(dataTypeOff.rData);
      setIsLoading(false);
    })();
  }, [callback]);
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
          {row.LastName} {row.FirstName}
        </div>
      ),
      width: "200px",
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
  const handleReturn = async (id) => {
    let res = await putDataCus(`recall-approved-leave?regid=${id}`);
    if (res.isSuccess === 1) {
      console.log("first");
      toast.success("Thu hồi đơn thành công \n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setcallback(!callback);
    } else if (res.isSuccess === 0) {
      toast.error(res.note, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
    }
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
    if (aStatus === 2) {
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
          <div
            className="border border-light btn btn-warning"
            style={{ width: "40px", height: "40px" }}
            onClick={() => handleReturn(regid)}
          >
            <i className="fas fa-undo" title="Thu hồi" />
          </div>
        </>
      );
    }
    if (aStatus === 4) {
      return (
        <>
          <div
            className="border border-light btn btn-danger"
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
            <i className="fas fa-undo" title="Đã Thu hồi" />
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
      toast.success("Duyệt thành công \n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
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
            className="row  d-flex justify-content-center position-relative pt-1 "
            style={{
              justifyContent: "center ",
              background: "rgb(224 224 224)",
            }}
          >
            <h3>DANH SÁCH ĐƠN NGHỈ PHÉP</h3>
          </div>
        </div>
        <div
          className="card-body m-0 p-0 "
          style={{ height: props.sizeConten }}
        >
          {IsLoading ? (
            <Loading />
          ) : (
            <DataTable
              columns={col}
              data={ftTableMana}
              pagination
              paginationRowsPerPageOptions={[25, 50, 100]}
              paginationResetDefaultPage={resetPaginationToggle}
              fixedHeader
              fixedHeaderScrollHeight={props.sizeContenTB}
              selectableRows
              selectableRowsHighlight
              noDataComponent="Không có dữ liệu"
              highlightOnHover
              persistTableHead
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
                      <option value="4">Đã Hủy</option>
                    </select>
                  </div>
                  <div className="input-group mb-2" style={{ width: "30%" }}>
                    <input
                      type="text"
                      id="search"
                      className="form-control"
                      placeholder="Search..."
                      aria-label="Search Input"
                      value={filterText}
                      onChange={(e) => setFilterText(e.target.value)}
                    />
                    <div className="input-group-append">
                      <button
                        className="btn btn-primary"
                        type="button"
                        onClick={handleClear}
                      >
                        <i className="fas fa-times"> </i>
                      </button>
                    </div>
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
