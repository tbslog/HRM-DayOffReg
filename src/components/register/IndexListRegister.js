import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import React, { useState, useEffect } from "react";
import { getData, getfile, getDataCustom } from "../../services/user.service";
import StaffPage from "./StaffPage";
import ManagerPage from "./ManagerPage";
import OtherDepartments from "./OtherDepartments";
import Usermanual from "../usermanual/Usermanual";
import Cookies from "js-cookie";
import DatePicker from "react-datepicker";
import moment from "moment";

const IndexListRegister = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const HandleOnChangeTabs = (tabIndex) => {
    setTabIndex(tabIndex);
  };

  let info = Cookies.get("info") && JSON?.parse(Cookies.get("info")); // kiểm tra đk 1 nếu có chạy câu lệnh sau
  const [startDate, setStartDate] = useState(new Date());
  const [open, setOpen] = useState(false);
  const [pbkhac, setpbkhac] = useState([]);
  const [showMess, setShowMess] = useState(false);
  const [showMesspb, setShowMesspb] = useState(false);
  const [showNotiMana, setShowNotiMana] = useState();
  const [showNotiManapbk, setShowNotiManapbk] = useState();

  useEffect(() => {
    (async () => {
      let dataMana = await getData("day-off-letters?needAppr=1");
      let datapb = await getData(
        "day-off-letters?needAppr=3 &astatus=1%2C2%2C3%4%5"
      );

      let notiMana = dataMana.rData.reduce((count, i) => {
        if (i.aStatus === 1) {
          count += 1;
        }
        return count;
      }, 0);
      let notiManaPbk = datapb.rData.reduce((count, i) => {
        if (i.aStatus === 1) {
          count += 1;
        }
        return count;
      }, 0);
      if (notiMana > 0 || notiManaPbk > 0) {
        setShowMess(true);
        setShowNotiMana(notiMana);
        setShowNotiManapbk(notiManaPbk);
      } else {
        setShowMess(false);
        setShowNotiMana();
        setShowNotiManapbk();
      }
      // if (dataMana.rData[0]?.aStatus === 1) {
      //   setShowMess(true);
      // } else {
      //   setShowMess(false);
      // }
      // if (datapb.rData[0]?.aStatus === 1) {
      //   setShowMesspb(true);
      // } else {
      //   setShowMesspb(true);
      // }

      setpbkhac(datapb);
      //console.log(dataMana);
      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(true);
    })();
  }, []);
  const onSubmitDownload = async () => {
    let res = await getfile("day-off-summary");
    console.log(res);
    //const url = window.URL.createObjectURL(new Blob([res]));//list file
    const url = window.URL.createObjectURL(res); // một file
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "Data.xlsx");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };
  const handelDownd = async (data) => {
    let day = moment(new Date(data).toISOString()).format("YYYY-MM-DD");

    let res = await getfile(`day-off-summary?date=${day}`);
    //const url = window.URL.createObjectURL(new Blob([res]));//list file
    const url = window.URL.createObjectURL(res); // một file
    const link = document.createElement("a"); // tao the a gan link
    link.href = url;
    link.setAttribute("download", "Data.xlsx");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <>
      {open ? (
        <div className="content-wrapper ">
          <section
            className="content"
            style={{ maxHeight: "100%", height: "100vh" }}
          >
            {/* Default box */}
            <div className="card " style={{ height: "100%" }}>
              <div className="card-header py-0 border-0">
                <Tabs
                  selectedIndex={tabIndex}
                  onSelect={(index) => HandleOnChangeTabs(index)}
                >
                  <TabList>
                    <Tab>QL Đơn Nghỉ Phép</Tab>
                    <Tab>
                      Đơn Cần Phê Duyệt {""}
                      {showMess && (
                        <span
                          className="badge badge-danger navbar-badge"
                          style={{ right: " -2px", top: "12px" }}
                        >
                          {showNotiMana}
                        </span>
                      )}
                    </Tab>
                    {pbkhac.rData.length > 0 && (
                      <Tab>
                        Đơn Cần Phê Duyệt Phòng Ban Khác {""}
                        {showMesspb && (
                          <span
                            className="badge badge-danger navbar-badge"
                            style={{ right: " -2px", top: "12px" }}
                          >
                            {showNotiManapbk}
                          </span>
                        )}
                      </Tab>
                    )}

                    <Tab>Hướng Dẫn Quy Trình</Tab>
                    {(info?.DeptID === "NS" || info?.JPLevelID <= 50) && (
                      <Tab>Export</Tab>
                    )}
                  </TabList>
                  <TabPanel>
                    <div style={{ height: "100vh" }}>
                      <StaffPage sizeConten={"85vh"} sizeContenTB={"83%"} />
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{ height: "100vh" }}>
                      <ManagerPage sizeConten={"85vh"} sizeContenTB={"68%"} />
                    </div>
                  </TabPanel>
                  {pbkhac.rData.length > 0 && (
                    <TabPanel>
                      <div style={{ height: "100vh" }}>
                        <OtherDepartments
                          sizeConten={"85vh"}
                          sizeContenTB={"68%"}
                        />
                      </div>
                    </TabPanel>
                  )}

                  <TabPanel>
                    <div style={{ height: "100vh" }}>
                      <Usermanual />
                    </div>
                  </TabPanel>
                  {(info?.DeptID === "NS" || info?.JPLevelID <= 50) && (
                    <TabPanel>
                      <div className="card-body  p-0 d-flex justify-content-center mt-3">
                        <span>
                          Chọn Tháng cần lấy danh sách nghỉ phép &nbsp;
                        </span>
                        <div>
                          <DatePicker
                            className=" border border-primary rounded "
                            showicon
                            selected={startDate}
                            onChange={(date) =>
                              handelDownd(date, setStartDate(date))
                            }
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                          />
                        </div>
                      </div>
                    </TabPanel>
                  )}
                </Tabs>
              </div>
            </div>
          </section>
        </div>
      ) : (
        <div className="content-wrapper " style={{ height: "100vh" }}>
          <Tabs
            selectedIndex={tabIndex}
            onSelect={(index) => HandleOnChangeTabs(index)}
          >
            <TabList>
              <Tab>QL Đơn Nghỉ Phép</Tab>
              <Tab>Hướng Dẫn Quy Trình</Tab>
              {(info?.DeptID === "NS" || info?.JPLevelID <= 50) && (
                <Tab>Export</Tab>
              )}
            </TabList>

            <TabPanel>
              <div style={{ height: "100vh" }}>
                <StaffPage sizeConten={"85vh"} sizeContenTB={"83%"} />
              </div>
            </TabPanel>
            <TabPanel>
              <div style={{ height: "100vh" }}>
                <Usermanual />
              </div>
            </TabPanel>
            {(info?.DeptID === "NS" || info?.JPLevelID <= 50) && (
              <TabPanel>
                <div className="card-body  p-0 d-flex justify-content-center mt-3">
                  <span>Chọn Tháng cần lấy danh sách nghỉ phép &nbsp;</span>
                  <div>
                    <DatePicker
                      className=" border border-primary rounded "
                      showicon
                      selected={startDate}
                      onChange={(date) => handelDownd(date, setStartDate(date))}
                      dateFormat="MM/yyyy"
                      showMonthYearPicker
                    />
                  </div>
                </div>
              </TabPanel>
            )}
          </Tabs>
        </div>
      )}
    </>
  );
};
export default IndexListRegister;
