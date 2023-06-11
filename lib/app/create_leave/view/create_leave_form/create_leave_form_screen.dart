import 'package:find_dropdown/find_dropdown.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/controller/create_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/of_subordinates_model.dart';

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
                child: Form(
                  autovalidateMode: AutovalidateMode.always,
                  key: controller.formKeyCreateLetter,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Obx(() {
                        return controller.isUserInfo.value
                            ? Column(
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
                                              title:
                                                  "Hướng Dẫn Quy Định/Quy Trình",
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
                                    content:
                                        "${controller.userName.value.empID}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Họ và Tên",
                                    content:
                                        "${controller.userName.value.lastName} ${controller.userName.value.firstName}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Ngày vào",
                                    content: day.format(
                                      DateTime.parse(
                                        controller.userName.value.comeDate
                                            .toString(),
                                      ),
                                    ),
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Đ.Vị/B.Phận",
                                    content:
                                        "${controller.userName.value.deptID}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Chức vụ",
                                    content:
                                        "${controller.userName.value.jPLevelName}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Vị trí CV",
                                    content:
                                        "${controller.userName.value.jobpositionName}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Phép năm hiện có *",
                                    content: controller
                                                .userName.value.annualLeave !=
                                            null
                                        ? "${controller.userName.value.annualLeave}"
                                        : "0",
                                    size: size,
                                  ),
                                ],
                              )
                            : Column();
                      }),
                      Column(
                        children: [
                          _buildLoaiPhep(size),
                          _listCustomer(size),
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
                            maxLines: 3,
                            height: 120,
                            controller: controller.addressController,
                            validator: null,
                          ),
                          const SizedBox(height: 15),
                          SizedBox(
                            height: 70,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                                          .formKeyCreateLetter.currentState!
                                          .validate();
                                      if (!validate) {
                                        controller.postRegister(
                                          emplid: int.parse(controller
                                              .selectMember.value
                                              .toString()),
                                          type: int.parse(controller
                                              .selectedValue.value
                                              .toString()),
                                          reason:
                                              controller.reasonController.text,
                                          startdate:
                                              controller.timeController.text,
                                          period: double.parse(
                                              controller.dayController.text),
                                          address:
                                              controller.addressController.text,
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
                                      // print(controller.selectedValue.value);
                                      var validate = controller
                                          .formKeyCreateLetter.currentState!
                                          .validate();
                                      if (!validate) {
                                        print(controller.selectedValue.value);
                                        // If the form is valid, display a snackbar. In the real world,
                                        // you'd often call a server or save the information in a database.
                                        controller.postRegister(
                                          emplid: int.parse(controller
                                              .selectMember.value
                                              .toString()),
                                          type: int.parse(controller
                                              .selectedValue.value
                                              .toString()),
                                          reason:
                                              controller.reasonController.text,
                                          startdate:
                                              controller.timeController.text,
                                          period: double.parse(
                                              controller.dayController.text),
                                          address:
                                              controller.addressController.text,
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
                        ],
                      ),
                      Container(
                        height: 80,
                      ),
                    ],
                  ),
                ),
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
                  keyboardType: TextInputType.text,
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
                    // border: InputBorder.none,
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
                      keyboardType: TextInputType.number,
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

  Widget _listCustomer(Size size) {
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
                  child: const Text("MSNV")),
            ),
            Expanded(
              flex: 5,
              child: Container(
                // margin: const EdgeInsets.only(top: 10),
                child: FindDropdown<OfSubordinatesModel>(
                  validate: (value) {
                    // ignore: unrelated_type_equality_checks
                    if (value == "" || value == 0 || value == null) {
                      return 'Chọn nhân viên !';
                    }
                    return null;
                  },
                  onFind: (String filter) => controller.getDataCustomer(filter),
                  onChanged: (OfSubordinatesModel? data) {
                    controller.selectMember.value = data!.empID!;
                  },
                  dropdownBuilder:
                      (BuildContext context, OfSubordinatesModel? item) {
                    return Container(
                      height: 40,
                      decoration: BoxDecoration(
                        border:
                            Border.all(color: Theme.of(context).dividerColor),
                        borderRadius: BorderRadius.circular(5),
                        color: Colors.white,
                      ),
                      child: (item == null)
                          ? Row(
                              children: const [
                                Padding(
                                  padding: EdgeInsets.only(left: 10),
                                  child: Text(
                                    "Chọn nhân viên",
                                    style: TextStyle(fontSize: 15),
                                  ),
                                ),
                                Icon(
                                  Icons.arrow_drop_down_outlined,
                                  color: Colors.black,
                                )
                              ],
                            )
                          : Row(
                              children: [
                                Padding(
                                  padding: const EdgeInsets.only(left: 10),
                                  child: Text(
                                    "${item.lastName!} ${item.firstName}",
                                    style: const TextStyle(fontSize: 15),
                                  ),
                                ),
                                const Icon(
                                  Icons.arrow_drop_down_outlined,
                                  color: Colors.black,
                                )
                              ],
                            ),
                    );
                  },
                  dropdownItemBuilder: (BuildContext context,
                      OfSubordinatesModel item, bool isSelected) {
                    return Container(
                      decoration: !isSelected
                          ? null
                          : BoxDecoration(
                              border: Border.all(
                                  color: Theme.of(context).primaryColor),
                              borderRadius: BorderRadius.circular(5),
                              color: Colors.white,
                            ),
                      child: Card(
                        shape: OutlineInputBorder(
                          borderSide: const BorderSide(
                            color: Colors.orangeAccent,
                          ),
                          borderRadius: BorderRadius.circular(5),
                        ),
                        child: ListTile(
                          selected: isSelected,
                          title: Text(
                            "${item.lastName!} ${item.firstName}",
                            style: const TextStyle(fontSize: 15),
                          ),
                          subtitle: Text(
                            "${item.empID!}",
                            style: const TextStyle(fontSize: 15),
                          ),
                        ),
                      ),
                    );
                  },
                ),
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
              flex: 5,
              child: FindDropdown<ListOffTypeModel>(
                validate: (value) {
                  // ignore: unrelated_type_equality_checks
                  if (value == "" || value == 0 || value == null) {
                    return 'Chọn loại phép !';
                  }
                  return null;
                },
                onFind: (String filter) => controller.getTypeOff(filter),
                onChanged: (ListOffTypeModel? data) {
                  controller.selectedValue.value = int.parse(data!.offTypeID!);
                  controller.nameType.value = data.note!;
                },
                dropdownBuilder:
                    (BuildContext context, ListOffTypeModel? item) {
                  return Container(
                    height: 40,
                    decoration: BoxDecoration(
                      border: Border.all(color: Theme.of(context).dividerColor),
                      borderRadius: BorderRadius.circular(5),
                      color: Colors.white,
                    ),
                    child: (item?.note == null)
                        ? Row(
                            children: const [
                              Padding(
                                padding: EdgeInsets.only(left: 10),
                                child: Text(
                                  "Chọn loại phép",
                                  style: TextStyle(fontSize: 15),
                                ),
                              ),
                              Icon(
                                Icons.arrow_drop_down_outlined,
                                color: Colors.black,
                              )
                            ],
                          )
                        : Row(
                            children: [
                              Padding(
                                padding: const EdgeInsets.only(left: 10),
                                child: Text(
                                  item!.note!,
                                  style: const TextStyle(fontSize: 15),
                                ),
                              ),
                              const Icon(
                                Icons.arrow_drop_down_outlined,
                                color: Colors.black,
                              )
                            ],
                          ),
                  );
                },
                dropdownItemBuilder: (BuildContext context,
                    ListOffTypeModel item, bool isSelected) {
                  return Container(
                    decoration: !isSelected
                        ? null
                        : BoxDecoration(
                            border: Border.all(
                                color: Theme.of(context).primaryColor),
                            borderRadius: BorderRadius.circular(5),
                            color: Colors.white,
                          ),
                    child: Card(
                      shape: OutlineInputBorder(
                        borderSide: const BorderSide(
                          color: Colors.orangeAccent,
                        ),
                        borderRadius: BorderRadius.circular(5),
                      ),
                      child: ListTile(
                        selected: isSelected,
                        title: Text(
                          item.note!,
                          style: const TextStyle(fontSize: 15),
                        ),
                        subtitle: Text(
                          item.name!,
                          style: const TextStyle(fontSize: 15),
                        ),
                      ),
                    ),
                  );
                },
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
