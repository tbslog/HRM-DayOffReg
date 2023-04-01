import React from "react";

const Pupup = ({
  className,
  color,
  onClose,
  children,
  title,
  isHideScroll = true,
}) => {
  return (
    <div
      // onDoubleClick={onClose}
      className=" card position-fixed  d-flex  align-items-center justify-content-center"
      style={{
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        background: "rgba(0, 0, 0, 0.4)",
      }}
    >
      <div className="card border border-1 p-3 ">
        <span
          onClick={onClose}
          className="position-absolute"
          style={{ right: "6px", cursor: "pointer", top: 0 }}
        >
          <i className="fas fa-times fa-lg" />
        </span>{" "}
        <h3 className="text-center ">{title}</h3>
        <div
          onClick={(e) => e.stopPropagation()}
          className={` border border-1  ${className}  ${
            isHideScroll && "hideSrcoll"
          } ml-1 mr-1 rounded position-relative `}
          style={{
            maxHeight: "90vh",
            maxWidth: "90vw ",
            minWidth: "30vw",
            background: ` ${color}`,
          }}
        >
          {children}
        </div>
      </div>
    </div>
  );
};

export default Pupup;
