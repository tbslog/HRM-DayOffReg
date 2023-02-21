import 'package:dropdown_search/dropdown_search.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/single_view/controller/detail_single_controller.dart';

class DetailSingleView extends GetView<DetailSingleController> {
  const DetailSingleView({super.key});
  final String routes = "/DETAIL_SINGLE_VIEW";

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    var timeNow = DateTime.now();
    var day = DateFormat("dd-MM-yyyy");
    var dayPost = DateFormat("yyyy-MM-dd");
    if (Get.arguments != null && Get.arguments is int) {
      var regID = Get.arguments;
      return GetBuilder<DetailSingleController>(
        init: DetailSingleController(),
        builder: (controller) => Scaffold(
          appBar: AppBar(
            title: Text(
              "Chi tiết đơn xin nghỉ",
              style: TextStyle(
                color: Theme.of(context).primaryColorDark,
              ),
            ),
            centerTitle: true,
            leading: IconButton(
              onPressed: () {
                Get.back();
              },
              icon: Icon(
                Icons.arrow_back_ios_new_outlined,
                color: Theme.of(context).primaryColorDark,
                size: 25,
              ),
            ),
            backgroundColor: Colors.orangeAccent,
          ),
          body: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 15),
              child: FutureBuilder(
                  future: controller.detailSingle(regID: regID),
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      var items = snapshot.data as DetailSingleModel;
                      var detail = items.rData;

                      return detail!.aStatus == 0
                          ? Column(
                              mainAxisAlignment: MainAxisAlignment.start,
                              children: [
                                _buildFormText(
                                    title: "Tình trạng",
                                    content: "Chờ mới",
                                    size: size,
                                    color: Colors.green),
                                _buildFormText(
                                  title: "MSNV",
                                  content: "${detail.empID}",
                                  size: size,
                                  color: Colors.black,
                                ),
                                _buildLoaiPhep(
                                  size,
                                  items,
                                  detail.type == "1"
                                      ? "Phép Năm (PN)"
                                      : detail.type == "2"
                                          ? "Việc Riêng (VR)"
                                          : detail.type == "3"
                                              ? "Bệnh Ốm (BO)"
                                              : detail.type == "4"
                                                  ? "Thai Sản (TS)"
                                                  : detail.type == "5"
                                                      ? "Tai Nạn (TN)"
                                                      : detail.type == "6"
                                                          ? "Chờ Việc (CV)"
                                                          : "Hiếu Hỉ, Tang lễ (HH-TL)",
                                ),
                                _buildDateTime(
                                  title: "Bắt đầu nghỉ từ *",
                                  content: day.format(timeNow),
                                  size: size,
                                  controller: controller.timeController,
                                  hintText: day.format(
                                    DateTime.parse(
                                      detail.startDate.toString(),
                                    ),
                                  ),
                                  onTap: () {
                                    controller.selectDate();
                                  },
                                ),
                                _buildFormText(
                                  title: "Số ngày phép năm hiện có *",
                                  content: "${detail.annualLeave}",
                                  size: size,
                                  color: Colors.black,
                                ),
                                _buildDayFree(size, "${detail.period}"),
                                _buildReason(
                                  size: size,
                                  hintText: "${detail.reason}",
                                  title: "Lý do nghỉ phép *",
                                  maxLines: 3,
                                  height: 120,
                                  controller: controller.reasonController,
                                ),
                                _buildReason(
                                  size: size,
                                  hintText: detail.address == null
                                      ? ""
                                      : detail.address.toString(),
                                  title: "Địa chỉ nghỉ phép *",
                                  maxLines: 3,
                                  height: 80,
                                  controller: controller.addressController,
                                ),
                                const SizedBox(height: 15),
                                SizedBox(
                                  height: 60,
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
                                                MaterialStateProperty.all<
                                                    Color>(
                                              Colors.yellow.shade800,
                                            ),
                                          ),
                                          onPressed: () {
                                            controller.postDetailRegister(
                                              type: controller
                                                          .selectedLoaiPhep ==
                                                      ""
                                                  ? int.parse(
                                                      detail.type.toString())
                                                  : int.parse(controller
                                                      .selectedLoaiPhep),
                                              reason: controller
                                                          .reasonController
                                                          .text ==
                                                      ""
                                                  ? detail.reason.toString()
                                                  : controller
                                                      .reasonController.text,
                                              startdate: controller
                                                          .timeController
                                                          .text ==
                                                      ""
                                                  ? dayPost.format(
                                                      DateTime.parse(
                                                        detail.startDate
                                                            .toString(),
                                                      ),
                                                    )
                                                  : controller
                                                      .dayController.text,
                                              period: controller
                                                          .dayController.text ==
                                                      ""
                                                  ? int.parse(
                                                      detail.period.toString())
                                                  : int.parse(controller
                                                      .dayController.text),
                                              address: controller
                                                          .addressController
                                                          .text ==
                                                      ""
                                                  ? detail.address.toString()
                                                  : controller
                                                      .addressController.text,
                                              command: 0,
                                              regID: regID,
                                            );
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
                                                MaterialStateProperty.all<
                                                    Color>(
                                              Colors.green,
                                            ),
                                          ),
                                          onPressed: () {
                                            controller.postDetailRegister(
                                              type: controller
                                                          .selectedLoaiPhep ==
                                                      ""
                                                  ? int.parse(
                                                      detail.type.toString())
                                                  : int.parse(controller
                                                      .selectedLoaiPhep),
                                              reason: controller
                                                          .reasonController
                                                          .text ==
                                                      ""
                                                  ? detail.reason.toString()
                                                  : controller
                                                      .reasonController.text,
                                              startdate: controller
                                                          .timeController
                                                          .text ==
                                                      ""
                                                  ? dayPost.format(
                                                      DateTime.parse(
                                                        detail.startDate
                                                            .toString(),
                                                      ),
                                                    )
                                                  : controller
                                                      .dayController.text,
                                              period: controller
                                                          .dayController.text ==
                                                      ""
                                                  ? int.parse(
                                                      detail.period.toString())
                                                  : int.parse(controller
                                                      .dayController.text),
                                              address: controller
                                                          .addressController
                                                          .text ==
                                                      ""
                                                  ? detail.address.toString()
                                                  : controller
                                                      .addressController.text,
                                              command: 1,
                                              regID: regID,
                                            );
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
                                  height: 50,
                                ),
                              ],
                            )
                          : detail.aStatus == 1
                              ? Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  children: [
                                    _buildFormStatusText(
                                      title: "Tình trạng",
                                      content: detail.aStatus == 1
                                          ? "Chờ duyệt"
                                          : detail.aStatus == 2
                                              ? "Đã duyệt"
                                              : "Từ chối",
                                      size: size,
                                      color: detail.aStatus == 1
                                          ? Colors.yellow
                                          : detail.aStatus == 2
                                              ? Colors.green
                                              : Colors.red,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "MSNV",
                                      content: "${detail.empID}",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Loại phép",
                                      content: detail.type == "1"
                                          ? "Phép Năm (PN)"
                                          : detail.type == "2"
                                              ? "Việc Riêng (VR)"
                                              : detail.type == "3"
                                                  ? "Bệnh Ốm (BO)"
                                                  : detail.type == "4"
                                                      ? "Thai Sản (TS)"
                                                      : detail.type == "5"
                                                          ? "Tai Nạn (TN)"
                                                          : detail.type == "6"
                                                              ? "Chờ Việc (CV)"
                                                              : "Hiếu Hỉ, Tang lễ (HH-TL)",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Nghỉ bắt đầu từ ngày ",
                                      content: day.format(
                                        DateTime.parse(
                                          detail.startDate.toString(),
                                        ),
                                      ),
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Số ngày nghỉ",
                                      content: "${detail.period}",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Lý do nghỉ phép",
                                      content: "${detail.reason}",
                                      size: size,
                                    ),
                                  ],
                                )
                              : Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  children: [
                                    _buildFormStatusText(
                                      title: "Tình trạng",
                                      content: detail.aStatus == 1
                                          ? "Chờ duyệt"
                                          : detail.aStatus == 2
                                              ? "Đã duyệt"
                                              : "Từ chối",
                                      size: size,
                                      color: detail.aStatus == 1
                                          ? Colors.yellow
                                          : detail.aStatus == 2
                                              ? Colors.green
                                              : Colors.red,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "MSNV",
                                      content: "${detail.empID}",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Loại phép",
                                      content: detail.type == "1"
                                          ? "Phép Năm (PN)"
                                          : detail.type == "2"
                                              ? "Việc Riêng (VR)"
                                              : detail.type == "3"
                                                  ? "Bệnh Ốm (BO)"
                                                  : detail.type == "4"
                                                      ? "Thai Sản (TS)"
                                                      : detail.type == "5"
                                                          ? "Tai Nạn (TN)"
                                                          : detail.type == "6"
                                                              ? "Chờ Việc (CV)"
                                                              : "Hiếu Hỉ, Tang lễ (HH-TL)",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Nghỉ bắt đầu từ ngày ",
                                      content: day.format(
                                        DateTime.parse(
                                          detail.startDate.toString(),
                                        ),
                                      ),
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Số ngày nghỉ",
                                      content: "${detail.period} ngày",
                                      size: size,
                                    ),
                                    _buildFormText(
                                      color: Colors.black,
                                      title: "Lý do nghỉ phép",
                                      content: "${detail.reason}",
                                      size: size,
                                    ),
                                    SizedBox(
                                      height: 300.0 *
                                          double.parse(
                                            detail.apprInf!.length.toString(),
                                          ),
                                      width: size.width,
                                      child: ListView.builder(
                                          physics:
                                              const NeverScrollableScrollPhysics(),
                                          itemCount: detail.apprInf!.length,
                                          itemBuilder: (context, index) {
                                            var apprInf =
                                                detail.apprInf![index];
                                            return _buildListApprove(
                                              size: size,
                                              firstName: apprInf.approFirstName
                                                  .toString(),
                                              lastName: apprInf.approLastName
                                                  .toString(),
                                              approveDate: day.format(
                                                DateTime.parse(
                                                  apprInf.approvalDate
                                                      .toString(),
                                                ),
                                              ),
                                              approveJobName: apprInf
                                                  .approJobName
                                                  .toString(),
                                              comemt:
                                                  apprInf.comment.toString(),
                                              stateName:
                                                  apprInf.stateName.toString(),
                                            );
                                          }),
                                    ),
                                  ],
                                );
                    }
                    return const Center(
                      child: CircularProgressIndicator(
                        color: Colors.orangeAccent,
                      ),
                    );
                  }),
            ),
          ),
        ),
      );
    } else {
      return Scaffold(
        appBar: AppBar(
          title: Text(
            "Chi tiết đơn xin nghỉ",
            style: TextStyle(
              color: Theme.of(context).primaryColorDark,
            ),
          ),
          centerTitle: true,
          leading: IconButton(
            onPressed: () {
              Get.back();
            },
            icon: Icon(
              Icons.arrow_back_ios_new_outlined,
              color: Theme.of(context).primaryColorDark,
              size: 25,
            ),
          ),
          backgroundColor: Colors.orangeAccent,
        ),
        body: SizedBox(
          height: size.height,
          width: size.width,
          child: const Center(
            child: CircularProgressIndicator(
              color: Colors.orangeAccent,
            ),
          ),
        ),
      );
    }
  }

  Widget _buildListApprove({
    required Size size,
    required String approveDate,
    required String firstName,
    required String lastName,
    required String approveJobName,
    required String comemt,
    required String stateName,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 10),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Card(
            child: SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: Padding(
                        padding: EdgeInsets.only(
                          left: size.width * 0.05,
                        ),
                        child: const Text(
                          "Người duyệt",
                          style: TextStyle(color: Colors.green),
                        )),
                  ),
                  Expanded(
                    flex: 4,
                    // ignore: prefer_interpolation_to_compose_strings
                    child: Text(lastName + " " + firstName),
                  ),
                ],
              ),
            ),
          ),
          Card(
            child: SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: Padding(
                        padding: EdgeInsets.only(
                          left: size.width * 0.05,
                        ),
                        child: const Text("Ngày duyệt")),
                  ),
                  Expanded(
                    flex: 4,
                    child: Text(approveDate),
                  ),
                ],
              ),
            ),
          ),
          Card(
            child: SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: Padding(
                        padding: EdgeInsets.only(
                          left: size.width * 0.05,
                        ),
                        child: const Text("Chức vụ")),
                  ),
                  Expanded(
                    flex: 4,
                    child: Text(approveJobName),
                  ),
                ],
              ),
            ),
          ),
          Card(
            child: SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: Padding(
                        padding: EdgeInsets.only(
                          left: size.width * 0.05,
                        ),
                        child: const Text("Lý do")),
                  ),
                  Expanded(
                    flex: 4,
                    child: Text(comemt),
                  ),
                ],
              ),
            ),
          ),
          Card(
            child: SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: Padding(
                        padding: EdgeInsets.only(
                          left: size.width * 0.05,
                        ),
                        child: const Text("Tình trạng ")),
                  ),
                  Expanded(
                    flex: 4,
                    child: Text(stateName),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReason({
    required Size size,
    required String title,
    required String hintText,
    required int maxLines,
    required double height,
    required TextEditingController controller,
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
                      top: 25,
                      left: 20,
                      bottom: 20,
                      right: 20,
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

  Widget _buildDayFree(Size size, String hintText) {
    return Card(
      child: SizedBox(
        height: 60,
        child: Row(
          children: [
            Expanded(
              flex: 7,
              child: Padding(
                padding: EdgeInsets.only(
                  left: size.width * 0.05,
                ),
                child: const Text("Số ngày nghỉ"),
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
                    height: 60,
                    width: size.width * 0.35,
                    margin: const EdgeInsets.only(left: 10),
                    child: TextFormField(
                      textAlign: TextAlign.left,
                      controller: controller.dayController,
                      decoration: InputDecoration(
                        contentPadding: const EdgeInsets.only(
                          top: 25,
                          // left: 10,
                          right: 10,
                          bottom: 10,
                        ),
                        hintText: hintText,
                        border: InputBorder.none,
                        isDense: true,
                        // icon: const Icon(
                        //   Icons.calendar_month,
                        //   color: Colors.orangeAccent,
                        //   size: 25,
                        // ),
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
              flex: 7,
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
                    height: 60,
                    width: size.width * 0.35,
                    margin: const EdgeInsets.only(left: 10),
                    child: TextFormField(
                      textAlign: TextAlign.left,
                      onTap: onTap,
                      controller: controller,
                      decoration: InputDecoration(
                        contentPadding: const EdgeInsets.only(
                          top: 25,
                          // left: 10,
                          right: 10,
                          bottom: 10,
                        ),
                        hintText: hintText,
                        border: InputBorder.none,
                        isDense: true,
                        // icon: const Icon(
                        //   Icons.calendar_month,
                        //   color: Colors.orangeAccent,
                        //   size: 25,
                        // ),
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

  Widget _buildLoaiPhep(Size size, DetailSingleModel items, String hintText) {
    // ignore: unused_local_variable
    var detail = items.rData;
    return Card(
      child: SizedBox(
        height: 80,
        child: Row(
          children: [
            Expanded(
              flex: 7,
              child: Padding(
                  padding: EdgeInsets.only(
                    left: size.width * 0.05,
                  ),
                  child: const Text("Loại phép")),
            ),
            Expanded(
              flex: 5,
              child: Theme(
                data: ThemeData(
                  inputDecorationTheme:
                      const InputDecorationTheme(border: InputBorder.none),
                ),
                child: DropdownSearch<ListOffTypeModel>(
                  asyncItems: (String? query) {
                    return controller.getTypeOff(query);
                  },
                  popupProps: PopupProps.dialog(
                    showSelectedItems: true,
                    itemBuilder: _customPopupItemBuilderExample2,
                    showSearchBox: true,
                  ),
                  compareFn: (item, sItem) {
                    return item.note == sItem.note;
                  },
                  onChanged: (ListOffTypeModel? newValue) {
                    controller.selectedLoaiPhep =
                        newValue!.offTypeID.toString();
                  },
                  dropdownDecoratorProps: DropDownDecoratorProps(
                    dropdownSearchDecoration: InputDecoration(
                      hintText: hintText,
                      hintStyle: const TextStyle(
                        fontSize: 15,
                        color: Colors.black,
                      ),
                      filled: true,
                      iconColor: const Color(0xFFF3BD60),
                      focusColor: const Color(0xFFF3BD60),
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
      {required String title,
      required String content,
      required Size size,
      required Color color}) {
    return Card(
      child: SizedBox(
        height: 50,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Expanded(
              flex: 6,
              child: Padding(
                  padding: EdgeInsets.only(
                    left: size.width * 0.05,
                  ),
                  child: Text(title)),
            ),
            Expanded(
              flex: 4,
              child: Text(
                content,
                style: TextStyle(
                  color: color,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFormStatusText({
    required String title,
    required String content,
    required Size size,
    required Color color,
  }) {
    return Card(
      child: SizedBox(
        height: 50,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Expanded(
              flex: 6,
              child: Padding(
                  padding: EdgeInsets.only(
                    left: size.width * 0.05,
                  ),
                  child: Text(title)),
            ),
            Expanded(
              flex: 4,
              child: Text(
                content,
                style: TextStyle(
                  color: color,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
