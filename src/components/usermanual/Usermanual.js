import React from "react";
import tbsgropimg from "../../assets/imgs/huongdan.jpg";

const Usermanual = () => {
  return (
    <div className="form-horizontal" style={{ height: "calc(100vh - 157px)" }}>
      <img
        style={{
          objectFit: "contain",
          width: "100%",
          height: "100%",
          maxWidth: "100%",
        }}
        className="h-100"
        src={tbsgropimg}
      />
    </div>
  );
};
export default Usermanual;
