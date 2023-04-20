import { getData, postData, putData } from "../../services/user.service";
import React, { useState, useEffect, useCallback, useRef } from "react";
import DataTable from "react-data-table-component";
import { useForm, Controller } from "react-hook-form";
import Loading from "../common/loading/Loading";
import { toast } from "react-toastify";
import { QuestionCircleOutlined } from "@ant-design/icons";
import {
  Modal,
  Select,
  TreeSelect,
  Button,
  Form,
  Input,
  Popconfirm,
  InputNumber,
} from "antd";

const JobTitle = () => {
  const [dbTable, setdbTable] = useState([]);

  const [IsLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [jobTitle, setJobTitle] = useState({});
  const [callback, setcallback] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors },
  } = useForm();

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData("get-jplevel");
      setdbTable(data.rData);
      setIsLoading(false);
    })();
  }, [callback]);

  const validateForm = {
    jplevelID: {
      required: "Không được để trống",
      pattern: {
        value: /^[0-9]*$/,
        message: "Chỉ được nhập ký tự là số",
      },
    },
    jobname: {
      required: "Không được để trống",
    },
  };

  const col = [
    {
      name: "Cấp chức danh",
      selector: (row) => row.JPLevelID,
      sortable: true,
    },
    {
      name: "Tên chức vụ",
      selector: (row) => row.Name,
      sortable: true,
    },
    {
      name: "Ghi Chú",
      selector: (row) => row.Note,
      sortable: true,
    },
    {
      name: "Trạng thái",
      selector: (row) => checkStatus(row.Status),
      sortable: true,
    },
    {
      name: "Action",
      cell: (row) => actionEdit(row),
    },
  ];
  const checkStatus = (id) => {
    if (id === 1) {
      return (
        <i
          className="far fa-pause-circle"
          style={{ fontSize: "20px" }}
          title="Hoạt động"
        />
      );
    }
    if (id === 0) {
      return (
        <i
          className="far fa-play-circle"
          style={{ fontSize: "20px" }}
          title="Tạm ngưng"
        />
      );
    }
  };

  const actionEdit = (record) => {
    return (
      <>
        <button
          type="button"
          data-toggle="modal"
          data-target="#exampleModalCenter"
          className="ml-1"
          style={{ border: "none", background: "white" }}
          onClick={() => handleEditButtonClick(record)}
        >
          <i className="fas fa-info-circle fa-lg" title="Thông tin"></i>
        </button>
        <Popconfirm
          title="Xóa Chức Vụ"
          description="Bạn có chắc muốn xóa"
          okText="Xác Nhận"
          cancelText="Hủy"
          onConfirm={() => handleDelete(record)}
        >
          <Button type="button">
            <i className="fas fa-trash fa-lg" title="Xóa"></i>
          </Button>
        </Popconfirm>
      </>
    );
  };
  const handleDelete = async (record) => {
    console.log(record);
    var editdata = await putData(
      `delete-jplevel?jplevelID=${record.JPLevelID}`
    );

    if (editdata.isSuccess === 1) {
      toast.success("Xóa thành công \n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      setcallback(!callback);
    } else {
      console.log(editdata);
      toast.error("Xóa thất bại Lỗi: \n" + editdata.rMsg, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
    }
  };
  const handleEditButtonClick = async (record) => {
    setJobTitle(record);
    setOpen(true);
  };

  const onSubmitCreateJob = async (data) => {
    console.log(data);

    var create = await postData("import-jplevel", {
      jplevelID: data.jplevelID,

      Name: data.jobname,
      note: data.note,
    });
    if (create.isSuccess === 1) {
      toast.success("Thêm mới thành công \n" + create.rMsg, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setcallback(!callback);
      setIsLoading(false);
    } else {
      console.log(create);
      toast.error("Thêm mới thất bại Lỗi: \n" + create.rMsg, {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });
      setIsLoading(false);
    }
  };
  const hideUserModal = () => {
    setOpen(false);
  };
  const useResetFormOnCloseModal = ({ form, open }) => {
    const prevOpenRef = useRef();
    useEffect(() => {
      prevOpenRef.current = open;
    }, [open]);
    const prevOpen = prevOpenRef.current;
    useEffect(() => {
      if (!open && prevOpen) {
        form.resetFields();
      }
    }, [form, prevOpen, open]);
  };
  const ModalForm = ({ open, onCancel }) => {
    const [form] = Form.useForm();

    useEffect(() => {
      form.setFieldsValue({
        Name: jobTitle.Name,
        JPLevelID: jobTitle.JPLevelID,
        Note: jobTitle.Note,
        Status: jobTitle.Status,
      });
    }, [jobTitle, form]);

    useResetFormOnCloseModal({
      form,
      open,
    });
    const onOk = () => {
      form.submit();
    };

    const updatejplv = async (data) => {
      console.log(data);
      var editdata = await putData("update-jplevel", {
        jplevelID: data.JPLevelID,
        name: data.Name,
        note: data.Note,
        status: data.Status,
      });

      if (editdata.isSuccess === 1) {
        toast.success("Cập nhật thành công \n" + editdata.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
        setcallback(!callback);
        hideUserModal();
      } else {
        console.log(editdata);
        toast.error("Cập nhật thất bại Lỗi: \n" + editdata.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
      }
    };

    return (
      <Modal
        title="CHỈNH SỬA CHỨC VỤ"
        open={open}
        onOk={onOk}
        okText="Lưu"
        cancelText="Hủy"
        onCancel={onCancel}
      >
        <Form
          form={form}
          name="basic"
          onFinish={updatejplv}
          layout="vertical"
          //onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item
            name="Name"
            label="Tên"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="JPLevelID"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
            label="Cấp Chức Danh"
          >
            <Input />
          </Form.Item>
          <Form.Item label="Ghi Chú" name="Note">
            <Input />
          </Form.Item>
          <Form.Item
            name="Status"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },

              {
                pattern: /^[0-9]*$/,
                message: "Chỉ được nhập ký tự là số",
              },
            ]}
            label={
              <label className="form-label">
                Trạng Thái{" "}
                <span style={{ color: "#dfdfdf" }}>
                  &ensp; ( 0 Là 'Tạm ngưng', 1 là 'Hoạt đông')
                </span>
              </label>
            }
          >
            <Input />
            {/* <div className="p-2 ">
              
            </div> */}
          </Form.Item>
        </Form>
      </Modal>
    );
  };

  return (
    <>
      <form>
        {IsLoading ? (
          <Loading />
        ) : (
          <div className="content-wrapper  pl-2">
            <div className="card-header py-0 border-0">
              <div
                className="row pt-1 "
                style={{
                  justifyContent: "space-between ",
                  background: "rgb(224 224 224)",
                }}
              >
                <div className="pt-2 ml-2">
                  {/* style={{ alignSelf: "end" }} */}
                  Name
                </div>
                <div className="pt-2 ml-2">
                  {/* style={{ alignSelf: "end" }} */}
                  <h3> DANH SÁCH CHỨC VỤ</h3>
                </div>

                <div className="pt-1 ">
                  {/* style={{ alignSelf: "end" }} */}
                </div>
              </div>
            </div>
            <div className="card-header py-0 border-0 pb-2">
              <div
                className="row pt-1 "
                style={{
                  justifyContent: "space-between ",
                }}
              >
                <div className=" d-flex flex-column align-items-center">
                  {/* style={{ alignSelf: "end" }} */}
                  Cấp chức danh
                  <input
                    type="text"
                    className="form-control ml-3"
                    {...register("jplevelID", validateForm.jplevelID)}
                  />
                  <span
                    className=""
                    style={{
                      color: "red",
                      fontSize: "10px",
                    }}
                  >
                    {errors.jplevelID?.message}
                  </span>
                </div>
                <div className=" d-flex flex-column align-items-center">
                  {/* style={{ alignSelf: "end" }} */}
                  Tên chức vụ
                  <input
                    type="text"
                    className="form-control ml-3"
                    {...register("jobname", validateForm.jobname)}
                  />
                  <span
                    className=""
                    style={{
                      color: "red",
                      fontSize: "10px",
                    }}
                  >
                    {errors.jobname?.message}
                  </span>
                </div>
                <div className=" d-flex flex-column align-items-center">
                  {/* style={{ alignSelf: "end" }} */}
                  Ghi chú
                  <input
                    type="text"
                    className="form-control ml-3"
                    {...register("note")}
                  />
                </div>
                <div className="pt-1 d-flex align-items-end ">
                  {/* style={{ alignSelf: "end" }} */}
                  <button
                    className="btn btn-sm btn-success mr-3 d-flex align-items-center "
                    style={{ height: "37px" }}
                    onClick={handleSubmit(onSubmitCreateJob)}
                  >
                    <i className="fas fa-plus fa-lg" /> Thêm Mới
                  </button>
                </div>
              </div>
            </div>
            <div className="card-body m-0 p-0 " style={{ height: "85vh" }}>
              <DataTable
                columns={col}
                data={dbTable}
                pagination
                paginationPerPage={25}
                paginationRowsPerPageOptions={[25, 50, 75]}
                fixedHeader
                fixedHeaderScrollHeight={"73%"}
                selectableRowsHighlight
                highlightOnHover
              />
            </div>
            <ModalForm open={open} onCancel={hideUserModal} />
          </div>
        )}
      </form>
    </>
  );
};
export default JobTitle;
