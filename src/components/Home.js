import React, { useState, useEffect } from "react";

import tbsgropimg from "../assets/imgs/tbsgrop.jpg";

function Home() {
  return (
    <form>
      <div className="content-wrapper">
        <div
          className="form-horizontal"
          style={{ height: "calc(100vh - 114px)" }}
        >
          <img
            style={{
              objectFit: "cover",
              width: "100%",
              height: "100%",
              maxWidth: "100%",
            }}
            // className="h-100"
            src={tbsgropimg}
          />
        </div>
      </div>
    </form>
  );
}

export default Home;
