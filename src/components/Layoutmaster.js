import face1 from "../assets/imgs/face1.jpg";
import logo from "../assets/imgs/LOGO 2013_1.png";
import { Link } from "react-router-dom";
import { logout } from "../actions/auth";
import { useDispatch, useSelector } from "react-redux";
import React, { useState, useEffect, useCallback, useRef } from "react";
import Cookies from "js-cookie";
import { getData } from "../services/user.service";
import { Modal } from "bootstrap";

import ChangepassHome from "./Changepass/ChangepassHome";
let emID = Cookies.get("empid");
//console.log(emID);
const Header = ({ children }) => {
  const dispatch = useDispatch();
  const logOut = useCallback(() => {
    dispatch(logout());
  }, [dispatch]);

  const [name, setname] = useState("");
  const [showNotiMana, setShowNotiMana] = useState();
  const [showNotiManapbk, setShowNotiManapbk] = useState();
  const [showNotitotal, setShowNotitotal] = useState();
  const [showNoti, setShowNoti] = useState(false);
  const [clear, setClear] = useState(false);

  const [ShowModal, SetShowModal] = useState("");
  const [modal, setModal] = useState(null);
  const parseExceptionModal = useRef();

  const showModalForm = () => {
    const modal = new Modal(parseExceptionModal.current, {
      keyboard: false,
      backdrop: "static",
    });
    setModal(modal);
    modal.show();
  };
  const hideModal = () => {
    setClear(false);
    modal.hide();
  };
  useEffect(() => {
    var fistlog = Cookies.get("fisstlogin");
    console.log(fistlog);
    if (fistlog == 1) {
      console.log("log");
      handelchangepass(SetShowModal("FirstLogin"));
      // confirmAlert({
      //   title: "Cảnh báo",
      //   message: "Bạn đang đăng nhập lần đầu tiên \n Vui lòng đổi mật khẩu ",
      //   buttons: [
      //     {
      //       label: "Đồng Ý",
      //       onClick: () =>
      //         handelchangepass(SetShowModal("Changepass"), setClear(true)),
      //     },
      //   ],
      // });
    }
  }, []);

  useEffect(() => {
    (async () => {
      let data = await getData("getEmpInfo");
      // console.log(data);
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
        setShowNoti(true);
        setShowNotiMana(notiMana);
        setShowNotiManapbk(notiManaPbk);
        setShowNotitotal(notiMana + notiManaPbk);
      } else {
        setShowNoti(false);
        setShowNotiMana();
        setShowNotiManapbk();
        setShowNotitotal(0);
      }

      Cookies.set(
        "info",
        JSON.stringify({
          FirstName: data.rData.FirstName,
          LastName: data.rData.LastName,
          JobpositionName: data.rData.JobpositionName,
          DeptID: data.rData.DeptID,
          JPLevelID: data.rData.JPLevelID,
        })
      );
      setname(data.rData.LastName + " " + data.rData.FirstName);
    })();
  }, []);
  const handelchangepass = () => {
    showModalForm();
  };
  const handelchangepass1 = () => {
    hideModal();
    showModalForm();
  };

  return (
    <>
      <div className="hold-transition sidebar-mini layout-fixed">
        <div className="wrapper">
          {/* Navbar */}
          <nav className="main-header navbar navbar-expand navbar-white navbar-light">
            {/* Left navbar links */}
            <ul className="navbar-nav">
              <li className="nav-item">
                <a
                  className="nav-link"
                  data-widget="pushmenu"
                  href="#"
                  role="button"
                >
                  <i className="fas fa-bars" />
                </a>
              </li>
              <li className="nav-item d-none d-sm-inline-block">
                <a href="/" className="nav-link">
                  Trang chủ
                </a>
              </li>
            </ul>
            {/* Right navbar links */}
            <ul className="navbar-nav ml-auto mr-3">
              {showNoti === true && (
                <li className="nav-item dropdown">
                  {" "}
                  <a className="nav-link" data-toggle="dropdown">
                    <i className="far fa-bell fa-lg" />
                    <span className="badge badge-danger navbar-badge">
                      {showNotitotal}
                    </span>
                  </a>
                  <div
                    className="dropdown-menu dropdown-menu-lg dropdown-menu-right"
                    style={{ borderRadius: "8px", overflow: "hidden" }}
                  >
                    {showNotiMana > 0 && (
                      <>
                        <div className="dropdown-divider" />

                        <Link
                          to={`/indexListRegister`}
                          style={{ fontSize: "13px" }}
                        >
                          <a className="dropdown-item">
                            {showNotiMana} đơn cần phê duyệt
                          </a>
                        </Link>
                      </>
                    )}

                    <div className="dropdown-divider" />
                    {showNotiManapbk > 0 && (
                      <>
                        {" "}
                        <div className="dropdown-divider" />
                        <Link
                          to={`/indexListRegister`}
                          style={{ fontSize: "13px" }}
                        >
                          <a className="dropdown-item">
                            {showNotiManapbk} đơn phòng ban khác cần phê duyệt
                          </a>
                        </Link>
                      </>
                    )}
                  </div>
                </li>
              )}

              <li className="nav-item dropdown">
                <a className="nav-link" data-toggle="dropdown">
                  <i className="far fa-user-circle fa-lg mr-1" />
                  {name}
                </a>

                <div
                  className="dropdown-menu dropdown-menu-sm dropdown-menu-right"
                  style={{ borderRadius: "8px", overflow: "hidden" }}
                >
                  <div className="d-flex flex-column flex-nowrap align-items-start">
                    {" "}
                    {/* <span className="dropdown-header d-flex justify-content-center p-0 ">
                      <Link to={`/info`} className="nav-link ">
                        <i
                          className="far fa-id-card  fa-lg mr-2  "
                          style={{ color: "#79859a" }}
                        />
                        Profile
                      </Link>
                    </span> */}
                    <div className="dropdown-divider w-100 p-0 m-0" />{" "}
                    <span
                      className=" dropdown-header d-flex justify-content-center "
                      onClick={() =>
                        handelchangepass(
                          SetShowModal("Changepass"),
                          setClear(true)
                        )
                      }
                    >
                      <i className="fas fa-exchange-alt fa-lg  mr-2" />
                      Đổi mật khẩu
                    </span>
                    <div className="dropdown-divider w-100 p-0 m-0" />
                    <a
                      href="/"
                      className="nav-link d-flex justify-content-center  "
                      style={{ color: "rgba(0,0,0,.5)" }}
                      onClick={logOut}
                    >
                      <i className="fas fa-sign-out-alt fa-lg d-flex align-items-center mr-1" />
                      Đăng xuất
                    </a>
                  </div>
                </div>
              </li>

              <li className="nav-item dropdown"> </li>
              {/* Navbar Search */}
            </ul>
          </nav>

          {/* /.navbar */}
          {/* Main Sidebar Container */}
          <aside className="main-sidebar main-sidebar-custom sidebar-dark-primary elevation-4">
            {/* Brand Logo */}
            <a href="/" className="brand-link">
              <span className="brand-text font-weight-light">
                {/* <img src={logo} style={{ height: "70px", width: "150px" }} /> */}
                <h5> TBS Logistics</h5>
              </span>
            </a>
            {/* Sidebar */}
            <div className="sidebar">
              {/* Sidebar user (optional) */}
              <div className="user-panel mt-3 pb-3 mb-3 d-flex">
                <div className="image">
                  <img
                    src={face1}
                    className="img-circle elevation-2"
                    alt="User Image"
                  />
                </div>
                <div className="info d-flex align-items-center">
                  <a className="d-block ">{name}</a>
                </div>
              </div>
              {/* SidebarSearch Form */}
              <div className="form-inline">
                <div className="input-group" data-widget="sidebar-search">
                  <input
                    className="form-control form-control-sidebar"
                    type="search"
                    placeholder="Search"
                    aria-label="Search"
                  />
                  <div className="input-group-append">
                    <button className="btn btn-sidebar">
                      <i className="fas fa-search fa-fw" />
                    </button>
                  </div>
                </div>
              </div>
              {/* Sidebar Menu */}
              <nav className="mt-2">
                <ul
                  className="nav nav-pills nav-sidebar flex-column"
                  data-widget="treeview"
                  role="menu"
                  data-accordion="false"
                >
                  <li className="nav-item">
                    <Link to={`/indexListRegister`} className="nav-link ">
                      <i className="far fa-circle nav-icon" />
                      <p>Quản lý ngày nghỉ</p>
                    </Link>
                  </li>
                  {/* Add icons to the links using the .nav-icon class
         with font-awesome or any other icon font library */}
                  {/* <li className="nav-item menu-open">
                    <a className="nav-link active">
                      <i className="nav-icon fas fa-tachometer-alt" />
                      <p>
                        Danh Mục
                        <i className="right fas fa-angle-left" />
                      </p>
                    </a>

                    <ul className="nav nav-treeview">
                      <li className="nav-item">
                        <Link to={`/indexListRegister`} className="nav-link ">
                          <i className="far fa-circle nav-icon" />
                          <p>Quản lý ngày nghỉ</p>
                        </Link>
                      </li>
                    </ul>
                  </li> */}
                </ul>
              </nav>
              {/* /.sidebar-menu */}
            </div>
            {/* /.sidebar */}
          </aside>
          <div>{children}</div>
          <footer className="main-footer">
            <strong>
              Copyright © 2022
              <a href="http://hrm-dor.tbslogistics.com.vn/"> TBSL</a>.
            </strong>
            <div className="float-right d-none d-sm-inline-block">
              <b>Version</b> 1.0.0
            </div>
          </footer>
          {/* Control Sidebar */}
          <aside className="control-sidebar control-sidebar-dark">
            {/* Control sidebar content goes here */}
          </aside>
          {/* /.control-sidebar */}
        </div>
      </div>
      <>
        <div
          className="modal fade"
          id="modal-xl"
          data-backdrop="static"
          ref={parseExceptionModal}
          aria-labelledby="parseExceptionModal"
          backdrop="static"
        >
          <div
            className="modal-dialog modal-dialog-scrollable"
            style={{ width: "40%" }}
          >
            <div className="modal-content">
              <div className="modal-header border-0 p-0">
                <button
                  type="button"
                  className="close"
                  style={{ marginRight: "2px" }}
                  data-dismiss="modal"
                  onClick={() => hideModal()}
                  aria-label="Close"
                >
                  <span aria-hidden="true" style={{ fontSize: "30px" }}>
                    ×
                  </span>
                </button>
              </div>
              <div className="modal-body pt-0">
                <>
                  {ShowModal === "Changepass" && (
                    <ChangepassHome clear={clear} hideModal={hideModal} />
                  )}
                </>
                <>
                  {ShowModal === "FirstLogin" && (
                    <div className="row d-flex flex-column h-100">
                      <div className="text-center">
                        <h3 style={{ color: "#ffc107" }}>CẢNH BÁO</h3>
                        <div className="dropdown-divider" />
                        <div className=" mb-1">
                          <label className="form-label" htmlFor="password">
                            Bạn đang đăng nhập lần đầu tiên <br></br> Vui lòng
                            đổi mật khẩu
                          </label>
                        </div>
                      </div>
                      <div className="d-flex justify-content-end">
                        <button
                          type="button"
                          className="btn btn-outline-secondary"
                          onClick={() =>
                            handelchangepass1(
                              SetShowModal("Changepass"),
                              setClear(true)
                            )
                          }
                        >
                          Đồng Ý
                        </button>
                      </div>
                    </div>
                  )}
                </>
              </div>
            </div>
          </div>
        </div>
      </>
    </>
  );
};

export default Header;
