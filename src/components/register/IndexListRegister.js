import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import React, { useState, useEffect } from "react";
import { getData, getDataCustom } from "../../services/user.service";
import StaffPage from "./StaffPage";
import ManagerPage from "./ManagerPage";
import Usermanual from "../usermanual/Usermanual";
const IndexListRegister = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const HandleOnChangeTabs = (tabIndex) => {
    setTabIndex(tabIndex);
  };

  const [open, setOpen] = useState(false);
  useEffect(() => {
    (async () => {
      let dataMana = await getDataCustom("day-off-letters", {
        needAppr: 1,
        astatus: [],
      });
      //console.log(dataMana);
      if (dataMana.rData.length > 0) {
        setOpen(true);
      } else setOpen(false);
    })();
  }, []);
  return (
    <>
      {open ? (
        <div className="content-wrapper ">
          <section
            className="content"
            style={{ maxHeight: "100%", height: "100vh" }}
          >
            {/* Default box */}
            <div className="card  " style={{ height: "100%" }}>
              <div className="card-header py-0 border-0">
                <Tabs
                  selectedIndex={tabIndex}
                  onSelect={(index) => HandleOnChangeTabs(index)}
                >
                  <TabList>
                    <Tab>Đơn Cần Phê Duyệt</Tab>
                    <Tab>Đơn Của Tôi</Tab>
                    <Tab>Hướng Dẫn Quy Trình</Tab>
                  </TabList>
                  <TabPanel>
                    <div style={{ height: "100vh" }}>
                      <ManagerPage sizeConten={"85vh"} sizeContenTB={"68%"} />
                    </div>
                  </TabPanel>
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
          <StaffPage sizeConten={"90vh"} sizeContenTB={"73%"} />
        </div>
      )}
    </>
  );
};
export default IndexListRegister;
