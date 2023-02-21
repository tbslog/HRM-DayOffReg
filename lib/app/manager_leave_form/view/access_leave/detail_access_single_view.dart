import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/controller/detail_access_single_controller.dart';

class DetailAccessSingleView extends GetView<DetailAccessSingleController> {
  const DetailAccessSingleView(this.regID, {super.key});
  final int regID;

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    // ignore: unnecessary_null_comparison
    if (regID != null) {
      return GetBuilder<DetailAccessSingleController>(
        init: DetailAccessSingleController(),
        builder: (controller) => SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 15),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  FutureBuilder(
                      future: controller.detailSingle(regID: regID),
                      builder: (context, snapshot) {
                        if (snapshot.hasData) {
                          var items = snapshot.data as DetailSingleModel;
                          var detail = items.rData;
                          return Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            children: [
                              _buildFormText(
                                title: "MSNV",
                                content: "${detail!.empID}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Loại phép",
                                content: "${detail.type}",
                                size: size,
                              ),
                              FutureBuilder(
                                  future: controller.getInfoClient(
                                      empId: "${detail.empID}"),
                                  builder: (context, snapshot) {
                                    if (snapshot.hasData) {
                                      var itemsClient =
                                          snapshot.data as UserModel;
                                      return Column(
                                        children: [
                                          _buildFormText(
                                            title: "Tên nhân viên",
                                            content:
                                                "${itemsClient.lastName} ${itemsClient.firstName}",
                                            size: size,
                                          ),
                                          _buildFormText(
                                            title: "Bộ phận",
                                            content:
                                                "${itemsClient.jobpositionName}",
                                            size: size,
                                          ),
                                        ],
                                      );
                                    }
                                    return Container();
                                  }),
                              _buildFormText(
                                title: "Số ngày nghỉ",
                                content: "${detail.period}",
                                size: size,
                              ),
                              _buildFormText(
                                title: "Lý do nghỉ phép",
                                content: "${detail.reason}",
                                size: size,
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
                ],
              )),
        ),
      );
    }
    return SizedBox(
      height: size.height,
      width: size.width,
      child: const Center(
        child: CircularProgressIndicator(
          color: Colors.orangeAccent,
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

  // ignore: unused_element
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
