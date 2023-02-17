import React, { useState, useEffect } from "react";
import DataTable from "react-data-table-component";
import { getData } from "../services/user.service";
import moment from "moment";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";

const Demo1 = () => {
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
      let data = await getData("day-off-letters");
      let dataMana = await getData("day-off-letters?needAppr=1");
      console.log(dataMana.rData);
      if (dataMana.rData.length > 0) {
        setOpen(true);
        setsizeConten("500px");
        setsizeContenTB("420px");
      } else setOpen(false);

      setdbEmpid(data.rData[0].EmpID);
      setdbFullName(data.rData[0].FirstName + "" + data.rData[0].LastName);
      console.log(data.rData);
      setdbTable(data.rData);
      let dataTypeOff = await getData("dayOffType");
      // console.log(dataTypeOff);
      setlistTypeOff(dataTypeOff);
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
      cell: (row) => actionEdit(row.aStatus),
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
  const actionEdit = (aStatus) => {
    if (aStatus === 0) {
      return (
        <button className="btn btn-primary">
          <i className="fas fa-edit" />
        </button>
      );
    }
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
    <form>
      <div className="content-wrapper ">
        <section className="content">
          {/* Default box */}
          <div className="card ">
            <div className="card-header py-0 border-0">
              {open && (
                <ul class="nav nav-pills">
                  <li className="nav-item">
                    <a
                      className="nav-link active"
                      href="#activity"
                      data-toggle="tab"
                    >
                      Đơn Của Tôi
                    </a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#timeline" data-toggle="tab">
                      Đơn Cần Phê Duyệt
                    </a>
                  </li>
                </ul>
              )}

              <div
                className="row m-3 "
                style={{
                  justifyContent: "space-between ",
                }}
              >
                <div style={{ alignSelf: "end" }}>
                  {empid}||{fullName}
                </div>
                <div>
                  <h3>Danh Sách Đơn Nghỉ Phép</h3>
                </div>
                <div style={{ alignSelf: "end" }}>
                  <a href="" className="btn btn-sm btn-success">
                    <i className="fas fa-plus" /> Create New
                  </a>
                </div>
              </div>
            </div>
            <div className="card-body m-0 p-0 " style={{ height: sizeConten }}>
              <DataTable
                columns={col}
                data={dbTable}
                pagination
                fixedHeader
                fixedHeaderScrollHeight={sizeContenTB}
                selectableRows
                selectableRowsHighlight
                highlightOnHover
                subHeader
                subHeaderComponent={<input type="text" placeholder="Search" />}
              />
            </div>
          </div>
        </section>
      </div>
    </form>
  );
};
export default Demo1;
