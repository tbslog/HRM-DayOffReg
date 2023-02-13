import React, { useState, useEffect } from "react";
import DataTable from "react-data-table-component";
import { getData } from "../../services/user.service";
import moment from "moment";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";

const ManagerPage = () => {
  const [dbTable, setdbTable] = useState([]);
  const [dbTableMana, setdbTableMana] = useState([]);
  const [listTypeOff, setlistTypeOff] = useState([]);
  const [fullName, setdbFullName] = useState([]);
  const [empid, setdbEmpid] = useState([]);
  const [open, setOpen] = useState(false);
  const [sizeConten, setsizeConten] = useState("568px");
  const [sizeContenTB, setsizeContenTB] = useState("450px");
  useEffect(() => {
    (async () => {
      let dataMana = await getData("day-off-letters?needAppr=1");
      console.log(dataMana.rData);
      if (dataMana.rData.length > 0) {
        setOpen(true);
        setsizeConten("500px");
        setsizeContenTB("420px");
      } else setOpen(false);
      setdbTableMana(dataMana.rData);
      let dataTypeOff = await getData("dayOffType");
      // console.log(dataTypeOff);
      setlistTypeOff(dataTypeOff);
    })();
  }, []);
  const col = [
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
      width: "100px",
      sortable: true,
    },
    {
      name: "Loại Phép",
      selector: (row) => checkTypeOff(row.Type),
      sortable: true,
    },
    {
      name: "",
      cell: (row) => aStatusShow(row.aStatus),

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
  const aStatusShow = (aStatus) => {
    if (aStatus === 1) {
      return (
        <div>
          <button
            className="border border-light btn btn-success "
            style={{ width: "40px", height: "40px" }}
          >
            <i className=" fas fa-check-circle" title="Duyệt" />
          </button>
          <button
            className="border border-light btn btn-danger"
            style={{ width: "40px", height: "40px" }}
          >
            <i className=" fas fa-times" title="Từ Chối" />
          </button>
        </div>
      );
    }
    if (aStatus === 3) {
      return (
        <div
          className="border border-light btn btn-danger "
          style={{ width: "40px", height: "40px" }}
        >
          <i className=" fas fa-times" title="Đã Từ Chối" />
        </div>
      );
    }
    if (aStatus === 2) {
      return (
        <div
          className="border border-light btn btn-success"
          style={{ width: "40px", height: "40px" }}
        >
          <i className="  fas fa-check-circle" title="Đã Duyệt" />
        </div>
      );
    }
  };
  return (
    <form>
      <div className="card-header py-0 border-0">
        <div
          className="row m-3 "
          style={{
            justifyContent: "center ",
          }}
        >
          <h3>Danh Sách Đơn Nghỉ Phép</h3>
        </div>
      </div>
      <div className="card-body m-0 p-0 " style={{ height: sizeConten }}>
        <DataTable
          columns={col}
          data={dbTableMana}
          pagination
          fixedHeader
          fixedHeaderScrollHeight={sizeContenTB}
          selectableRows
          selectableRowsHighlight
          highlightOnHover
          subHeader
          subHeaderComponent={
            <div className="d-flex justify-content-between w-100">
              <div class="dropdown show">
                <a
                  class="btn btn-secondary dropdown-toggle"
                  href="#"
                  role="button"
                  id="dropdownMenuLink"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  Tất cả đơn
                </a>

                <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                  <a class="dropdown-item" href="#">
                    Đơn Mới
                  </a>
                  <a class="dropdown-item" href="#">
                    Đã Phê Duyệt
                  </a>
                  <a class="dropdown-item" href="#">
                    Chưa Phê Duyệt
                  </a>
                </div>
              </div>
              <input type="text" placeholder="Search"></input>
            </div>
          }
        />
      </div>
    </form>
  );
};

export default ManagerPage;
