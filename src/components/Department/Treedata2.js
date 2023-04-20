import {
  Select,
  TreeSelect,
  Button,
  Popconfirm,
  Form,
  Input,
  Modal,
  Table,
  InputNumber,
} from "antd";
import { useState, useEffect, useRef } from "react";

import { getData, postData, putData } from "../../services/user.service";
import { toast } from "react-toastify";
import Loading from "../common/loading/Loading";

const Treedata2 = ({ data, callback, setcallback }) => {
  const [dataSource, setDataSource] = useState([]);
  const [dbTree, setdbTree] = useState([]);
  const [listDeptlv, setlistDeptlv] = useState([]);
  const [value, setValue] = useState();
  const [form] = Form.useForm();
  const [open, setOpen] = useState(false);
  const [recordDept, setrecordDept] = useState({});

  useEffect(() => {
    setDataSource(data);
    (async () => {
      let datalistDept = await getData("get-deptlevel");

      setlistDeptlv(datalistDept.rData);

      setdbTree(getAncestors(data));
    })([dataSource]);
  }, [dataSource, data]);

  const getAncestors = (array) => {
    if (typeof array != "undefined") {
      for (let i = 0; i < array.length; i++) {
        array[i].value = array[i].DeptID;
        array[i].title = array[i].Name;
        if (array[i].children?.length > 0) {
          getAncestors(array[i].children);
        }
      }
    }
    return array;
  };
  const checkStatus = (id) => {
    if (id.Status === 1) {
      return (
        <i
          className="far fa-pause-circle"
          style={{ fontSize: "20px" }}
          title="Hoạt động"
        />
      );
    }
    if (id.Status === 0) {
      return (
        <i
          className="far fa-play-circle"
          style={{ fontSize: "20px" }}
          title="Tạm ngưng"
        />
      );
    }
  };
  // const checkDepLV = (id) => {
  //   const result = listDeptlv.find(({ DLvlCode }) => DLvlCode === id);
  //   let a = result?.DLvlName;
  //   return a;
  // };
  const columns = [
    {
      title: "Tên Phòng Ban",
      dataIndex: "Name",
      key: "Name",
    },
    {
      title: "Mã PB",
      dataIndex: "DeptID",
      key: "DeptID",
      width: "15%",
    },
    {
      title: "Ghi Chú",
      dataIndex: "Note",
      key: "Note",
      width: "20%",
    },
    {
      title: "Tình trạng",
      dataIndex: "",
      width: "15%",
      key: "Status",
      render: (record) => <> {checkStatus(record)}</>,
    },
    {
      title: "Action",
      dataIndex: "",
      width: "15%",
      key: "DeptID",
      render: (record) => <> {actionEdit(record)}</>,
    },
  ];
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
          title="Xóa Phòng Ban"
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
    var editdata = await putData(`delete-department?deptID=${record.DeptID}`);

    if (editdata.isSuccess === 1) {
      toast.success("Xóa thành công \n", {
        autoClose: 2000,
        className: "",
        position: "top-center",
        theme: "colored",
      });

      hideUserModalonFinish();
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
  const hideUserModal = () => {
    setOpen(false);
  };
  const rowSelection = {
    onChange: (selectedRowKeys, selectedRows) => {
      console.log(
        `selectedRowKeys: ${selectedRowKeys}`,
        "selectedRows: ",
        selectedRows
      );
    },
    onSelect: (record, selected, selectedRows) => {
      console.log(record, selected, selectedRows);
    },
    onSelectAll: (selected, selectedRows, changeRows) => {
      console.log(selected, selectedRows, changeRows);
    },
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
  const getAncestorsdb = (array) => {
    if (typeof array != "undefined") {
      for (let i = 0; i < array.length; i++) {
        array[i].key = array[i].DeptID;

        if (array[i].children?.length > 0) {
          getAncestors(array[i].children);
        }
      }
    }
    return array;
  };
  const hideUserModalonFinish = () => {
    setOpen(false);
    setcallback(!callback);
  };
  const handleEditButtonClick = async (record) => {
    setrecordDept(record);
    console.log(record);
    setOpen(true);
  };
  const ModalForm = ({ open, onCancel }) => {
    const [valuetree, setValuetree] = useState();
    const onChange1 = (newValue) => {
      setValuetree(newValue);
    };

    const [form] = Form.useForm();

    useEffect(() => {
      form.setFieldsValue({
        Name: recordDept.Name,
        Note: recordDept.Note,
        Status: recordDept.Status,
        pDeptID: recordDept.pDeptID,
        DeptLevel: recordDept.DeptLevel,
        DeptID: recordDept.DeptID,
      });
    }, [recordDept]);

    useResetFormOnCloseModal({
      form,
      open,
    });
    const onOk = () => {
      form.submit();
    };

    const editpos = async (data) => {
      console.log(data);
      var editdata = await putData("update-department", {
        deptID: recordDept.DeptID,
        nameDeptID: data.Name,
        deptLevel: data.DeptLevel,
        pDeptID: data.pDeptID,
        deptMng: 0,
        status: data.status,
        note: data.Note,
      });

      if (editdata.isSuccess === 1) {
        toast.success("Cập nhật thành công \n" + editdata.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });

        hideUserModalonFinish();
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
        title="CẬP NHẬT PHÒNG BAN"
        onOk={onOk}
        okText="Lưu"
        cancelText="Hủy"
        open={open}
        onCancel={onCancel}
      >
        <Form
          form={form}
          name="basic"
          onFinish={editpos}
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
          <Form.Item name="Note" label="Ghi chú">
            <Input />
          </Form.Item>
          <Form.Item
            name="Status"
            rules={[
              {
                required: true,
                message: "Không được để trống",
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
            <Input type="number" />
            {/* <div className="p-2 ">
              
            </div> */}
          </Form.Item>
          <Form.Item
            name="pDeptID"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
            label="Trực Thuộc Phòng Ban"
          >
            <TreeSelect
              showSearch
              style={{
                width: "100%",
              }}
              value={valuetree}
              dropdownStyle={{
                maxHeight: 400,
                overflow: "auto",
              }}
              placeholder="Please select"
              treeDefaultExpandAll
              onChange={onChange1}
              treeData={dbTree}
            />
          </Form.Item>

          <Form.Item label="Trực Thuộc Đơn Vị Bộ Phận" name="DeptLevel">
            <Select
              options={listDeptlv?.reduce(
                (arr, d) =>
                  (arr = [...arr, { value: d.DLvlCode, label: d.DLvlName }]),
                []
              )}
            ></Select>
          </Form.Item>
        </Form>
      </Modal>
    );
  };

  return (
    <>
      <div className="pt-2">
        <Table
          columns={columns}
          // rowSelection={{
          //   ...rowSelection,
          // }}
          dataSource={dataSource}
        />
        <ModalForm open={open} onCancel={hideUserModal} />
      </div>
    </>
  );
};
export default Treedata2;
