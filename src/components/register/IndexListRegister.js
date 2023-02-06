import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import React, { useState, useEffect } from "react";
import { getData } from "../../services/user.service";
import StaffPage from "./StaffPage";
import ManagerPage from "./ManagerPage";
const IndexListRegister = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const HandleOnChangeTabs = (tabIndex) => {
    setTabIndex(tabIndex);
  };
  const [open, setOpen] = useState(false);
  useEffect(() => {
    (async () => {
      let dataMana = await getData("day-off-letters?needAppr=1");
      console.log(dataMana.rData);
      if (dataMana.rData.length > 0) {
        setOpen(true);
        console.log(dataMana.rData.length);
      } else setOpen(false);
    })();
  }, []);
  return (
    <>
      {open ? (
        <div className="content-wrapper ">
          <section className="content">
            {/* Default box */}
            <div className="card ">
              <div className="card-header py-0 border-0">
                <Tabs
                  selectedIndex={tabIndex}
                  onSelect={(index) => HandleOnChangeTabs(index)}
                >
                  <TabList>
                    <Tab>Đơn Của Tôi</Tab>
                    <Tab>Đơn Cần Phê Duyệt</Tab>
                  </TabList>
                  <TabPanel>
                    <div style={{ height: "586px" }}>
                      <StaffPage />
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{ height: "586px" }}>
                      <ManagerPage />
                    </div>
                  </TabPanel>
                </Tabs>
              </div>
            </div>
          </section>
        </div>
      ) : (
        <StaffPage />
      )}
    </>
  );
};
export default IndexListRegister;
