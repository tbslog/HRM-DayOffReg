import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import React, { useState, useEffect } from "react";
import { getData, getDataCustom } from "../../services/user.service";
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
      let dataMana = await getDataCustom("day-off-letters", {
        needAppr: 1,
        astatus: [],
      });
      console.log(dataMana);
      if (dataMana.rData.length > 0) {
        setOpen(true);
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
                    <Tab>Đơn Cần Phê Duyệt</Tab>
                    <Tab>Đơn Của Tôi</Tab>
                  </TabList>
                  <TabPanel>
                    <div style={{ height: "590px" }}>
                      <ManagerPage
                        sizeConten={"500px"}
                        sizeContenTB={"420px"}
                      />
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{ height: "596px" }}>
                      <StaffPage sizeConten={"560px"} sizeContenTB={"414px"} />
                    </div>
                  </TabPanel>
                </Tabs>
              </div>
            </div>
          </section>
        </div>
      ) : (
        <div className="content-wrapper ">
          <StaffPage sizeConten={"480px"} sizeContenTB={"470px"} />
        </div>
      )}
    </>
  );
};
export default IndexListRegister;
