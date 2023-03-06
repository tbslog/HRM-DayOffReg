import 'package:dropdown_search/dropdown_search.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/controller/create_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';

class CreateLeaveFormScreen extends GetView<CreateLeaveFormController> {
  const CreateLeaveFormScreen({super.key});
  final String routes = "/CREATE_LEAVE_FORM_SCREEN";

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    var timeNow = DateTime.now();
    var day = DateFormat("dd-MM-yyyy");

    return GetBuilder<CreateLeaveFormController>(
        init: CreateLeaveFormController(),
        builder: (controller) => SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: Container(
                padding: EdgeInsets.only(
                  bottom: MediaQuery.of(context).viewInsets.bottom,
                  left: 10,
                  right: 10,
                ),
                child: FutureBuilder(
                    future: controller.getInfo(),
                    builder: (context, snapshot) {
                      if (snapshot.hasData) {
                        var items = snapshot.data as UserModel;
                        return Form(
                          autovalidateMode: AutovalidateMode.always,
                          key: controller.formKey,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            children: [
                              Container(
                                padding: const EdgeInsets.only(right: 5),
                                height: 40,
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    InkWell(
                                      onTap: () {
                                        Get.defaultDialog(
                                          barrierDismissible: false,
                                          title: "Hướng Dẫn Quy Định/Quy Trình",
                                          titleStyle: const TextStyle(
                                            fontSize: 14,
                                          ),
                                          content: SizedBox(
                                            height: size.height * 0.6,
                                            width: size.width * 0.9,
                                            child: Image.asset(
                                                "assets/images/QuyDinh.png"),
                                          ),
                                          confirm: TextButton(
                                            onPressed: () {
                                              Get.back();
                                            },
                                            child: const Text(
                                              "Xác nhận",
                                              style: TextStyle(
                                                color: Colors.orangeAccent,
                                              ),
                                            ),
                                          ),
                                        );
                                      },
                                      child: const Text(
                                        "HD Quy định/Quy trình !",
                                        style: TextStyle(
                                          color: Colors.green,
                                        ),
                                      ),
                                    )
                                  ],
                                ),
                              ),
                              _buildFormText(
                                title: "MSNV",
                                content: "${items.empID}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Họ và Tên",
                                content: "${items.lastName} ${items.firstName}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Ngày vào",
                                content: day.format(
                                  DateTime.parse(
                                    items.comeDate.toString(),
                                  ),
                                ),
                                size: size,
                              ),
                              _buildFormText(
                                title: "Đ.Vị/B.Phận",
                                content: "${items.deptID}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Chức vụ",
                                content: "${items.jPLevelName}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Vị trí CV",
                                content: "${items.jobpositionName}",
                                size: size,
                              ),
                              _buildLoaiPhep(size),
                              _buildDateTime(
                                title: "Bắt đầu nghỉ từ *",
                                content: day.format(timeNow),
                                size: size,
                                controller: controller.timeController,
                                hintText: day.format(
                                  DateTime.parse(
                                    timeNow.toString(),
                                  ),
                                ),
                                onTap: () {
                                  controller.selectDate();
                                },
                              ),
                              _buildFormText(
                                title: "Phép năm hiện có *",
                                content: items.annualLeave != null
                                    ? "${items.annualLeave}"
                                    : "0",
                                size: size,
                              ),
                              _buildDayFree(
                                size: size,
                                text: "Số ngày nghỉ",
                              ),
                              _buildReason(
                                size: size,
                                hintText: "Nhập lý do",
                                title: "Lý do nghỉ phép *",
                                maxLines: 3,
                                height: 120,
                                controller: controller.reasonController,
                                validator: (value) {
                                  if (value == null || value == "") {
                                    return "Nhập lý do";
                                  }
                                  return "";
                                },
                              ),
                              _buildReason(
                                size: size,
                                hintText: "Nhập địa chỉ",
                                title: "Địa chỉ nghỉ phép ",
                                maxLines: 2,
                                height: 80,
                                controller: controller.addressController,
                                validator: null,
                              ),
                              const SizedBox(height: 15),
                              SizedBox(
                                height: 70,
                                child: Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceAround,
                                  children: [
                                    SizedBox(
                                      width: size.width * 0.25,
                                      height: size.width * 0.1,
                                      child: TextButton(
                                        style: ButtonStyle(
                                          backgroundColor:
                                              MaterialStateProperty.all<Color>(
                                            Colors.yellow.shade800,
                                          ),
                                        ),
                                        onPressed: () {
                                          var validate = controller
                                              .formKey.currentState!
                                              .validate();
                                          if (!validate &&
                                              controller.selectedLoaiphep
                                                      .toString() !=
                                                  "") {
                                            controller.postRegister(
                                              type: int.parse(controller
                                                  .selectedLoaiphep
                                                  .toString()),
                                              reason: controller
                                                  .reasonController.text,
                                              startdate: controller
                                                  .timeController.text,
                                              period: int.parse(controller
                                                  .dayController.text),
                                              address: controller
                                                  .addressController.text,
                                              command: 0,
                                            );
                                          }
                                        },
                                        child: const Text(
                                          "Lưu",
                                          style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 16,
                                          ),
                                        ),
                                      ),
                                    ),
                                    SizedBox(
                                      width: size.width * 0.25,
                                      height: size.width * 0.1,
                                      child: TextButton(
                                        style: ButtonStyle(
                                          backgroundColor:
                                              MaterialStateProperty.all<Color>(
                                            Colors.green,
                                          ),
                                        ),
                                        onPressed: () {
                                          var validate = controller
                                              .formKey.currentState!
                                              .validate();
                                          if (!validate &&
                                              controller.selectedLoaiphep
                                                      .toString() !=
                                                  "") {
                                            // If the form is valid, display a snackbar. In the real world,
                                            // you'd often call a server or save the information in a database.
                                            controller.postRegister(
                                              type: int.parse(controller
                                                  .selectedLoaiphep
                                                  .toString()),
                                              reason: controller
                                                  .reasonController.text,
                                              startdate: controller
                                                  .timeController.text,
                                              period: int.parse(controller
                                                  .dayController.text),
                                              address: controller
                                                  .addressController.text,
                                              command: 1,
                                            );
                                          }
                                        },
                                        child: const Text(
                                          "Gửi đơn",
                                          style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 16,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Container(
                                height: 80,
                              ),
                            ],
                          ),
                        );
                      }
                      return const Center(
                        child: CircularProgressIndicator(
                          color: Colors.orangeAccent,
                        ),
                      );
                    }),
              ),
            ));
  }

  Widget _buildReason({
    required Size size,
    required String title,
    required String hintText,
    required int maxLines,
    required double height,
    required TextEditingController controller,
    required String Function(String?)? validator,
  }) {
    return Card(
      child: SizedBox(
        height: height,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Expanded(
              flex: 1,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Padding(
                    padding:
                        EdgeInsets.symmetric(horizontal: size.width * 0.05),
                    child: Text(
                      title,
                      textAlign: TextAlign.left,
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              flex: 3,
              child: Container(
                // height: 45,
                width: size.width - 20,
                padding: EdgeInsets.symmetric(
                  horizontal: size.width * 0.05,
                  vertical: 10,
                ),
                child: TextFormField(
                  validator: validator,
                  maxLines: maxLines,
                  controller: controller,
                  decoration: InputDecoration(
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(
                        color: Colors.black.withOpacity(0.2),
                        width: 1,
                      ),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(
                        color: Colors.black.withOpacity(0.2),
                        width: 1,
                      ),
                    ),
                    hintMaxLines: 3,
                    contentPadding: const EdgeInsets.only(
                      top: 5,
                      left: 5,
                    ),
                    hintText: hintText,
                    border: InputBorder.none,
                    isDense: true,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDayFree({required Size size, required String text}) {
    return Card(
      child: SizedBox(
        height: 60,
        child: Row(
          children: [
            Expanded(
              flex: 5,
              child: Padding(
                padding: EdgeInsets.only(
                  left: size.width * 0.05,
                ),
                child: Text(text),
              ),
            ),
            Expanded(
              flex: 5,
              child: Row(
                children: [
                  Container(
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 1,
                        color: Colors.white,
                      ),
                      color: Colors.white,
                    ),
                    height: 35,
                    width: size.width * 0.35,
                    // margin: EdgeInsets.symmetric(vertical: size.height * 0.02),
                    child: TextFormField(
                      validator: (value) {
                        // ignore: unrelated_type_equality_checks
                        if (value == "" || value == 0 || value == null) {
                          return 'Nhập số ngày !';
                        }
                        return null;
                      },
                      controller: controller.dayController,
                      decoration: const InputDecoration(
                        contentPadding: EdgeInsets.only(
                          top: 5,
                        ),
                        hintMaxLines: 2,
                        hintText: "Nhập số ngày",
                        border: InputBorder.none,
                        isDense: true,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDateTime({
    required String title,
    required String content,
    required Size size,
    required VoidCallback onTap,
    required TextEditingController controller,
    required String hintText,
  }) {
    return Card(
      child: SizedBox(
        height: 60,
        child: Row(
          children: [
            Expanded(
              flex: 5,
              child: Padding(
                padding: EdgeInsets.only(
                  left: size.width * 0.05,
                ),
                child: Text(title),
              ),
            ),
            Expanded(
              flex: 5,
              child: Row(
                children: [
                  Container(
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 1,
                        // color: Color(0xFFF3BD60),
                        color: Colors.white,
                      ),
                      color: Colors.white,
                    ),
                    height: 35,
                    width: size.width * 0.35,
                    // margin: EdgeInsets.symmetric(vertical: size.height * 0.02),
                    child: TextFormField(
                      validator: (value) {
                        if (value == null || value == "") {
                          return 'Chọn ngày';
                        }
                        return null;
                      },
                      onTap: onTap,
                      controller: controller,
                      decoration: InputDecoration(
                        contentPadding: const EdgeInsets.only(top: 5),
                        hintText: hintText,
                        border: InputBorder.none,
                        isDense: true,
                        icon: const Icon(
                          Icons.calendar_month,
                          color: Colors.orangeAccent,
                          size: 25,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLoaiPhep(Size size) {
    return Card(
      child: SizedBox(
        height: 70,
        child: Row(
          children: [
            Expanded(
              flex: 5,
              child: Padding(
                  padding: EdgeInsets.only(
                    left: size.width * 0.05,
                  ),
                  child: const Text("Loại phép")),
            ),
            Expanded(
              flex: 6,
              child: Theme(
                data: ThemeData(
                  inputDecorationTheme:
                      const InputDecorationTheme(border: InputBorder.none),
                ),
                child: DropdownSearch<ListOffTypeModel>(
                  validator: (value) {
                    // ignore: unrelated_type_equality_checks
                    if (value == null || value == "") {
                      return 'Chọn loại phép';
                    }
                    return null;
                  },
                  asyncItems: (String? query) {
                    return controller.getTypeOff(query);
                  },
                  popupProps: PopupPropsMultiSelection.dialog(
                    showSelectedItems: true,
                    itemBuilder: _customPopupItemBuilderExample2,
                    showSearchBox: true,
                  ),
                  compareFn: (item, sItem) {
                    return item.note == sItem.note && item.name == sItem.name;
                  },
                  onChanged: (ListOffTypeModel? newValue) {
                    controller.selectedLoaiphep =
                        newValue!.offTypeID.toString();
                  },
                  dropdownDecoratorProps: const DropDownDecoratorProps(
                    dropdownSearchDecoration: InputDecoration(
                      hintText: "Chọn loại phép",
                      filled: true,
                      iconColor: Color(0xFFF3BD60),
                      focusColor: Color(0xFFF3BD60),
                      fillColor: Colors.white,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _customPopupItemBuilderExample2(
    BuildContext context,
    ListOffTypeModel? item,
    bool isSelected,
  ) {
    return Card(
      child: ListTile(
        style: ListTileStyle.drawer,
        focusColor: Colors.white,
        leading: Text("${item?.offTypeID}"),
        title: Text(
          "${item?.note} (${item?.name})",
          style: const TextStyle(color: Colors.blueGrey),
        ),
      ),
    );
  }

  Widget _buildFormText(
      {required String title, required String content, required Size size}) {
    return Card(
      child: SizedBox(
        height: 35,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Expanded(
              flex: 5,
              child: Padding(
                  padding: EdgeInsets.only(
                    left: size.width * 0.05,
                  ),
                  child: Text(title)),
            ),
            Expanded(
              flex: 5,
              child: Padding(
                padding: const EdgeInsets.only(left: 5),
                child: Text(content),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
