import Cookies from "js-cookie";
import Loading from "../common/loading/Loading";
import React, { useState, useEffect, useCallback, useRef } from "react";

import Treedata2 from "./Treedata2";
import { toast } from "react-toastify";
import { getData, postData } from "../../services/user.service";
import {
  Select,
  TreeSelect,
  Button,
  Form,
  Input,
  InputNumber,
  Modal,
} from "antd";

//import "./treedata.css";

let emID = Cookies.get("empid");

const Department = () => {
  const [dbTree, setdbTree] = useState([]);

  const [open, setOpen] = useState(false);

  const [listDeptlv, setlistDeptlv] = useState([]);
  const [IsLoading, setIsLoading] = useState(false);
  const [callback, setcallback] = useState(false);

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      let data = await getData("get-department-tree?deptID=tg");

      setdbTree(getAncestors(data.rData));

      let datalistDept = await getData("get-deptlevel");

      setlistDeptlv(datalistDept.rData);
      setIsLoading(false);
    })();
  }, [callback]);

  const getAncestors = (array) => {
    if (typeof array != "undefined") {
      for (let i = 0; i < array.length; i++) {
        array[i].key = array[i].DeptID;

        if (array[i].children?.length > 0) {
          getAncestors(array[i].children);
        }
      }
    }
    return array;
  }; // convert data them key vaof

  const showUserModal = () => {
    setOpen(true);
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
    useResetFormOnCloseModal({
      form,
      open,
    });
    const onOk = () => {
      form.submit();
    };

    const create = async (data) => {
      console.log(data);

      var create = await postData("import-department", {
        name_deptID: data.DLvlName,
        deptlevel: data.deplv,
        pDeptID: data.pDep,
        note: data.Note,
      });

      if (create.isSuccess === 1) {
        toast.success("Thêm mới thành công \n" + create.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });

        hideUserModal();
        setcallback(!callback);
      } else {
        console.log(create);
        toast.error("Thêm mới thất bại Lỗi: \n" + create.rMsg, {
          autoClose: 2000,
          className: "",
          position: "top-center",
          theme: "colored",
        });
      }
    };
    return (
      <Modal
        title=" THÊM MỚI PHÒNG BAN"
        open={open}
        onOk={onOk}
        okText="Lưu"
        cancelText="Hủy"
        onCancel={onCancel}
      >
        <Form form={form} onFinish={create} layout="vertical" name="userForm">
          <div className="d-flex justify-content-sm-between">
            <Form.Item
              name="DLvlName"
              label="Tên phòng ban"
              rules={[
                {
                  required: true,
                  message: "không được để trống",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item name="Note" label="Ghi chú">
              <Input />
            </Form.Item>
          </div>
          <div>
            <Form.Item
              name="deplv"
              label="Trực thuộc ĐV/BP "
              rules={[
                {
                  required: true,
                  message: "không được để trống",
                },
              ]}
            >
              <Select
                options={listDeptlv?.reduce(
                  (arr, d) =>
                    (arr = [...arr, { value: d.DLvlCode, label: d.DLvlName }]),
                  []
                )}
              ></Select>
            </Form.Item>
          </div>
          <div>
            <Form.Item
              name="pDep"
              label="Trực thuộc phòng ban "
              rules={[
                {
                  required: true,
                  message: "không được để trống",
                },
              ]}
            >
              <TreeSelect treeData={dbTree} treeDefaultExpandAll />
            </Form.Item>
          </div>
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
              <div style={{ overflowY: "auto", overflowX: "hidden" }}>
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
                        <h3> DANH SÁCH CÁC PHÒNG BAN</h3>
                      </div>

                      <div className="pt-1 ">
                        {/* style={{ alignSelf: "end" }} */}

                        <Button
                          className="btn btn-sm btn-success mr-3 mb-2"
                          onClick={showUserModal}
                        >
                          <i className="fas fa-plus" /> Thêm
                        </Button>
                      </div>
                    </div>
                  </div>
                  <div
                    className="card-body m-0 p-0 "
                    style={{ height: "88vh" }}
                  >
                    <div>
                      {/* <Treedata datatree={summaryData} /> */}
                      <Treedata2
                        data={dbTree}
                        callback={callback}
                        setcallback={setcallback}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
      <ModalForm open={open} onCancel={hideUserModal} />
    </>
  );
};
export default Department;
