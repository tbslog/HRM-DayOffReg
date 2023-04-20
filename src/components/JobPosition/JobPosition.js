import { SearchOutlined } from "@ant-design/icons";

import { useRef, useState, useEffect } from "react";
import Highlighter from "react-highlight-words";
import { getData, postData, putData } from "../../services/user.service";
import Loading from "../common/loading/Loading";
import { toast } from "react-toastify";
import {
  Button,
  Input,
  Space,
  Table,
  Modal,
  Select,
  TreeSelect,
  Popconfirm,
  Form,
  InputNumber,
} from "antd";
import { set } from "react-hook-form";

const JobPosition = () => {
  const [searchText, setSearchText] = useState("");
  const [searchedColumn, setSearchedColumn] = useState("");
  const searchInput = useRef(null);
  const [data, setData] = useState([]);
  const [IsLoading, setIsLoading] = useState(false);
  const [listjptlv, setlistjptlv] = useState([]);
  const [listDep, setlistlistDep] = useState([]);
  const [listjpname, setlistjpname] = useState([]);
  const [open, setOpen] = useState(false);
  const [openCreate, setOpenCreate] = useState(false);
  const [jobPos, setJobPos] = useState({});
  const [dbTree, setdbTree] = useState([]);
  const [callback, setcallback] = useState(false);

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData("get-jobPosition");
      setData(data.rData);
      console.log(data);

      let datalistjp = await getData("get-jplevel");
      setlistjptlv(datalistjp.rData);

      let datalistDept = await getData("get-department");
      setlistlistDep(datalistDept.rData);

      let datalistjpname = await getData("get-jpname");

      setlistjpname(datalistjpname.rData);

      let datat = await getData("get-department-tree?deptID=tg");

      setdbTree(getAncestors(datat.rData));

      setIsLoading(false);
    })();
  }, [callback]);

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
  }; // thêm value và title vào dbtree

  const handleSearch = (selectedKeys, confirm, dataIndex) => {
    confirm();
    setSearchText(selectedKeys[0]);
    setSearchedColumn(dataIndex);
  };
  const handleReset = (clearFilters) => {
    clearFilters();
    setSearchText("");
  };
  const getColumnSearchProps = (dataIndex) => ({
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters,
      close,
    }) => (
      <div
        style={{
          padding: 8,
        }}
        onKeyDown={(e) => e.stopPropagation()}
      >
        <Input
          ref={searchInput}
          placeholder={`Search ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={(e) =>
            setSelectedKeys(e.target.value ? [e.target.value] : [])
          }
          onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
          style={{
            marginBottom: 8,
            display: "block",
          }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
            icon={<SearchOutlined />}
            size="small"
            style={{
              width: 90,
            }}
          >
            Tìm kiếm
          </Button>
          <Button
            onClick={() => clearFilters && handleReset(clearFilters)}
            size="small"
            style={{
              width: 90,
            }}
          >
            Reset
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              confirm({
                closeDropdown: false,
              });
              setSearchText(selectedKeys[0]);
              setSearchedColumn(dataIndex);
            }}
          >
            Lọc
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              close();
            }}
          >
            Đóng
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered) => (
      <SearchOutlined
        style={{
          color: filtered ? "#1890ff" : undefined,
        }}
      />
    ),
    onFilter: (value, record) =>
      record[dataIndex].toString().toLowerCase().includes(value.toLowerCase()),
    onFilterDropdownOpenChange: (visible) => {
      if (visible) {
        setTimeout(() => searchInput.current?.select(), 100);
      }
    },
    render: (text) =>
      searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{
            backgroundColor: "#ffc069",
            padding: 0,
          }}
          searchWords={[searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ""}
        />
      ) : (
        text
      ),
  });
  const columns = [
    {
      title: "ID",
      dataIndex: "JobPosID",
      key: "JobPosID",
      width: "8%",

      ...getColumnSearchProps("JobPosID"),
      sorter: (a, b) => a.JobPosID - b.JobPosID,
      sortDirections: ["descend", "ascend"],
    },
    {
      title: "Tên",
      dataIndex: "Name",
      key: "Name",

      ...getColumnSearchProps("Name"),
      sorter: (a, b) => a.Name.length - b.Name.length,
      sortDirections: ["descend", "ascend"],
    },
    {
      title: "Cấp bậc",
      dataIndex: "JPLevel",
      key: "v",

      ...getColumnSearchProps("JPLevel"),
      render: (record) => <> {checkJPLevel(record)}</>,
    },
    {
      title: "Phòng ban",
      dataIndex: "DeptID",
      key: "DeptID",

      ...getColumnSearchProps("DeptID"),
      render: (record) => <> {checkDep(record)}</>,
    },
    {
      title: "Tình trạng",
      dataIndex: "Status",
      key: "Status",
      width: "10%",

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
      console.log(id);
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
          title="Xóa Vị Trí Công Việc"
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
    var editdata = await putData(
      `delete-jobPosition?jobPosID=${record.JobPosID}`
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
  const checkJPLevel = (id) => {
    const result = listjptlv?.find((d) => d.JPLevelID === id);

    let a = result?.Name;
    return a;
  };
  const checkDep = (id) => {
    const result = listDep?.find((d) => d.DeptID === id);

    let a = result?.Name;
    return a;
  };
  const hideUserModal = () => {
    setOpen(false);
  };
  const hideUserModalCreate = () => {
    setOpenCreate(false);
  };
  const hideUserModalonFinish = () => {
    setOpen(false);
    (async () => {
      setIsLoading(true);
      let data = await getData("get-jobPosition");
      setData(data.rData);
      setIsLoading(false);
      setOpenCreate(false);
    })();
  };
  const handleEditButtonClick = async (record) => {
    setJobPos(record);
    console.log(record);
    setOpen(true);
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
  const handleCreate = async () => {
    setOpenCreate(true);
  };

  const ModalFormAdd = ({ open, onCancel }) => {
    const [valuetree, setValuetree] = useState();
    const onChange1 = (newValue) => {
      setValuetree(newValue);
    };

    const [form] = Form.useForm();
    useResetFormOnCloseModal({
      form,
      open,
    });
    const onOk = () => {
      form.submit();
    };
    const create = async (data) => {
      console.log(data);

      var createjob = await postData("import-jobPosition", {
        jplevel: data.JPLevel,
        jpname: data.jpname,
        deptID: data.DeptID,
        note: data.Note,
      });
      console.log(createjob);
      if (createjob.isSuccess === 1) {
        toast.success("Thêm mới thành công \n" + createjob.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });

        hideUserModalonFinish();
      } else {
        console.log(createjob);
        toast.error("Thêm mới thất bại Lỗi: \n" + createjob.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
      }
    };
    return (
      <Modal
        title="THÊM VỊ TRÍ CHỨC VỤ"
        onOk={onOk}
        okText="Lưu"
        cancelText="Hủy"
        open={openCreate}
        onCancel={onCancel}
      >
        <Form
          form={form}
          name="basic"
          onFinish={create}
          layout="vertical"
          //onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item
            name="DeptID"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
            label="Phòng Ban"
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
              placeholder="Chọn"
              treeDefaultExpandAll
              onChange={onChange1}
              treeData={dbTree}
            />
          </Form.Item>

          <Form.Item
            label="Chức Danh"
            name="JPLevel"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
          >
            <Select
              options={listjptlv?.reduce(
                (arr, d) =>
                  (arr = [...arr, { value: d.JPLevelID, label: d.Name }]),
                []
              )}
            ></Select>
          </Form.Item>
          <Form.Item
            label="Công Việc"
            name="jpname"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
          >
            <Select
              options={listjpname?.reduce(
                (arr, d) =>
                  (arr = [...arr, { value: d.JPNameID, label: d.Name }]),
                []
              )}
            ></Select>
          </Form.Item>
          <Form.Item name="Note" label="Ghi Chú">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    );
  };

  const ModalForm = ({ open, onCancel }) => {
    const [valuetree, setValuetree] = useState();
    const onChange1 = (newValue) => {
      setValuetree(newValue);
    };

    const [form] = Form.useForm();

    useEffect(() => {
      form.setFieldsValue({
        DeptID: jobPos.DeptID,
        JPLevel: jobPos.JPLevel,
        JPName: jobPos.JPName,
        JobPosID: jobPos.JobPosID,
        Name: jobPos.Name,
        Note: jobPos.Note,
        Status: jobPos.Status,
      });
    }, [jobPos]);

    useResetFormOnCloseModal({
      form,
      open,
    });
    const onOk = () => {
      form.submit();
    };

    const editpos = async (data) => {
      console.log(data);
      var editdata = await putData("update-jobPosition", {
        jobPosID: data.JobPosID,
        name: data.Name,
        jplevel: data.JPLevel,
        jpname: data.JPName,
        deptID: data.DeptID,
        status: data.Status,
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
        title="CẬP NHẬT VỊ TRÍ CHỨC VỤ"
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
          <Form.Item name="JobPosID" label="Mã">
            <Input readOnly />
          </Form.Item>
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
            name="DeptID"
            rules={[
              {
                required: true,
                message: "Không được để trống",
              },
            ]}
            label="Phòng Ban"
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

          <Form.Item label="Chức Danh" name="JPLevel">
            <Select
              options={listjptlv?.reduce(
                (arr, d) =>
                  (arr = [...arr, { value: d.JPLevelID, label: d.Name }]),
                []
              )}
            ></Select>
          </Form.Item>
          <Form.Item name="Note" label="Ghi Chú">
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
        </Form>
      </Modal>
    );
  };
  return (
    <>
      <div className="content-wrapper ">
        {IsLoading ? (
          <Loading />
        ) : (
          <section className="content" style={{ height: "100vh" }}>
            <div className="card p-3 mt-2 mb-3 " style={{ height: "100%" }}>
              <div style={{ overflowY: "hidden", overflowX: "hidden" }}>
                <div
                  className="tab-content profile-tab ml-4"
                  id="myTabContent"
                  style={{ maxWidth: "100%", minWidth: "63%" }}
                >
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
                        <h3> DANH SÁCH VỊ TRÍ CÔNG VIỆC</h3>
                      </div>

                      <div className="pt-1 ">
                        {/* style={{ alignSelf: "end" }} */}

                        <Button
                          className="btn btn-sm btn-success mr-3 mb-2"
                          onClick={() => handleCreate()}
                        >
                          <i className="fas fa-plus" /> Thêm
                        </Button>
                      </div>
                    </div>
                  </div>
                  <div
                    className="card-body m-0 p-0 "
                    style={{ height: "72vh" }}
                  >
                    <div>
                      {/* <Treedata datatree={summaryData} /> */}
                      <Table
                        columns={columns}
                        dataSource={data}
                        size="middle"
                        scroll={{
                          x: 1000,
                          y: 460,
                        }}
                        pagination
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <ModalForm open={open} onCancel={hideUserModal} />
            <ModalFormAdd open={openCreate} onCancel={hideUserModalCreate} />
          </section>
        )}
      </div>
    </>
  );
};
export default JobPosition;
