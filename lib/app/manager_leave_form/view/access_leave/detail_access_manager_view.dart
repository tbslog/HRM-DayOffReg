import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/controller/detail_access_single_controller.dart';

// ignore: must_be_immutable
class DetailAccessManagerView extends GetView<DetailAccessSingleController> {
  DetailAccessManagerView(this.regID, {super.key});
  final int regID;

  @override
  var controller = Get.put(DetailAccessSingleController());

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    var timeNow = DateTime.now();
    var day = DateFormat("dd/MM/yyyy");
    // ignore: unnecessary_null_comparison
    if (regID != null) {
      return SingleChildScrollView(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: FutureBuilder(
              future: controller.detailSingle(regID: regID),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  var items = snapshot.data as DetailSingleModel;
                  var detail = items.rData;

                  return Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      _buildFormText(
                        title: "Trạng thái",
                        content: detail!.aStatus == 1
                            ? "Chờ duyệt"
                            : detail.aStatus == 2
                                ? "Đồng ý"
                                : "Từ chối",
                        size: size,
                      ),
                      _buildFormText(
                        title: "Ngày duyệt",
                        content: day.format(
                          DateTime.parse(
                            timeNow.toString(),
                          ),
                        ),
                        size: size,
                      ),
                      FutureBuilder(
                          future: controller.getInfo(),
                          builder: (context, snapshot) {
                            if (snapshot.hasData) {
                              var items = snapshot.data as UserModel;
                              return Column(
                                children: [
                                  _buildFormText(
                                    title: "Người duyệt",
                                    content:
                                        "${items.lastName} ${items.firstName}",
                                    size: size,
                                  ),
                                  _buildFormText(
                                    title: "Chức vụ",
                                    content: "${items.jobpositionName}",
                                    size: size,
                                  ),
                                ],
                              );
                            }
                            return Container();
                          }),
                      detail.aStatus == 1
                          ? _buildReason(
                              height: 120,
                              hintText: 'Nhập ý kiến ',
                              maxLines: 3,
                              size: size,
                              title: 'Ý kiến',
                              controller: controller.reasonManagerController,
                            )
                          : _buildFormText(
                              title: "Ý kiến",
                              content: items.rData!.apprInf!.isEmpty
                                  ? "${items.rData!.apprInf![0].comment}"
                                  : "",
                              size: size,
                            ),
                      // ignore: unrelated_type_equality_checks
                      detail.aStatus == 1
                          ? SizedBox(
                              height: 60,
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceAround,
                                children: [
                                  TextButton(
                                    style: ButtonStyle(
                                      backgroundColor:
                                          MaterialStateProperty.all<Color>(
                                        Colors.yellow.shade800,
                                      ),
                                    ),
                                    onPressed: () {
                                      controller.postApprove(
                                        regID: regID,
                                        comment: controller
                                            .reasonManagerController.text,
                                        state: 0,
                                      );
                                    },
                                    child: const Text(
                                      "Không Duyệt",
                                      style: TextStyle(
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                  TextButton(
                                    style: ButtonStyle(
                                      backgroundColor:
                                          MaterialStateProperty.all<Color>(
                                        Colors.green,
                                      ),
                                    ),
                                    onPressed: () {
                                      controller.postApprove(
                                        regID: regID,
                                        comment: controller
                                            .reasonManagerController.text,
                                        state: 1,
                                      );
                                    },
                                    child: const Text(
                                      "Duyệt",
                                      style: TextStyle(
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            )
                          : Container(),
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
      );
    }
    return Container();
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
                    padding: EdgeInsets.symmetric(
                      horizontal: size.width * 0.05,
                    ),
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
                  validator: (value) {
                    if (value == null || value == "") {
                      return 'Nhập lý do';
                    }
                    return null;
                  },
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

  Widget _buildFormText(
      {required String title, required String content, required Size size}) {
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
              child: Text(content),
            ),
          ],
        ),
      ),
    );
  }
}
