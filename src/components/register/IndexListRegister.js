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

  useEffect(() => {
    (async () => {
      let dataMana = await getData("day-off-letters?needAppr=1");
      let datapb = await getData(
        "day-off-letters?needAppr=3 &astatus=1%2C2%2C3%4%5"
      );
      if (dataMana.rData[0]?.aStatus === 1) {
        setShowMess(true);
      } else {
        setShowMess(false);
      }
      if (datapb.rData[0]?.aStatus === 1) {
        setShowMesspb(true);
      } else {
        setShowMesspb(false);
      }

      setpbkhac(datapb);
      //console.log(dataMana);
      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(false);
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
    //console.log(res);
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
                    <Tab>
                      Đơn Cần Phê Duyệt {""}
                      {showMess && (
                        <i
                          className="fas fa-info-circle "
                          style={{ color: "#ff0000" }}
                        />
                      )}
                    </Tab>
                    {pbkhac.rData.length > 0 && (
                      <Tab>
                        Đơn Cần Phê Duyệt Phòng Ban Khác {""}
                        {showMesspb && (
                          <i
                            className="fas fa-info-circle "
                            style={{ color: "#ff0000" }}
                          />
                        )}
                      </Tab>
                    )}
                    <Tab>Đơn Của Tôi</Tab>
                    <Tab>Hướng Dẫn Quy Trình</Tab>
                    {info?.DeptID === "NS" && (
                      <Tab>
                        <div className="d-flex align-items-center ">
                          <span
                            style={{ fontSize: "12px", whiteSpace: "nowrap" }}
                          >
                            File tổng hợp &nbsp;
                          </span>
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
                      </Tab>
                    )}
                  </TabList>
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
                      <StaffPage sizeConten={"85vh"} sizeContenTB={"68%"} />
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{ height: "100vh" }}>
                      <Usermanual />
                    </div>
                  </TabPanel>
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
              <Tab>Đơn Của Tôi</Tab>
              <Tab>Hướng Dẫn Quy Trình</Tab>
              {info?.DeptID === "NS" && (
                <Tab>
                  <div className="d-flex align-items-center ">
                    <span style={{ fontSize: "12px", whiteSpace: "nowrap" }}>
                      File tổng hợp &nbsp;
                    </span>
                    <DatePicker
                      className=" border border-primary rounded "
                      showicon
                      selected={startDate}
                      onChange={(date) => handelDownd(date, setStartDate(date))}
                      dateFormat="MM/yyyy"
                      showMonthYearPicker
                    />
                  </div>
                </Tab>
              )}
            </TabList>

            <TabPanel>
              <div style={{ height: "100vh" }}>
                <StaffPage sizeConten={"85vh"} sizeContenTB={"68%"} />
              </div>
            </TabPanel>
            <TabPanel>
              <div style={{ height: "100vh" }}>
                <Usermanual />
              </div>
            </TabPanel>
          </Tabs>
        </div>
      )}
    </>
  );
};
export default IndexListRegister;
