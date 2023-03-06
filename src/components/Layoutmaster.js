import face1 from "../assets/imgs/face1.jpg";
import { Link } from "react-router-dom";
import { logout } from "../actions/auth";
import { useDispatch, useSelector } from "react-redux";
import React, { useState, useEffect, useCallback } from "react";
import Cookies from "js-cookie";
import { getData } from "../services/user.service";
let emID = Cookies.get("empid");

const Header = ({ children }) => {
  const dispatch = useDispatch();
  const logOut = useCallback(() => {
    dispatch(logout());
  }, [dispatch]);

  const [name, setname] = useState("");

  useEffect(() => {
    (async () => {
      let data = await getData("getEmpInfo");

      Cookies.set(
        "info",
        JSON.stringify({
          FirstName: data.rData.FirstName,
          LastName: data.rData.LastName,
          JobpositionName: data.rData.JobpositionName,
          DeptID: data.rData.DeptID,
        })
      );
      setname(data.rData.FirstName + " " + data.rData.LastName);
    })();
  }, []);

  return (
    <>
      <div className="hold-transition sidebar-mini layout-fixed">
        <div className="wrapper">
          {/* Navbar */}
          <nav className="main-header navbar navbar-expand navbar-white navbar-light d-flex justify-content-between">
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
            <li className="nav-item d-none d-sm-inline-block">
              <a
                href="/"
                className="nav-link"
                style={{ color: "rgba(0,0,0,.5)" }}
                onClick={logOut}
              >
                Đăng xuất
              </a>
            </li>
            {/* Right navbar links */}
          </nav>
          {/* /.navbar */}
          {/* Main Sidebar Container */}
          <aside className="main-sidebar main-sidebar-custom sidebar-dark-primary elevation-4">
            {/* Brand Logo */}
            <a href="index3.html" className="brand-link">
              <span className="brand-text font-weight-light">
                TBS Logistics
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
                  {/* Add icons to the links using the .nav-icon class
         with font-awesome or any other icon font library */}
                  <li className="nav-item ">
                    <a href="#" className="nav-link active">
                      <i className="nav-icon fas fa-tachometer-alt" />
                      <p>
                        Danh Mục
                        <i className="right fas fa-angle-left" />
                      </p>
                    </a>
                    <ul className="nav nav-treeview">
                      <li className="nav-item">
                        <Link to="/indexListRegister" className="nav-link ">
                          <i className="far fa-circle nav-icon" />
                          <p>Quản lý ngày nghỉ</p>
                        </Link>
                      </li>
                      {/* <li className="nav-item">
                        <Link to="/Approve" className="nav-link ">
                          <i className="far fa-circle nav-icon" />
                          <p>Phê Duyệt</p>
                        </Link>
                      </li> */}
                    </ul>
                  </li>
                </ul>
              </nav>
              {/* /.sidebar-menu */}
            </div>
            {/* /.sidebar */}
          </aside>
          <div
            className="w-100"
            style={{ overflow: "hidden", maxHeight: "100%", height: "85vh" }}
          >
            {children}
          </div>
          <footer className="main-footer">
            <strong>
              Copyright © 2022<a href="https://adminlte.io"> TBSL</a>.
            </strong>
            All rights reserved.
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
    </>
  );
};

export default Header;
