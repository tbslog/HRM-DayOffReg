import face1 from "../assets/imgs/face1.jpg";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import React, { useState } from "react";

const Demo2 = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const HandleOnChangeTabs = (tabIndex) => {
    setTabIndex(tabIndex);
  };
  return (
    <div className="card-body">
      <Tabs
        selectedIndex={tabIndex}
        onSelect={(index) => HandleOnChangeTabs(index)}
      >
        <TabList>
          <Tab>Tab1</Tab>
          <Tab>Tab2</Tab>
        </TabList>
        <TabPanel>
          <div>Tab1 conten</div>
        </TabPanel>
        <TabPanel>
          <div>Tab2 conten</div>
        </TabPanel>
      </Tabs>
    </div>
  );
};
export default Demo2;
