import face1 from "../../assets/imgs/face1.jpg";
import Cookies from "js-cookie";
import { getData } from "../../services/user.service";
import { postIMG, getIMG } from "../../services/upload-files.service";
import { useNavigate } from "react-router-dom";
import "./info.css";

import React, { useState, useEffect, useCallback } from "react";
import moment from "moment";
import { CLEAR_MESSAGE } from "../../actions/type";

let emID = Cookies.get("empid");

const Info = () => {
  const [data, setData] = useState([]);
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isShow, setisShow] = useState(false);
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    async function fetchData() {
      let data1 = await getData("profile_img/", emID);
      setData(data1);
      console.log(data1);
    }
    fetchData();
    async function fetchData() {
      const response = await getIMG("get-image/");
      //const imageUrl = URL.createObjectURL(response);
      setImageUrl(response);
    }
  }, [emID, isShow]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };
  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", image);

    let data = await postIMG("upload/", formData);
    if (data?.rCode === 1) {
      async function fetchData() {
        const response = await getIMG("get-image/");
        console.log(response);
        //const imageUrl = URL.createObjectURL(response);
        setImageUrl(response);
        window.location.reload();
      }
      setisShow(false);
    }
  };
  const handeledit = () => {
    console.log(1);
    setisShow(true);
  };
  return (
    <div className="content-wrapper ">
      {" "}
      <section
        className="content"
        style={{ maxHeight: "100%", height: "100vh" }}
      >
        <div className="card p-3 mt-2 mb-3 " style={{ height: "100%" }}>
          <div style={{ overflowY: "auto", overflowX: "hidden" }}>
            <div className="row gutters-sm">
              <div className="col-lg-3 mb-3">
                <button className="btn">
                  <i
                    className="fas fa-edit "
                    title="Chỉnh Sửa"
                    onClick={handeledit}
                  />{" "}
                </button>
                <div className="card-body">
                  <div className="d-flex flex-column align-items-center text-center">
                    <img
                      src={imageUrl}
                      alt="Admin"
                      className="rounded-circle"
                      width={150}
                    />
                    {isShow === true && (
                      <div className="row d-flex  flex-nowrap">
                        <input
                          className=" btn custom-file-input"
                          type="file"
                          onChange={handleImageChange}
                          style={{ fontSize: "12px", opacity: "1" }}
                        />
                        <button
                          className="btn "
                          type="submit"
                          onClick={handleSubmit}
                          style={{ fontSize: "15px" }}
                        >
                          <i className="fa fa-upload" title="Tải Lên"></i>
                        </button>
                      </div>
                    )}

                    <div className="mt-3">
                      <h4> {data.rData?.FirstName}</h4>
                      <p className="text-secondary mb-1">
                        {data.rData?.ZoneName}
                      </p>
                      <p className="text-muted font-size-sm">
                        {data.rData?.JobpositionName}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="card mt-3">
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                      <h6 className="mb-0">Họ tên</h6>
                      <span className="text-secondary">
                        {" "}
                        {data.rData?.LastName} {data.rData?.FirstName}
                      </span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                      <h6 className="mb-0">SĐT</h6>
                      <span className="text-secondary">0988.888.888</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                      <h6 className="mb-0">Địa chỉ</h6>
                      <span className="text-secondary">HCM</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                      <h6 className="mb-0">Ngày sinh</h6>
                      <span className="text-secondary">...</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div
                className="tab-content profile-tab ml-4"
                id="myTabContent"
                style={{ maxWidth: "100%", minWidth: "63%" }}
              >
                <div className="profile-head">
                  <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item">
                      <a
                        className="nav-link active"
                        id="home-tab"
                        data-toggle="tab"
                        href="#home"
                        role="tab"
                        aria-controls="home"
                        aria-selected="true"
                      >
                        <span style={{ fontSize: "12px" }}>Thông cá nhân</span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link"
                        id="profile-tab"
                        data-toggle="tab"
                        href="#profile"
                        role="tab"
                        aria-controls="profile"
                        aria-selected="false"
                      >
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Hợp đồng lao động
                        </span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link"
                        id="cd-tab"
                        data-toggle="tab"
                        href="#cd"
                        role="tab"
                        aria-controls="cd"
                        aria-selected="false"
                      >
                        {" "}
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Chế dộ làm việc
                        </span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link"
                        id="ls-tab"
                        data-toggle="tab"
                        href="#ls"
                        role="tab"
                        aria-controls="ls"
                        aria-selected="false"
                      >
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Lịch sử công tác
                        </span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link "
                        id="kl-tab"
                        data-toggle="tab"
                        href="#kl"
                        role="tab"
                        aria-controls="kl"
                        aria-selected="false"
                      >
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Vi phạm kỷ luật
                        </span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link "
                        id="qh-tab"
                        data-toggle="tab"
                        href="#qh"
                        role="tab"
                        aria-controls="qh"
                        aria-selected="false"
                      >
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Quan hệ gia đình
                        </span>
                      </a>
                    </li>
                    <li className="nav-item">
                      <a
                        className="nav-link "
                        id="qt-tab"
                        data-toggle="tab"
                        href="#qt"
                        role="tab"
                        aria-controls="qt"
                        aria-selected="false"
                      >
                        <span style={{ fontSize: "12px" }}>
                          {" "}
                          Quá trình học tập
                        </span>
                      </a>
                    </li>
                  </ul>
                </div>
                <div
                  className="tab-content profile-tab ml-1 pt-2"
                  id="myTabContent"
                >
                  <div
                    className="tab-pane fade show active"
                    id="home"
                    role="tabpanel"
                    aria-labelledby="home-tab"
                  >
                    <div className="card mb-3">
                      <div className="card-body">
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Họ tên:</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            {data.rData?.LastName} {data.rData?.FirstName}
                          </div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Ngày sinh</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">none</div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Chức vụ</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            {" "}
                            {data.rData?.JobpositionName}
                          </div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Phòng ban</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            {" "}
                            {data.rData?.DepartmentName}
                          </div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Email</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            {data.rData?.Email}{" "}
                          </div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Phone</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            0988.888.888
                          </div>
                        </div>

                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Address</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">HCM</div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Ngày vào làm</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            {moment(data.rData?.ComeDate).format("DD-MM-YYYY")}
                          </div>
                        </div>
                        <hr />
                        <div className="row">
                          <div className="col-sm-4">
                            <h6 className="mb-0">Số BHXH</h6>
                          </div>
                          <div className="col-sm-8 text-secondary">
                            888888888
                          </div>
                        </div>
                        <hr />
                        {/* <div className="row">
                        <div className="col-sm-12">
                          <a
                            className="btn btn-info "
                            target="__blank"
                            href="https://www.bootdey.com/snippets/view/profile-edit-data-and-skills"
                          >
                            Edit
                          </a>
                        </div>
                      </div> */}
                      </div>
                    </div>
                  </div>
                  <div
                    className="tab-pane fade"
                    id="profile"
                    role="tabpanel"
                    aria-labelledby="profile-tab"
                  >
                    <div className="row">
                      <div className="col-md-6">
                        <label>...</label>
                      </div>
                      <div className="col-md-6">
                        <p>...</p>
                      </div>
                    </div>
                  </div>
                  <div
                    className="tab-pane fade"
                    id="cd"
                    role="tabpanel"
                    aria-labelledby="cd-tab"
                  >
                    <div className="row">
                      <div className="col-md-6">
                        <label>...</label>
                      </div>
                      <div className="col-md-6">
                        <p>...</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
export default Info;
